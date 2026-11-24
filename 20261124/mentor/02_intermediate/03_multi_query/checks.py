"""단계별 역할 분리: checks.py / 독립 실행은 main.py. """

def check_query_list(queries):
    """검색 요청 수와 중복 여부를 기록합니다."""
    # BEGIN D27-03-I03
    # ANSWER D27-03-I03: 검색 요청 수와 중복 여부를 기록합니다.
    # 1. 입력: queries (필요한 값만 받습니다.)
    # 2. 절차: 검색 요청 수와 중복 여부를 기록합니다.
    # 3. 반환: 호출한 Stage가 사용할 값/상태를 반환합니다.
    # 4. 주의: 오류를 빈 결과로 숨기지 않고 출처·필터 계약을 유지합니다.
    return {'count':len(queries),'unique':len(queries)==len(set(queries)),
            'within_limit':len(queries)<=3}
    # END D27-03-I03
