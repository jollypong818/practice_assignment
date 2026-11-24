"""단계별 역할 분리: steps.py / 독립 실행은 main.py. """

def make_service_chain(offline):
    """Rewrite → Retrieve → Rerank → Context → Generation·Validation을 연결합니다."""
    # BEGIN D27-08-I01
    # TODO D27-08-I01: Rewrite → Retrieve → Rerank → Context → Generation·Validation을 연결합니다.
    # 반환값과 예외 조건은 README.md의 수행 기준을 따르세요.
    raise NotImplementedError("D27-08-I01 미완성")
    # END D27-08-I01


def wire_fastapi(chain):
    """API 요청의 role 문자열을 신뢰하지 않고 서버에서 learner 역할을 지정합니다."""
    # BEGIN D27-08-I02
    # TODO D27-08-I02: API 요청의 role 문자열을 신뢰하지 않고 서버에서 learner 역할을 지정합니다.
    # 반환값과 예외 조건은 README.md의 수행 기준을 따르세요.
    raise NotImplementedError("D27-08-I02 미완성")
    # END D27-08-I02
