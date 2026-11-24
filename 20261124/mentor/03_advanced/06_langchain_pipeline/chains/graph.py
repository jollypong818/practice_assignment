"""단계별 역할 분리: chains/graph.py / 독립 실행은 main.py. """

def wire_langchain_pipeline(dependencies, offline):
    """LCEL는 Runnable을 준비할 뿐이고 .invoke()가 실행 시작점입니다."""
    # BEGIN D27-06-A02
    # ANSWER D27-06-A02: LCEL는 Runnable을 준비할 뿐이고 .invoke()가 실행 시작점입니다.
    # 1. 입력: dependencies, offline (필요한 값만 받습니다.)
    # 2. 절차: LCEL는 Runnable을 준비할 뿐이고 .invoke()가 실행 시작점입니다.
    # 3. 반환: 호출한 Stage가 사용할 값/상태를 반환합니다.
    # 4. 주의: 오류를 빈 결과로 숨기지 않고 출처·필터 계약을 유지합니다.
    from coursekit.pipeline import create_rag_pipeline
    return create_rag_pipeline(*dependencies,offline=offline)
    # END D27-06-A02
