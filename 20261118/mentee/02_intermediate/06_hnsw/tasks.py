# Day23 / 실습 06 / 응용 / mentee
from day23kit.db import HNSW_SQL

# BEGIN D23-06-I01
def create_index_sql():
    """
    TODO D23-06-I01 · create_index_sql
        day23_search_docs.embedding의 Cosine HNSW 인덱스를 정의하세요.
        USING hnsw (embedding vector_cosine_ops)를 사용합니다.
        인덱스는 선택 항목이며 9건에서 빠른 성능을 보장하지 않습니다.
    """
    # TODO D23-06-I01: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-06-I01: 직접 구현하세요")
# END D23-06-I01

# BEGIN D23-06-I02
def explain_sql():
    """
    TODO D23-06-I02 · explain_sql
        SELECT id FROM day23_search_docs를 거리순으로 검색하는
        EXPLAIN (ANALYZE, BUFFERS) SQL을 작성하세요. 바인딩은 %s 두 개.
        인덱스 사용 여부를 임의로 주장하면 안 됩니다.
    """
    # TODO D23-06-I02: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-06-I02: 직접 구현하세요")
# END D23-06-I02

# BEGIN D23-06-I03
def read_scan_type(plan_lines):
    """
    TODO D23-06-I03 · read_scan_type
        PostgreSQL EXPLAIN 텍스트에서 Index Scan / Seq Scan / 기타를 구분하세요.
        계획이 없으면 unknown, index가 있으면 index, seq면 seq로 반환합니다.
        작은 9건 테이블에서 Seq Scan은 오류가 아닙니다.
    """
    # TODO D23-06-I03: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-06-I03: 직접 구현하세요")
# END D23-06-I03

# BEGIN D23-06-I04
def check_operator_compatibility(sql,operator_class):
    """
    TODO D23-06-I04 · check_operator_compatibility
        SQL이 cosine <=> 를 사용하면 vector_cosine_ops가 맞는지 검사하세요.
        불일치 시 ValueError, 정상 시 True.
        L2 / negative inner product와 혼동하지 않습니다.
    """
    # TODO D23-06-I04: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-06-I04: 직접 구현하세요")
# END D23-06-I04

# BEGIN D23-06-I05
def compare_topk(exact_ids,ann_ids):
    """
    TODO D23-06-I05 · compare_topk
        Exact Top-k와 ANN Top-k의 ID 집합 일치율을 계산하세요.
        겹치는 ID 수 / exact_ids 수. 빈 exact_ids는 None.
        인덱스 속도나 모델 품질을 만들어 내면 안 됩니다.
    """
    # TODO D23-06-I05: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-06-I05: 직접 구현하세요")
# END D23-06-I05
