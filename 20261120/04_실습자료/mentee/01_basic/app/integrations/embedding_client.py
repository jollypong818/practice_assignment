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
    """TODO B-10 · encode() — mentor와 동일한 함수 계약을 완성하세요."""
    # TODO B-10: E5 query/passage Prefix, normalize_embeddings=True, max_seq_length
    # TODO B-10: 검증, 384차원 벡터를 반환하세요. 실제 모델 호출만 성공으로 인정합니다.
    # 입력·반환형과 예외·상태코드는 요구사항 명세서/API 계약을 참조합니다.
    # 정답 구현 후 아래 예외를 지우고 로직을 작성하세요.
    raise NotImplementedError("B-10 · encode() TODO 미완성")

def overview_hash(s:str)->str:
    # 해시 기준: 저장된 Overview의 UTF-8 원문. Prefix는 저장해시에서 제외합니다.
    return hashlib.sha256(s.encode('utf-8')).hexdigest()
