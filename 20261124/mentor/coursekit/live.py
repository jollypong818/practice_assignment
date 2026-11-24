"""E5 GPU Embedding + PostgreSQL/pgvector. Day26 E5 계약과 동일한 Prefix·Normalization."""
from functools import lru_cache
from coursekit.config import MODEL_ID, DIMENSION, require_cuda, db_options, schema_name
import os

@lru_cache(maxsize=3)
def _encoder(revision,device):
    from sentence_transformers import SentenceTransformer
    model=SentenceTransformer(MODEL_ID,revision=revision,device=device)
    if model.get_sentence_embedding_dimension()!=DIMENSION:
        raise RuntimeError('E5와 저장 Schema의 Embedding 차원이 다릅니다.')
    return model

def load_encoder():
    from coursekit.config import load_env
    load_env()
    revision=os.getenv('E5_REVISION','main')
    return _encoder(revision,require_cuda())

def embedding_contract(model):
    if model.get_sentence_embedding_dimension()!=DIMENSION:raise ValueError('E5 DIM mismatch')
    revision=None
    try:revision=model[0].auto_model.config._commit_hash
    except (AttributeError,IndexError,TypeError):pass
    return {'model_id':MODEL_ID,'revision':str(revision or os.getenv('E5_REVISION','main')),
            'dimension':DIMENSION,'query_prefix':'query: ','passage_prefix':'passage: ',
            'normalized':True,'max_seq_length':int(model.max_seq_length)}

def encode(model,text,prefix):
    import numpy as np
    if not isinstance(text,str) or not text.strip():raise ValueError('빈 Embedding 입력')
    full=prefix+text
    tokens=model.tokenizer(full,truncation=False,add_special_tokens=True)['input_ids']
    if len(tokens)>model.max_seq_length:
        raise ValueError(f'E5 Token 초과: {len(tokens)} > {model.max_seq_length}. 청크를 다시 구성하세요.')
    v=np.asarray(model.encode(full,normalize_embeddings=True,convert_to_numpy=True),dtype=np.float32)
    if v.shape!=(DIMENSION,) or not np.isfinite(v).all():raise ValueError('잘못된 Embedding')
    if abs(float(np.linalg.norm(v))-1)>1e-3:raise ValueError('E5 벡터 정규화 오류')
    return v

def open_db():
    """pgvector 확장을 선행 설치해야 합니다. import만으로 DB에 접속하지 않습니다."""
    import psycopg
    from psycopg import sql
    from pgvector.psycopg import register_vector
    conn=psycopg.connect(**db_options(),autocommit=True)
    try:
        v=conn.execute('SELECT n.nspname FROM pg_catalog.pg_extension e '
                       'JOIN pg_catalog.pg_namespace n ON e.extnamespace=n.oid '
                       'WHERE e.extname=%s',('vector',)).fetchone()
        if v is None:raise RuntimeError('DB에 pgvector 확장이 없습니다. CREATE EXTENSION vector 확인')
        conn.execute(sql.SQL('SET search_path TO {}, {}, pg_catalog').format(sql.Identifier(schema_name()),sql.Identifier(v[0])))
        register_vector(conn)
        return conn
    except Exception:
        conn.close()
        raise


def make_live_search(model=None,connector=None):
    """실제 E5 검색 함수. 실행 오류를 빈 후보 목록으로 위장하지 않습니다."""
    from coursekit.db import search_db
    model=load_encoder() if model is None else model
    connector=open_db if connector is None else connector
    contract=embedding_contract(model)
    def search(question,category='시설',k=5,role='learner'):
        vector=encode(model,question,'query: ')
        with connector() as conn:
            rows=search_db(conn,vector,category,k,role,contract)
        from coursekit.documents import hit_to_document
        return [hit_to_document(hit) for hit in rows]
    return search


def make_live_retriever(search=None):
    """LangChain RunnableLambda. 호출 시 실제 Embedding·DB 검색."""
    from langchain_core.runnables import RunnableLambda
    search=make_live_search() if search is None else search
    return RunnableLambda(lambda req:search(req['query'],req['category'],req.get('candidate_k',5),req.get('role','learner')))
