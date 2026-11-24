"""단계별 역할 분리: services/audit.py / 독립 실행은 main.py. """

def audit_comparison(row, offline):
    """시간·실행모드·비교 조건을 기록하고 단일 사례로 성능 개선을 단정하지 않습니다."""
    # BEGIN D27-07-A04
    # ANSWER D27-07-A04: 시간·실행모드·비교 조건을 기록하고 단일 사례로 성능 개선을 단정하지 않습니다.
    # 1. 입력: row, offline (필요한 값만 받습니다.)
    # 2. 절차: 시간·실행모드·비교 조건을 기록하고 단일 사례로 성능 개선을 단정하지 않습니다.
    # 3. 반환: 호출한 Stage가 사용할 값/상태를 반환합니다.
    # 4. 주의: 오류를 빈 결과로 숨기지 않고 출처·필터 계약을 유지합니다.
    return {'mode':'offline_fixture' if offline else 'live',
           'timing_nonnegative':row['search_ms']>=0 and row['rerank_ms']>=0,
           'repeat_needed':True,'causal_improvement_claim':False}
    # END D27-07-A04
