# Day23 / 실습 06 / 심화 index_sql / mentee
from day23kit.db import HNSW_SQL


# BEGIN D23-06-A01
def create_index_sql():
    """
    TODO D23-06-A01 · create_index_sql
        day23_search_docs.embedding의 Cosine HNSW 인덱스를 정의하세요.
        USING hnsw (embedding vector_cosine_ops)를 사용합니다.
        인덱스는 선택 항목이며 9건에서 빠른 성능을 보장하지 않습니다.
    """
    # TODO D23-06-A01: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-06-A01: 직접 구현하세요")
# END D23-06-A01

# BEGIN D23-06-A02
def explain_sql():
    """
    TODO D23-06-A02 · explain_sql
        SELECT id FROM day23_search_docs를 거리순으로 검색하는
        EXPLAIN (ANALYZE, BUFFERS) SQL을 작성하세요. 바인딩은 %s 두 개.
        인덱스 사용 여부를 임의로 주장하면 안 됩니다.
    """
    # TODO D23-06-A02: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-06-A02: 직접 구현하세요")
# END D23-06-A02
