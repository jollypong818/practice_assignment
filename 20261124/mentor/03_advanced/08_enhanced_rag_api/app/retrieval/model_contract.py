"""검색과 Reranker가 공통으로 요구하는 ID·Metadata 검증."""
from coursekit.documents import valid_document

def validate_candidates(documents):
    return [valid_document(d) for d in documents]
