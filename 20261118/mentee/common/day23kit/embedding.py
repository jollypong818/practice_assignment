from __future__ import annotations
import numpy as np
from .data import E5_MODEL_ID, DIMS, passage_text, query_text
from .fixtures import SimulatedEncoder

def get_encoder(mode='fixture'):
    if mode=='fixture': return SimulatedEncoder()
    if mode!='live': raise ValueError('mode는 fixture 또는 live')
    # 실습에서 명시적으로 live를 선택한 경우에만 네트워크 모델 로드 가능.
    import torch
    torch.set_num_threads(1)
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(E5_MODEL_ID,device='cpu')

def get_model_revision(encoder):
    if isinstance(encoder,SimulatedEncoder):return 'simulated_not_e5'
    try:
        model=encoder._first_module().auto_model
        return getattr(model.config,'_commit_hash',None) or 'unverified'
    except (AttributeError, TypeError):return 'unverified'

def encode_passages(encoder,rows):
    texts=[passage_text(r) for r in rows]
    vectors=encoder.encode(texts,normalize_embeddings=True,convert_to_numpy=True,batch_size=8)
    return np.asarray(vectors,dtype=np.float32)

def encode_question(encoder,question):
    if not isinstance(question,str) or not question.strip():raise ValueError('빈 질문')
    vectors=encoder.encode([query_text(question)],normalize_embeddings=True,convert_to_numpy=True)
    return np.asarray(vectors,dtype=np.float32)[0]

def validate_vectors(vectors,n):
    arr=np.asarray(vectors,dtype=np.float32)
    if arr.shape!=(n,DIMS):raise ValueError('벡터 shape/차원 오류')
    if not np.isfinite(arr).all():raise ValueError('NaN·Inf 오류')
    lengths=np.linalg.norm(arr,axis=1)
    if np.any(lengths<=1e-12):raise ValueError('영벡터 오류')
    if not np.allclose(lengths,1,rtol=0,atol=1e-5):raise ValueError('정규화 오류')
    return arr
