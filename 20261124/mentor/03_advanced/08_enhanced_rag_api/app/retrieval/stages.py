"""단계별 역할 분리: app/retrieval/stages.py / 독립 실행은 main.py. """

def make_service_chain(offline):
    """Rewrite → Retrieve → Rerank → Context → Generation·Validation을 연결합니다."""
    # BEGIN D27-08-A01
    # ANSWER D27-08-A01: Rewrite → Retrieve → Rerank → Context → Generation·Validation을 연결합니다.
    # 1. 입력: offline (필요한 값만 받습니다.)
    # 2. 절차: Rewrite → Retrieve → Rerank → Context → Generation·Validation을 연결합니다.
    # 3. 반환: 호출한 Stage가 사용할 값/상태를 반환합니다.
    # 4. 주의: 오류를 빈 결과로 숨기지 않고 출처·필터 계약을 유지합니다.
    from coursekit.runtime import create_demo_chain
    return create_demo_chain(offline=offline)
    # END D27-08-A01
