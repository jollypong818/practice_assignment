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
    # 해설: 없는 값에 or0을 쓰지 않습니다. delta 개수를출력 Token 수로쓰지 않습니다.
    u=get(response,"usage")
    if u is None:
        return None
    return {"input_tokens":get(u,"input_tokens"),"output_tokens":get(u,"output_tokens"),
            "cached_tokens":get(get(u,"input_tokens_details"),"cached_tokens"),
            "reasoning_tokens":get(get(u,"output_tokens_details"),"reasoning_tokens"),
            "total_tokens":get(u,"total_tokens")}
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
    # 해설: 가격은 USD/100만Token입니다. reasoning을출력에다시더하지 않습니다. unknown과0구분.
    i,c,o=(usage[k] for k in ("input_tokens","cached_tokens","output_tokens"))
    amount=((i-c)*D(price["input_per_million"])+c*D(price["cached_input_per_million"])
            +o*D(price["output_per_million"]))/D(1000000)
    return dict(checked,estimated_usd=str(amount))
    # END D22-05-B02

def make_row(result, attempt, cost):
    # TODO D22-05-B03: 시도번호·실행출처·시간·사용량·비용을 같은 행에 남기세요.
    # 입력·완료 기준: 이 도구는 기존 run.json을 읽습니다. 측정을 위해 필요없는유료재호출은하지 않습니다.
    # BEGIN D22-05-B03
    # 해설: 이 도구는 기존 run.json을 읽습니다. 측정을 위해 필요없는유료재호출은하지 않습니다.
    return {"run_id":result["run_id"],"source_mode":result["source_mode"],
            "send_attempt":attempt["send_attempt"],"request_ms":attempt["request_ms"],
            "first_text_ms":attempt.get("first_text_ms"),"usage":attempt.get("usage"),**cost}
    # END D22-05-B03

# 강사용 핵심 해설
# cached_tokens는 input_tokens의 일부이며 reasoning_tokens는 output_tokens의 일부입니다.
# 입력을 비캐시/캐시로 나누어 각각의 단가를 적용하고, 출력은 한 번만 더합니다.
# None은 관측하지 못했다는 뜻입니다. 실패 시 사용량을 0으로 채우면 실제보다 비용이 작아 보입니다.
# Decimal 계산은 적용한 단가표에 따른 추정이며 세금·환율·특별 과금까지 확정한 청구서가 아닙니다.

def main():
    args=parse_args(HERE)
    usage_lab(args,usage_reader=usage_of,calculator=calculate,row_builder=make_row)

if __name__=="__main__":
    guarded(main)
