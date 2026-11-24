"""단계별 역할 분리: services/quality.py / 독립 실행은 main.py. """

def check_query_list(queries):
    """검색 요청 수와 중복 여부를 기록합니다."""
    # BEGIN D27-03-A03
    # ANSWER D27-03-A03: 검색 요청 수와 중복 여부를 기록합니다.
    # 1. 입력: queries (필요한 값만 받습니다.)
    # 2. 절차: 검색 요청 수와 중복 여부를 기록합니다.
    # 3. 반환: 호출한 Stage가 사용할 값/상태를 반환합니다.
    # 4. 주의: 오류를 빈 결과로 숨기지 않고 출처·필터 계약을 유지합니다.
    return {'count':len(queries),'unique':len(queries)==len(set(queries)),
            'within_limit':len(queries)<=3}
    # END D27-03-A03


def audit_candidate_merge(pairs, merged):
    """중복 제거 후에도 출처가 보존되고 호출 횟수 상한을 지키는지 검사합니다."""
    # BEGIN D27-03-A04
    # ANSWER D27-03-A04: 중복 제거 후에도 출처가 보존되고 호출 횟수 상한을 지키는지 검사합니다.
    # 1. 입력: pairs, merged (필요한 값만 받습니다.)
    # 2. 절차: 중복 제거 후에도 출처가 보존되고 호출 횟수 상한을 지키는지 검사합니다.
    # 3. 반환: 호출한 Stage가 사용할 값/상태를 반환합니다.
    # 4. 주의: 오류를 빈 결과로 숨기지 않고 출처·필터 계약을 유지합니다.
    ids=[d.metadata['chunk_id'] for d in merged]
    return {'unique_ids':len(ids)==len(set(ids)),
            'source_preserved':all(d.metadata.get('citation_id') and
               d.metadata.get('source_locator') for d in merged),
            'query_runs':len(pairs)}
    # END D27-03-A04
