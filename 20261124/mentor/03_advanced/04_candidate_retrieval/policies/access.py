"""단계별 역할 분리: policies/access.py / 독립 실행은 main.py. """

def policy_check(docs, payload):
    """실제 권한 필터는 검색 SQL에서 적용합니다. 이 검사는 반환된 후보의 방어적 확인입니다."""
    # BEGIN D27-04-A04
    # ANSWER D27-04-A04: 실제 권한 필터는 검색 SQL에서 적용합니다. 이 검사는 반환된 후보의 방어적 확인입니다.
    # 1. 입력: docs, payload (필요한 값만 받습니다.)
    # 2. 절차: 실제 권한 필터는 검색 SQL에서 적용합니다. 이 검사는 반환된 후보의 방어적 확인입니다.
    # 3. 반환: 호출한 Stage가 사용할 값/상태를 반환합니다.
    # 4. 주의: 오류를 빈 결과로 숨기지 않고 출처·필터 계약을 유지합니다.
    return {'ready':all(d.metadata.get('ready',True) is True for d in docs),
            'current':all(d.metadata.get('is_current',True) is True for d in docs),
            'public':all(d.metadata.get('access_level','public')=='public' for d in docs)}
    # END D27-04-A04
