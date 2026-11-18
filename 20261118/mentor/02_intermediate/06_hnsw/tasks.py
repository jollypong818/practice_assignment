# Day23 / 실습 06 / 응용 / mentor
from day23kit.db import HNSW_SQL

# BEGIN D23-06-I01
def create_index_sql():
    """
    [강사용 정답] D23-06-I01 · create_index_sql
        day23_search_docs.embedding의 Cosine HNSW 인덱스를 정의하세요.
        USING hnsw (embedding vector_cosine_ops)를 사용합니다.
        인덱스는 선택 항목이며 9건에서 빠른 성능을 보장하지 않습니다.
    """
    # 해설 D23-06-I01: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    return HNSW_SQL
# END D23-06-I01

# BEGIN D23-06-I02
def explain_sql():
    """
    [강사용 정답] D23-06-I02 · explain_sql
        SELECT id FROM day23_search_docs를 거리순으로 검색하는
        EXPLAIN (ANALYZE, BUFFERS) SQL을 작성하세요. 바인딩은 %s 두 개.
        인덱스 사용 여부를 임의로 주장하면 안 됩니다.
    """
    # 해설 D23-06-I02: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    return """EXPLAIN (ANALYZE, BUFFERS)
    SELECT id FROM day23_search_docs
    WHERE embedding_model=%s
    ORDER BY embedding <=> %s ASC LIMIT 3"""
# END D23-06-I02

# BEGIN D23-06-I03
def read_scan_type(plan_lines):
    """
    [강사용 정답] D23-06-I03 · read_scan_type
        PostgreSQL EXPLAIN 텍스트에서 Index Scan / Seq Scan / 기타를 구분하세요.
        계획이 없으면 unknown, index가 있으면 index, seq면 seq로 반환합니다.
        작은 9건 테이블에서 Seq Scan은 오류가 아닙니다.
    """
    # 해설 D23-06-I03: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    s=' '.join(plan_lines)
    if 'Index Scan' in s:return 'index'
    if 'Seq Scan' in s:return 'seq'
    return 'unknown'
# END D23-06-I03

# BEGIN D23-06-I04
def check_operator_compatibility(sql,operator_class):
    """
    [강사용 정답] D23-06-I04 · check_operator_compatibility
        SQL이 cosine <=> 를 사용하면 vector_cosine_ops가 맞는지 검사하세요.
        불일치 시 ValueError, 정상 시 True.
        L2 / negative inner product와 혼동하지 않습니다.
    """
    # 해설 D23-06-I04: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    if '<=>' in sql and operator_class!='vector_cosine_ops':raise ValueError('operator_class_mismatch')
    return True
# END D23-06-I04

# BEGIN D23-06-I05
def compare_topk(exact_ids,ann_ids):
    """
    [강사용 정답] D23-06-I05 · compare_topk
        Exact Top-k와 ANN Top-k의 ID 집합 일치율을 계산하세요.
        겹치는 ID 수 / exact_ids 수. 빈 exact_ids는 None.
        인덱스 속도나 모델 품질을 만들어 내면 안 됩니다.
    """
    # 해설 D23-06-I05: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    if not exact_ids:return None
    return len(set(exact_ids)&set(ann_ids))/len(set(exact_ids))
# END D23-06-I05
