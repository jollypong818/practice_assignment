"""Day22 · 사용량·시간·비용 | PPT 39~46 | 02_intermediate
공통 제공 코드는 교시 독립 시작점입니다. 본 파일의 TODO 함수를 실행 경로에 연결합니다.
"""
from pathlib import Path
from decimal import Decimal as D
from coursekit.support import parse_args
from coursekit.io import read_json
from coursekit.response import get
from coursekit.metrics import estimate_cost as checkpoint_cost
from coursekit.labs import usage_lab

def usage_of(response):
    # TODO D22-05-I01: 사용량이 없으면 None, 있으면 입력·출력과부분 상세를 읽으세요.
    # 입력·완료 기준: 없는 값에 or0을 쓰지 않습니다. delta 개수를출력 Token 수로쓰지 않습니다.
    # BEGIN D22-05-I01
    u = get(response, "usage")
    values = {"input_tokens": None, "output_tokens": None, "cached_tokens": None,
              "reasoning_tokens": None, "total_tokens": None}
    # u가없으면None. 상세는 get(get(u,"..._details"),"..._tokens")
    raise NotImplementedError("D22-05-I01: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-05-I01

def calculate(usage, model, *, service_tier="default"):
    checked=checkpoint_cost(usage,model,service_tier=service_tier)
    if checked["estimated_usd"] is None:
        return checked
    from coursekit.io import ROOT
    price=read_json(ROOT/"config"/"prices.json")["models"][model]
    # TODO D22-05-I02: 캐시를제외한 입력·캐시입력·출력 비용을 Decimal로 계산하세요.
    # 입력·완료 기준: 가격은 USD/100만Token입니다. reasoning을출력에다시더하지 않습니다. unknown과0구분.
    # BEGIN D22-05-I02
    i = usage["input_tokens"]
    c = usage["cached_tokens"]
    o = usage["output_tokens"]
    uncached = None  # 입력 전체 - 캐시 입력
    amount = None    # 각 token수×해당단가의 합 / D(1000000)
    # 반환은 dict(checked, estimated_usd=str(amount))
    raise NotImplementedError("D22-05-I02: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-05-I02

def make_row(result, attempt, cost):
    # TODO D22-05-I03: 시도번호·실행출처·시간·사용량·비용을 같은 행에 남기세요.
    # 입력·완료 기준: 이 도구는 기존 run.json을 읽습니다. 측정을 위해 필요없는유료재호출은하지 않습니다.
    # BEGIN D22-05-I03
    row = {"run_id": result["run_id"], "source_mode": result["source_mode"]}
    # attempt에서 send_attempt·request_ms·first_text_ms·usage를읽고 cost와합칩니다.
    raise NotImplementedError("D22-05-I03: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-05-I03

def unknown_checks():
    # TODO D22-05-I04: usage 없음과 모델 단가 미등록에서 비용이None인지 검사하세요.
    # 입력·완료 기준: 부족한사용량은0원으로확정하지 않습니다.
    # BEGIN D22-05-I04
    # calculate(None, 알려진모델)와 calculate(usage, "unknown")을 검사합니다.
    raise NotImplementedError("D22-05-I04: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-05-I04

def summarize(attempts):
    # TODO D22-05-I05: 전체비용미확인을보존하는 합산함수를 연결하세요.
    # 입력·완료 기준: known_estimated_usd와total_estimated_usd의 차이를설명합니다.
    # BEGIN D22-05-I05
    from coursekit.metrics import sum_cost
    result = None  # sum_cost(attempts)
    raise NotImplementedError("D22-05-I05: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-05-I05

HERE = Path(__file__).resolve().parent

def main():
    args=parse_args(HERE)
    usage_lab(args,usage_reader=usage_of,calculator=calculate,row_builder=make_row,summarizer=summarize)
    unknown_checks()
