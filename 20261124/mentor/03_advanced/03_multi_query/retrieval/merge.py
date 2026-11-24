"""단계별 역할 분리: retrieval/merge.py / 독립 실행은 main.py. """

def merge_candidates(pairs):
    """chunk_id를 중복 제거 키로 사용하고 found_by_query를 Metadata에 기록합니다."""
    # BEGIN D27-03-A02
    # ANSWER D27-03-A02: chunk_id를 중복 제거 키로 사용하고 found_by_query를 Metadata에 기록합니다.
    # 1. 입력: pairs (필요한 값만 받습니다.)
    # 2. 절차: chunk_id를 중복 제거 키로 사용하고 found_by_query를 Metadata에 기록합니다.
    # 3. 반환: 호출한 Stage가 사용할 값/상태를 반환합니다.
    # 4. 주의: 오류를 빈 결과로 숨기지 않고 출처·필터 계약을 유지합니다.
    from coursekit.multi_query import merge_found
    return merge_found(pairs)
    # END D27-03-A02
