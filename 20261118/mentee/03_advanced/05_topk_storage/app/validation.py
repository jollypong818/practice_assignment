# Day23 / 실습 05 / 심화 validation / mentee
from day23kit.data import validate_snapshot
from day23kit.embedding import validate_vectors


# BEGIN D23-05-A05
def check_search_options(k,category):
    """
    TODO D23-05-A05 · check_search_options
        k는 bool을 제외한 정수 1~9, category는 None 또는 course/development/support인지 검사하세요.
        잘못된 값은 ValueError. 정상 시 {'k':k,'category':category} 반환.
    """
    # TODO D23-05-A05: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-05-A05: 직접 구현하세요")
# END D23-05-A05

# BEGIN D23-05-A06
def check_id_vector_integrity(rows,vectors):
    """
    TODO D23-05-A06 · check_id_vector_integrity
        지식 ID 중복·누락·벡터 행 수/차원/유한값/norm을 검사하세요.
        기존 원문과 행 순서를 유지하며 정상일 때 True를 반환합니다.
        실제 DB 저장 전 검증에 사용합니다.
    """
    # TODO D23-05-A06: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-05-A06: 직접 구현하세요")
# END D23-05-A06
