"""단계별 역할 분리: checks.py / 독립 실행은 main.py. """

def check_semantics(original, result):
    """원 질문의 부정·숫자 조건을 임의로 변경하지 않았는지 점검합니다. 자동 검사만으로 의미 동일성을 보장하지 않습니다."""
    # BEGIN D27-02-I03
    # ANSWER D27-02-I03: 원 질문의 부정·숫자 조건을 임의로 변경하지 않았는지 점검합니다. 자동 검사만으로 의미 동일성을 보장하지 않습니다.
    # 1. 입력: original, result (필요한 값만 받습니다.)
    # 2. 절차: 원 질문의 부정·숫자 조건을 임의로 변경하지 않았는지 점검합니다. 자동 검사만으로 의미 동일성을 보장하지 않습니다.
    # 3. 반환: 호출한 Stage가 사용할 값/상태를 반환합니다.
    # 4. 주의: 오류를 빈 결과로 숨기지 않고 출처·필터 계약을 유지합니다.
    checks={'negation_preserved': True,'number_preserved':True}
    if result.status!='ready':return checks
    for key in ('안 ', '않', '아니', '취소하지'):
        if key in original and key not in result.search_query:checks['negation_preserved']=False
    import re
    numbers=re.findall(r'\d+',original)
    checks['number_preserved']=all(value in result.search_query for value in numbers)
    return checks
    # END D27-02-I03
