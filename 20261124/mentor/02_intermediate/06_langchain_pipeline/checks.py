"""단계별 역할 분리: checks.py / 독립 실행은 main.py. """

def validate_trace(result):
    """원 질문·검색용 질문·후보·Context ID를 각각 확인합니다."""
    # BEGIN D27-06-I03
    # ANSWER D27-06-I03: 원 질문·검색용 질문·후보·Context ID를 각각 확인합니다.
    # 1. 입력: result (필요한 값만 받습니다.)
    # 2. 절차: 원 질문·검색용 질문·후보·Context ID를 각각 확인합니다.
    # 3. 반환: 호출한 Stage가 사용할 값/상태를 반환합니다.
    # 4. 주의: 오류를 빈 결과로 숨기지 않고 출처·필터 계약을 유지합니다.
    t=result['trace'];return {'questions_separate':bool(t['original_question'] and t['search_query']),
            'ids_recorded':isinstance(t['candidate_ids'],list) and isinstance(t['included_ids'],list),
            'included_from_candidates':set(t['included_ids']).issubset(t['candidate_ids'])}
    # END D27-06-I03
