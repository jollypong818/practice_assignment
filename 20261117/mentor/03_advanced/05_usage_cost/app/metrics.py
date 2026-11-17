"""Day22 · 사용량·시간·비용 | PPT 39~46 | 03_advanced
공통 제공 코드는 교시 독립 시작점입니다. 본 파일의 TODO 함수를 실행 경로에 연결합니다.
"""
from decimal import Decimal as D
from coursekit.io import read_json
from coursekit.response import get
from coursekit.metrics import estimate_cost as checkpoint_cost

def usage_of(response):
    # TODO D22-05-A01: 사용량이 없으면 None, 있으면 입력·출력과부분 상세를 읽으세요.
    # 입력·완료 기준: 없는 값에 or0을 쓰지 않습니다. delta 개수를출력 Token 수로쓰지 않습니다.
    # BEGIN D22-05-A01
    # 해설: 없는 값에 or0을 쓰지 않습니다. delta 개수를출력 Token 수로쓰지 않습니다.
    u=get(response,"usage")
    if u is None:
        return None
    return {"input_tokens":get(u,"input_tokens"),"output_tokens":get(u,"output_tokens"),
            "cached_tokens":get(get(u,"input_tokens_details"),"cached_tokens"),
            "reasoning_tokens":get(get(u,"output_tokens_details"),"reasoning_tokens"),
            "total_tokens":get(u,"total_tokens")}
    # END D22-05-A01

def calculate(usage, model, *, service_tier="default"):
    checked=checkpoint_cost(usage,model,service_tier=service_tier)
    if checked["estimated_usd"] is None:
        return checked
    from coursekit.io import ROOT
    price=read_json(ROOT/"config"/"prices.json")["models"][model]
    # TODO D22-05-A02: 캐시를제외한 입력·캐시입력·출력 비용을 Decimal로 계산하세요.
    # 입력·완료 기준: 가격은 USD/100만Token입니다. reasoning을출력에다시더하지 않습니다. unknown과0구분.
    # BEGIN D22-05-A02
    # 해설: 가격은 USD/100만Token입니다. reasoning을출력에다시더하지 않습니다. unknown과0구분.
    i,c,o=(usage[k] for k in ("input_tokens","cached_tokens","output_tokens"))
    amount=((i-c)*D(price["input_per_million"])+c*D(price["cached_input_per_million"])
            +o*D(price["output_per_million"]))/D(1000000)
    return dict(checked,estimated_usd=str(amount))
    # END D22-05-A02

def make_row(result, attempt, cost):
    # TODO D22-05-A03: 시도번호·실행출처·시간·사용량·비용을 같은 행에 남기세요.
    # 입력·완료 기준: 이 도구는 기존 run.json을 읽습니다. 측정을 위해 필요없는유료재호출은하지 않습니다.
    # BEGIN D22-05-A03
    # 해설: 이 도구는 기존 run.json을 읽습니다. 측정을 위해 필요없는유료재호출은하지 않습니다.
    return {"run_id":result["run_id"],"source_mode":result["source_mode"],
            "send_attempt":attempt["send_attempt"],"request_ms":attempt["request_ms"],
            "first_text_ms":attempt.get("first_text_ms"),"usage":attempt.get("usage"),**cost}
    # END D22-05-A03

def unknown_checks():
    # TODO D22-05-A04: usage 없음과 모델 단가 미등록에서 비용이None인지 검사하세요.
    # 입력·완료 기준: 부족한사용량은0원으로확정하지 않습니다.
    # BEGIN D22-05-A04
    # 해설: 부족한사용량은0원으로확정하지 않습니다.
    from coursekit.config import load_settings
    model=load_settings("simulated").models["fast"]
    assert calculate(None,model)["estimated_usd"] is None
    assert calculate({"input_tokens":1,"cached_tokens":0,"output_tokens":1},"unknown")["estimated_usd"] is None
    return True
    # END D22-05-A04

def summarize(attempts):
    # TODO D22-05-A05: 전체비용미확인을보존하는 합산함수를 연결하세요.
    # 입력·완료 기준: known_estimated_usd와total_estimated_usd의 차이를설명합니다.
    # BEGIN D22-05-A05
    # 해설: known_estimated_usd와total_estimated_usd의 차이를설명합니다.
    from coursekit.metrics import sum_cost
    return sum_cost(attempts)
    # END D22-05-A05

def check_unknown_total():
    # TODO D22-05-A06: 첫 실패비용이unknown이면 마지막성공만으로총비용을확정하지마세요.
    # 입력·완료 기준: 원래캐시생성비용을캐시hit마다새로합산하지않습니다.
    # BEGIN D22-05-A06
    # 해설: 원래캐시생성비용을캐시hit마다새로합산하지않습니다.
    report=summarize([{"source_mode":"api_live","estimated_usd":None},
                      {"source_mode":"api_live","estimated_usd":"0.00138"}])
    assert report["known_estimated_usd"]=="0.00138"
    assert report["total_estimated_usd"] is None
    assert report["unknown_cost_attempts"]==1
    return True
    # END D22-05-A06
