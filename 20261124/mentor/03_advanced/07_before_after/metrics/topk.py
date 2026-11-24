"""단계별 역할 분리: metrics/topk.py / 독립 실행은 main.py. """

def compare_rankings(before, after, gold):
    """고정한 관련 문서 ID를 Top-2에 포함했는지 확인합니다."""
    # BEGIN D27-07-A01
    # ANSWER D27-07-A01: 고정한 관련 문서 ID를 Top-2에 포함했는지 확인합니다.
    # 1. 입력: before, after, gold (필요한 값만 받습니다.)
    # 2. 절차: 고정한 관련 문서 ID를 Top-2에 포함했는지 확인합니다.
    # 3. 반환: 호출한 Stage가 사용할 값/상태를 반환합니다.
    # 4. 주의: 오류를 빈 결과로 숨기지 않고 출처·필터 계약을 유지합니다.
    from coursekit.evaluation import compare_lists
    return compare_lists(before,after,gold,k=2)
    # END D27-07-A01
