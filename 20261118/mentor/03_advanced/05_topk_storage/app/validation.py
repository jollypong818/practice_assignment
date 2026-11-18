# Day23 / 실습 05 / 심화 validation / mentor
from day23kit.data import validate_snapshot
from day23kit.embedding import validate_vectors


# BEGIN D23-05-A05
def check_search_options(k,category):
    """
    [강사용 정답] D23-05-A05 · check_search_options
        k는 bool을 제외한 정수 1~9, category는 None 또는 course/development/support인지 검사하세요.
        잘못된 값은 ValueError. 정상 시 {'k':k,'category':category} 반환.
    """
    # 해설 D23-05-A05: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    if type(k) is not int or not 1<=k<=9:raise ValueError('invalid_k')
    if category is not None and category not in ('course','development','support'):
        raise ValueError('invalid_category')
    return {'k':k,'category':category}
# END D23-05-A05

# BEGIN D23-05-A06
def check_id_vector_integrity(rows,vectors):
    """
    [강사용 정답] D23-05-A06 · check_id_vector_integrity
        지식 ID 중복·누락·벡터 행 수/차원/유한값/norm을 검사하세요.
        기존 원문과 행 순서를 유지하며 정상일 때 True를 반환합니다.
        실제 DB 저장 전 검증에 사용합니다.
    """
    # 해설 D23-05-A06: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    validate_snapshot(rows)
    validate_vectors(vectors,len(rows))
    if sorted(r['id'] for r in rows)!=list(range(101,110)):
        raise ValueError('knowledge_id_set_changed')
    for r in rows:
        expected='knowledge_v1' if r['id']<=103 else 'knowledge_search_v2'
        if r['source_version'] != expected:raise ValueError('source_version_mismatch')
    return True
# END D23-05-A06
