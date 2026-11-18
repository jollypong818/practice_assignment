# Day23 / 실습 07 / 응용 / mentee


# BEGIN D23-07-I01
def make_casebook():
    """
    TODO D23-07-I01 · make_casebook
        강의의 질문 3종과 확인할 지식 ID를 구성하세요.
        server(102), retention(101: 보관 기간 없음), error(103/108).
        자동 생성한 정답이 아니라 사람이 평가할 고정 기준 샘플임을 표시합니다.
    """
    # TODO D23-07-I01: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-07-I01: 직접 구현하세요")
# END D23-07-I01

# BEGIN D23-07-I02
def judge_training_reference(case_id,doc_id):
    """
    TODO D23-07-I02 · judge_training_reference
        교안에 미리 주어진 원문 근거로 관련/부분 관련/무관을 수동 기준표로 판정하세요.
        server:102 관련,106 부분 관련. retention:101 부분 관련(기간 없음).
        error:103,108 관련. 그 밖에는 무관.
        *이 표는 사람이 만든 교육용 기준이며 모델 검색 평가점수가 아닙니다.*
    """
    # TODO D23-07-I02: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-07-I02: 직접 구현하세요")
# END D23-07-I02

# BEGIN D23-07-I03
def make_review_row(case,hit):
    """
    TODO D23-07-I03 · make_review_row
        질문 ID·검색된 ID·본문·거리·교재 기준 라벨을 한 행으로 만드세요.
        distance는 정답 확률로 표현하지 않습니다.
        human_reviewed는 False로 두어 실제 수강생의 근거 검토 전임을 표시합니다.
    """
    # TODO D23-07-I03: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-07-I03: 직접 구현하세요")
# END D23-07-I03

# BEGIN D23-07-I04
def classify_search_state(rows,error=None):
    """
    TODO D23-07-I04 · classify_search_state
        데이터베이스 예외(error)는 error, 정상 조회 결과 []는 empty,
        후보가 있으면 candidates를 반환하세요. 결과 없음과 DB 장애를 섞지 마세요.
    """
    # TODO D23-07-I04: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-07-I04: 직접 구현하세요")
# END D23-07-I04

# BEGIN D23-07-I05
def review_filter_effect(before,after):
    """
    TODO D23-07-I05 · review_filter_effect
        필터 전후 ID 목록을 비교해 빠진 ID와 추가된 ID를 반환하세요.
        출력 {'removed': [...], 'added': [...]} 정렬된 목록.
        필터 때문에 k보다 적게 반환될 수 있습니다.
    """
    # TODO D23-07-I05: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-07-I05: 직접 구현하세요")
# END D23-07-I05
