"""pgvector와 E5-small의 *실제 실행*을 위한 선택 도구.

준비되지 않은 DB나 모델을 fixture 성공으로 둔갑시키지 않습니다.
기존 테이블은 삭제하지 않으며 모든 수업 테이블은 ingest_로 시작합니다.
"""
from __future__ import annotations
from pathlib import Path
import os
from .io import ROLE_ROOT

MODEL_ID='intfloat/multilingual-e5-small'
DIM=384
PIPELINE_VERSION='ingest-e5-v1'


def connect_db():
    try:
        import psycopg
        from dotenv import dotenv_values
        from pgvector.psycopg import register_vector
    except ImportError as exc:
        raise RuntimeError('필요 패키지 없음: python -m pip install "psycopg[binary]" pgvector python-dotenv') from exc
    path=ROLE_ROOT/'.env'
    if not path.is_file():raise RuntimeError('mentor 또는 mentee 폴더에 .env를 생성하세요. .env.example 참고')
    cfg=dotenv_values(path,interpolate=False,encoding='utf-8-sig')
    fields=('PGHOST','PGPORT','PGDATABASE','PGUSER','PGPASSWORD')
    missing=[k for k in fields if not (os.environ.get(k) or cfg.get(k))]
    if missing:raise RuntimeError('DB 설정 누락: '+', '.join(missing))
    val=lambda k: os.environ.get(k) or cfg[k]
    try:
        conn=psycopg.connect(host=val('PGHOST'),port=int(val('PGPORT')),
            dbname=val('PGDATABASE'),user=val('PGUSER'),password=val('PGPASSWORD'),
            autocommit=True,connect_timeout=6)
        if conn.execute("SELECT 1 FROM pg_extension WHERE extname='vector'").fetchone() is None:
            conn.close();raise RuntimeError('선택 DB에 pgvector 미활성화: pgAdmin에서 CREATE EXTENSION vector 실행')
        register_vector(conn)
        return conn
    except psycopg.Error as exc:
        raise RuntimeError('DB 연결 또는 확장 확인 실패: '+type(exc).__name__) from None


def load_encoder():
    try:
        import torch
        from sentence_transformers import SentenceTransformer
    except ImportError as exc:
        raise RuntimeError('E5 실행 패키지 없음: python -m pip install sentence-transformers') from exc
    torch.set_num_threads(1)
    model=SentenceTransformer(MODEL_ID,device='cpu')
    if model.get_sentence_embedding_dimension()!=DIM:
        raise ValueError('E5 모델 출력 차원이 384가 아닙니다')
    return model


def encode_passages(model,chunks:list[dict]):
    import numpy as np
    from .processing import token_len
    if not chunks:raise ValueError('empty chunks')
    texts=[]
    for row in chunks:
        t=row['embedding_text']
        if not t.startswith('passage: '):raise ValueError('missing E5 passage prefix')
        if token_len(model,t)>model.max_seq_length:raise ValueError('rechunk required: model token limit')
        texts.append(t)
    vecs=model.encode(texts,batch_size=8,normalize_embeddings=True,convert_to_numpy=True)
    v=np.asarray(vecs,dtype=np.float32)
    if v.shape!=(len(chunks),DIM) or not np.isfinite(v).all():raise ValueError('bad vectors')
    if not np.allclose(np.linalg.norm(v,axis=1),1.,rtol=0,atol=1e-5):
        raise ValueError('embedding normalization error')
    return v


def encode_query(model, question: str):
    import numpy as np
    from .processing import e5_query, token_len
    text=e5_query(question)
    if token_len(model,text)>model.max_seq_length:raise ValueError('query too long')
    v=np.asarray(model.encode([text],normalize_embeddings=True,convert_to_numpy=True)[0],dtype=np.float32)
    if v.shape!=(DIM,) or not np.isfinite(v).all():raise ValueError('invalid query vector')
    return v
