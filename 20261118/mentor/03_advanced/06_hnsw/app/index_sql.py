# Day23 / 실습 06 / 심화 index_sql / mentor
from day23kit.db import HNSW_SQL


# BEGIN D23-06-A01
def create_index_sql():
    """
    [강사용 정답] D23-06-A01 · create_index_sql
        day23_search_docs.embedding의 Cosine HNSW 인덱스를 정의하세요.
        USING hnsw (embedding vector_cosine_ops)를 사용합니다.
        인덱스는 선택 항목이며 9건에서 빠른 성능을 보장하지 않습니다.
    """
    # 해설 D23-06-A01: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    return HNSW_SQL
# END D23-06-A01

# BEGIN D23-06-A02
def explain_sql():
    """
    [강사용 정답] D23-06-A02 · explain_sql
        SELECT id FROM day23_search_docs를 거리순으로 검색하는
        EXPLAIN (ANALYZE, BUFFERS) SQL을 작성하세요. 바인딩은 %s 두 개.
        인덱스 사용 여부를 임의로 주장하면 안 됩니다.
    """
    # 해설 D23-06-A02: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    return """EXPLAIN (ANALYZE, BUFFERS)
    SELECT id FROM day23_search_docs
    WHERE embedding_model=%s
    ORDER BY embedding <=> %s ASC LIMIT 3"""
# END D23-06-A02
