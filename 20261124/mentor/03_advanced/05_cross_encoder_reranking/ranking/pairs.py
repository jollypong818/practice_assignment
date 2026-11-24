"""단계별 역할 분리: ranking/pairs.py / 독립 실행은 main.py. """

def create_pairs(question, docs):
    """CrossEncoder 입력은 [질문, 문서본문]의 쌍 목록입니다."""
    # BEGIN D27-05-A01
    # ANSWER D27-05-A01: CrossEncoder 입력은 [질문, 문서본문]의 쌍 목록입니다.
    # 1. 입력: question, docs (필요한 값만 받습니다.)
    # 2. 절차: CrossEncoder 입력은 [질문, 문서본문]의 쌍 목록입니다.
    # 3. 반환: 호출한 Stage가 사용할 값/상태를 반환합니다.
    # 4. 주의: 오류를 빈 결과로 숨기지 않고 출처·필터 계약을 유지합니다.
    return [(question,d.page_content) for d in docs]
    # END D27-05-A01
