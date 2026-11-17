"""Day22 · 명시적 모델 선택 | PPT 53~59 | 01_basic
공통 제공 코드는 교시 독립 시작점입니다. 본 파일의 TODO 함수를 실행 경로에 연결합니다.
"""
from pathlib import Path
import sys
HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))

from coursekit.support import parse_args, guarded
from coursekit.config import choose_model as checkpoint_choose
from coursekit.labs import routing_lab

def route(mode, models):
    # TODO D22-07-B01: fast·quality만허용하고실제모델과선택이유를반환하세요.
    # 입력·완료 기준: 알수없는모드를fast로조용히바꾸지않습니다. quality권한없으면not_run입니다.
    # BEGIN D22-07-B01
    allowed = {"fast", "quality"}
    model = None   # models.get(mode), 미설정은오류
    reason = ""    # explicit_mode:<mode>
    # checkpoint_choose(mode, models)를이용할수있습니다.
    raise NotImplementedError("D22-07-B01: TODO를 완성하고 이 raise를 제거하세요")
    return (model, reason)  # 위 TODO와 raise 제거를 마친 뒤 반환합니다.
    # END D22-07-B01

def record_view(result):
    # TODO D22-07-B02: 어떤모델이든동일한결과필드로비교하세요.
    # 입력·완료 기준: 고가모델이항상더좋다는결론을미리넣지않습니다.
    # BEGIN D22-07-B02
    fields = ["case_id", "source_mode", "model", "route_reason", "run_status",
              "answer_object", "evidence_ok", "usage", "request_ms", "estimated_usd"]
    row = {}  # {key: result.get(key) for key in fields}
    raise NotImplementedError("D22-07-B02: TODO를 완성하고 이 raise를 제거하세요")
    return row  # 위 TODO와 raise 제거를 마친 뒤 반환합니다.
    # END D22-07-B02

def comparison_modes():
    # TODO D22-07-B03: 명시적비교에서만fast·quality를한번씩선택하세요.
    # 입력·완료 기준: 기본run은한모델만호출합니다. compare는계정권한·예산확인후선택합니다.
    # BEGIN D22-07-B03
    modes = []  # fast와quality각한번, while fallback금지
    raise NotImplementedError("D22-07-B03: TODO를 완성하고 이 raise를 제거하세요")
    return modes  # 위 TODO와 raise 제거를 마친 뒤 반환합니다.
    # END D22-07-B03

def main():
    args=parse_args(HERE)
    routing_lab(args,router=route,record_view=record_view,compare_modes=comparison_modes)

if __name__=="__main__":
    guarded(main)
