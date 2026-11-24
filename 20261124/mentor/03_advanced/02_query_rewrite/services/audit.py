"""단계별 역할 분리: services/audit.py / 독립 실행은 main.py. """

def audit_rewrite(case, row):
    """원 질문·History 규모와 의미 대조 필요성을 남깁니다."""
    # BEGIN D27-02-A04
    # ANSWER D27-02-A04: 원 질문·History 규모와 의미 대조 필요성을 남깁니다.
    # 1. 입력: case, row (필요한 값만 받습니다.)
    # 2. 절차: 원 질문·History 규모와 의미 대조 필요성을 남깁니다.
    # 3. 반환: 호출한 Stage가 사용할 값/상태를 반환합니다.
    # 4. 주의: 오류를 빈 결과로 숨기지 않고 출처·필터 계약을 유지합니다.
    return {'question_id':case['id'],'history_turns':len(case['history']),
              'status':row['status'],'changed':row['original_question']!=row['search_query'],
              'human_review_needed':True}
    # END D27-02-A04
