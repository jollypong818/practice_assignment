"""Day22 · 명시적 모델 선택 | PPT 53~59 | 02_intermediate
공통 제공 코드는 교시 독립 시작점입니다. 본 파일의 TODO 함수를 실행 경로에 연결합니다.
"""
from pathlib import Path
from coursekit.support import parse_args
from coursekit.config import choose_model as checkpoint_choose
from coursekit.labs import routing_lab

def route(mode, models):
    # TODO D22-07-I01: fast·quality만허용하고실제모델과선택이유를반환하세요.
    # 입력·완료 기준: 알수없는모드를fast로조용히바꾸지않습니다. quality권한없으면not_run입니다.
    # BEGIN D22-07-I01
    # 해설: 알수없는모드를fast로조용히바꾸지않습니다. quality권한없으면not_run입니다.
    if mode not in {"fast","quality"}:
        raise ValueError("지원하지 않는 실행 모드")
    return checkpoint_choose(mode,models)
    # END D22-07-I01

def record_view(result):
    # TODO D22-07-I02: 어떤모델이든동일한결과필드로비교하세요.
    # 입력·완료 기준: 고가모델이항상더좋다는결론을미리넣지않습니다.
    # BEGIN D22-07-I02
    # 해설: 고가모델이항상더좋다는결론을미리넣지않습니다.
    return {key:result.get(key) for key in ("case_id","source_mode","model","route_reason","run_status",
            "answer_object","evidence_ok","usage","request_ms","estimated_usd")}
    # END D22-07-I02

def comparison_modes():
    # TODO D22-07-I03: 명시적비교에서만fast·quality를한번씩선택하세요.
    # 입력·완료 기준: 기본run은한모델만호출합니다. compare는계정권한·예산확인후선택합니다.
    # BEGIN D22-07-I03
    # 해설: 기본run은한모델만호출합니다. compare는계정권한·예산확인후선택합니다.
    return ["fast","quality"]
    # END D22-07-I03

def reject_unknown_mode():
    # TODO D22-07-I04: 잘못된mode가호출전에오류인지모의검사하세요.
    # 입력·완료 기준: 인증오류를다른모델이나계정으로우회하지않습니다.
    # BEGIN D22-07-I04
    # 해설: 인증오류를다른모델이나계정으로우회하지않습니다.
    try:
        route("unknown",{"fast":"example"})
    except ValueError:
        return True
    raise AssertionError("잘못된모드를허용했습니다")
    # END D22-07-I04

HERE = Path(__file__).resolve().parent

def main():
    args=parse_args(HERE)
    routing_lab(args,router=route,record_view=record_view,compare_modes=comparison_modes)
    reject_unknown_mode()
