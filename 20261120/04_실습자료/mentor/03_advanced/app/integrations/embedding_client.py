"""E5-small Adapter. 사용 전 SentenceTransformers·모델 가중치 준비 필요."""
from functools import lru_cache
import hashlib
from app.core.config import settings

@lru_cache(maxsize=1)
def get_model():
    import torch
    from sentence_transformers import SentenceTransformer
    torch.set_num_threads(1)
    return SentenceTransformer(settings.embedding_model,device='cpu')


def encode(texts:list[str],kind:str='passage')->list[list[float]]:
    if kind not in ('query','passage'):raise ValueError('kind는 query 또는 passage여야 합니다.')
    if not texts:return []
    prefixed=[f'{kind}: {s}' for s in texts]
    model=get_model()
    # 정규화 벡터 384차원 / query와 passage Prefix는 E5의 입력 계약입니다.
    # E5의 입력 한도를 초과하면 조용히 잘라서 다른 의미의 벡터를 만들 수 있습니다.
    # 학습자료가 아닌 실제 사용자 개요는 길이 초과를 명확히 거절합니다.
    tokenizer=getattr(model,'tokenizer',None)
    max_length=getattr(model,'max_seq_length',None)
    if tokenizer is not None and isinstance(max_length,int) and max_length>0:
        input_ids=tokenizer(prefixed,add_special_tokens=True,truncation=False)['input_ids']
        if any(len(ids)>max_length for ids in input_ids):
            raise ValueError(f'E5 토큰 길이가 모델 한도 {max_length}을 초과합니다.')
    vectors=model.encode(prefixed,normalize_embeddings=True,batch_size=16,
                         show_progress_bar=False)
    rows=[v.tolist() for v in vectors]
    if any(len(v)!=384 for v in rows):raise RuntimeError('Embedding 차원이 384가 아닙니다.')
    return rows

def overview_hash(s:str)->str:
    # 해시 기준: 저장된 Overview의 UTF-8 원문. Prefix는 저장해시에서 제외합니다.
    return hashlib.sha256(s.encode('utf-8')).hexdigest()
