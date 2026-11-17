"""Day22 · 사용량·시간·비용 | PPT 39~46 | 01_basic
공통 제공 코드는 교시 독립 시작점입니다. 본 파일의 TODO 함수를 실행 경로에 연결합니다.
"""
from pathlib import Path
import sys
HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))

from decimal import Decimal as D
from coursekit.support import parse_args, guarded
from coursekit.io import read_json
from coursekit.response import get
from coursekit.metrics import estimate_cost as checkpoint_cost
from coursekit.labs import usage_lab

def usage_of(response):
    # TODO D22-05-B01: 사용량이 없으면 None, 있으면 입력·출력과부분 상세를 읽으세요.
    # 입력·완료 기준: 없는 값에 or0을 쓰지 않습니다. delta 개수를출력 Token 수로쓰지 않습니다.
    # BEGIN D22-05-B01
    u = get(response, "usage")
    values = {"input_tokens": None, "output_tokens": None, "cached_tokens": None,
              "reasoning_tokens": None, "total_tokens": None}
    # u가없으면None. 상세는 get(get(u,"..._details"),"..._tokens")
    raise NotImplementedError("D22-05-B01: TODO를 완성하고 이 raise를 제거하세요")
    return values  # 위 TODO와 raise 제거를 마친 뒤 반환합니다.
    # END D22-05-B01

def calculate(usage, model, *, service_tier="default"):
    checked=checkpoint_cost(usage,model,service_tier=service_tier)
    if checked["estimated_usd"] is None:
        return checked
    from coursekit.io import ROOT
    price=read_json(ROOT/"config"/"prices.json")["models"][model]
    # TODO D22-05-B02: 캐시를제외한 입력·캐시입력·출력 비용을 Decimal로 계산하세요.
    # 입력·완료 기준: 가격은 USD/100만Token입니다. reasoning을출력에다시더하지 않습니다. unknown과0구분.
    # BEGIN D22-05-B02
    i = usage["input_tokens"]
    c = usage["cached_tokens"]
    o = usage["output_tokens"]
    uncached = None  # 입력 전체 - 캐시 입력
    amount = None    # 각 token수×해당단가의 합 / D(1000000)
    # 반환은 dict(checked, estimated_usd=str(amount))
    raise NotImplementedError("D22-05-B02: TODO를 완성하고 이 raise를 제거하세요")
    return dict(checked, estimated_usd=str(amount))  # 위 TODO와 raise 제거를 마친 뒤 반환합니다.
    # END D22-05-B02

def make_row(result, attempt, cost):
    # TODO D22-05-B03: 시도번호·실행출처·시간·사용량·비용을 같은 행에 남기세요.
    # 입력·완료 기준: 이 도구는 기존 run.json을 읽습니다. 측정을 위해 필요없는유료재호출은하지 않습니다.
    # BEGIN D22-05-B03
    row = {"run_id": result["run_id"], "source_mode": result["source_mode"]}
    # attempt에서 send_attempt·request_ms·first_text_ms·usage를읽고 cost와합칩니다.
    raise NotImplementedError("D22-05-B03: TODO를 완성하고 이 raise를 제거하세요")
    return row  # 위 TODO와 raise 제거를 마친 뒤 반환합니다.
    # END D22-05-B03

def main():
    args=parse_args(HERE)
    usage_lab(args,usage_reader=usage_of,calculator=calculate,row_builder=make_row)

if __name__=="__main__":
    guarded(main)
