# Day23 / 실습 07 / 심화 review / mentee
from day23kit.data import load_knowledge

from .reference import judge_training_reference

# BEGIN D23-07-A03
def make_review_row(case,hit):
    """
    TODO D23-07-A03 · make_review_row
        질문 ID·검색된 ID·본문·거리·교재 기준 라벨을 한 행으로 만드세요.
        distance는 정답 확률로 표현하지 않습니다.
        human_reviewed는 False로 두어 실제 수강생의 근거 검토 전임을 표시합니다.
    """
    # TODO D23-07-A03: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-07-A03: 직접 구현하세요")
# END D23-07-A03

# BEGIN D23-07-A04
def classify_search_state(rows,error=None):
    """
    TODO D23-07-A04 · classify_search_state
        데이터베이스 예외(error)는 error, 정상 조회 결과 []는 empty,
        후보가 있으면 candidates를 반환하세요. 결과 없음과 DB 장애를 섞지 마세요.
    """
    # TODO D23-07-A04: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-07-A04: 직접 구현하세요")
# END D23-07-A04

# BEGIN D23-07-A05
def review_filter_effect(before,after):
    """
    TODO D23-07-A05 · review_filter_effect
        필터 전후 ID 목록을 비교해 빠진 ID와 추가된 ID를 반환하세요.
        출력 {'removed': [...], 'added': [...]} 정렬된 목록.
        필터 때문에 k보다 적게 반환될 수 있습니다.
    """
    # TODO D23-07-A05: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-07-A05: 직접 구현하세요")
# END D23-07-A05

# BEGIN D23-07-A06
def check_evaluation_integrity(rows):
    """
    TODO D23-07-A06 · check_evaluation_integrity
        같은 case_id의 retrieved_id가 중복되면 ValueError.
        지식 101~109에 없는 ID나 원문 버전 불일치도 구분하세요.
        정상일 때 true. 주의: 이 검사는 사람의 관련성 평가를 대체하지 않습니다.
    """
    # TODO D23-07-A06: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-07-A06: 직접 구현하세요")
# END D23-07-A06
