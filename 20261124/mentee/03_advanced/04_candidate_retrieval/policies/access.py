"""단계별 역할 분리: policies/access.py / 독립 실행은 main.py. """

def policy_check(docs, payload):
    """실제 권한 필터는 검색 SQL에서 적용합니다. 이 검사는 반환된 후보의 방어적 확인입니다."""
    # BEGIN D27-04-A04
    # TODO D27-04-A04: 실제 권한 필터는 검색 SQL에서 적용합니다. 이 검사는 반환된 후보의 방어적 확인입니다.
    # 반환값과 예외 조건은 README.md의 수행 기준을 따르세요.
    raise NotImplementedError("D27-04-A04 미완성")
    # END D27-04-A04
