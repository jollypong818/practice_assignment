"""Day22 · 명시적 모델 선택 | PPT 53~59 | 03_advanced
공통 제공 코드는 교시 독립 시작점입니다. 본 파일의 TODO 함수를 실행 경로에 연결합니다.
"""
from coursekit.config import choose_model as checkpoint_choose

def route(mode, models):
    # TODO D22-07-A01: fast·quality만허용하고실제모델과선택이유를반환하세요.
    # 입력·완료 기준: 알수없는모드를fast로조용히바꾸지않습니다. quality권한없으면not_run입니다.
    # BEGIN D22-07-A01
    allowed = {"fast", "quality"}
    model = None   # models.get(mode), 미설정은오류
    reason = ""    # explicit_mode:<mode>
    # checkpoint_choose(mode, models)를이용할수있습니다.
    raise NotImplementedError("D22-07-A01: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-07-A01

def record_view(result):
    # TODO D22-07-A02: 어떤모델이든동일한결과필드로비교하세요.
    # 입력·완료 기준: 고가모델이항상더좋다는결론을미리넣지않습니다.
    # BEGIN D22-07-A02
    fields = ["case_id", "source_mode", "model", "route_reason", "run_status",
              "answer_object", "evidence_ok", "usage", "request_ms", "estimated_usd"]
    row = {}  # {key: result.get(key) for key in fields}
    raise NotImplementedError("D22-07-A02: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-07-A02

def comparison_modes():
    # TODO D22-07-A03: 명시적비교에서만fast·quality를한번씩선택하세요.
    # 입력·완료 기준: 기본run은한모델만호출합니다. compare는계정권한·예산확인후선택합니다.
    # BEGIN D22-07-A03
    modes = []  # fast와quality각한번, while fallback금지
    raise NotImplementedError("D22-07-A03: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-07-A03

def reject_unknown_mode():
    # TODO D22-07-A04: 잘못된mode가호출전에오류인지모의검사하세요.
    # 입력·완료 기준: 인증오류를다른모델이나계정으로우회하지않습니다.
    # BEGIN D22-07-A04
    # route("unknown", models)는ValueError여야합니다. 실제전송하지않습니다.
    raise NotImplementedError("D22-07-A04: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-07-A04

def check_unconfigured_quality():
    # TODO D22-07-A05: quality가미설정이면다른모델로자동대체하지않는지확인하세요.
    # 입력·완료 기준: 선택정책검사는simulated이고두모델실제비교와구분합니다.
    # BEGIN D22-07-A05
    from coursekit.config import SetupError
    # quality=None에대한예외를확인합니다.
    raise NotImplementedError("D22-07-A05: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-07-A05

def check_evidence_view():
    # TODO D22-07-A06: 자동검증결과를사람의근거승인으로만들지않는지확인하세요.
    # 입력·완료 기준: 공통결과구조의None을임의True로바꾸지않습니다.
    # BEGIN D22-07-A06
    row = record_view({"run_status":"validated", "evidence_ok":None})
    raise NotImplementedError("D22-07-A06: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-07-A06
