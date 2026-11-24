"""단계별 역할 분리: schemas/result.py / 독립 실행은 main.py. """

def record_rewrite(original, result):
    """원래 질문을 검색 질문으로 덮어쓰지 않습니다."""
    # BEGIN D27-02-A02
    # ANSWER D27-02-A02: 원래 질문을 검색 질문으로 덮어쓰지 않습니다.
    # 1. 입력: original, result (필요한 값만 받습니다.)
    # 2. 절차: 원래 질문을 검색 질문으로 덮어쓰지 않습니다.
    # 3. 반환: 호출한 Stage가 사용할 값/상태를 반환합니다.
    # 4. 주의: 오류를 빈 결과로 숨기지 않고 출처·필터 계약을 유지합니다.
    return {'original_question':original,'search_query':result.search_query,
            'status':result.status,'reason':result.reason}
    # END D27-02-A02
