"""단계별 역할 분리: checks.py / 독립 실행은 main.py. """

def metadata_check(docs, payload):
    """각 Document의 chunk_id·source_locator·Category를 검사합니다."""
    # BEGIN D27-04-I03
    # ANSWER D27-04-I03: 각 Document의 chunk_id·source_locator·Category를 검사합니다.
    # 1. 입력: docs, payload (필요한 값만 받습니다.)
    # 2. 절차: 각 Document의 chunk_id·source_locator·Category를 검사합니다.
    # 3. 반환: 호출한 Stage가 사용할 값/상태를 반환합니다.
    # 4. 주의: 오류를 빈 결과로 숨기지 않고 출처·필터 계약을 유지합니다.
    from coursekit.documents import valid_document
    return all(valid_document(d).metadata['category']==payload['category']
               for d in docs)
    # END D27-04-I03
