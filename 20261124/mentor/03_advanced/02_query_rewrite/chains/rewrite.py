"""단계별 역할 분리: chains/rewrite.py / 독립 실행은 main.py. """

def apply_rewrite(question, history, offline):
    """offline이면 고정 예시, 기본 실행이면 실제 ChatPromptTemplate → Chat Model을 호출합니다."""
    # BEGIN D27-02-A01
    # ANSWER D27-02-A01: offline이면 고정 예시, 기본 실행이면 실제 ChatPromptTemplate → Chat Model을 호출합니다.
    # 1. 입력: question, history, offline (필요한 값만 받습니다.)
    # 2. 절차: offline이면 고정 예시, 기본 실행이면 실제 ChatPromptTemplate → Chat Model을 호출합니다.
    # 3. 반환: 호출한 Stage가 사용할 값/상태를 반환합니다.
    # 4. 주의: 오류를 빈 결과로 숨기지 않고 출처·필터 계약을 유지합니다.
    from coursekit.rewrite import rewrite_query
    return rewrite_query(question,history,offline=offline)
    # END D27-02-A01
