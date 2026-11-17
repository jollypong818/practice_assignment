"""PPT 39~46, 79. None은 미확인이고 0은 관측된 0입니다."""
from decimal import Decimal, InvalidOperation
from .response import get
from .io import read_json, ROOT


def read_usage(response):
    usage = get(response, "usage")
    if usage is None:
        return None
    return {
        "input_tokens": get(usage, "input_tokens"),
        "output_tokens": get(usage, "output_tokens"),
        "total_tokens": get(usage, "total_tokens"),
        "cached_tokens": get(get(usage, "input_tokens_details"), "cached_tokens"),
        "reasoning_tokens": get(get(usage, "output_tokens_details"), "reasoning_tokens"),
    }


def estimate_cost(usage, model, *, service_tier="default", pricebook=None):
    book = read_json(ROOT / "config" / "prices.json") if pricebook is None else pricebook
    price = book["models"].get(model)
    unknown = {"estimated_usd": None, "cost_status": "unknown", "price_version": book["version"],
               "price_checked_at": book["checked_at"], "currency": "USD", "service_tier": service_tier}
    if price is None or usage is None or service_tier != "default":
        return unknown
    values = [usage.get(name) for name in ("input_tokens", "cached_tokens", "output_tokens")]
    if any(type(v) is not int or v < 0 for v in values):
        return unknown
    i, c, o = values
    if c > i:
        return dict(unknown, cost_status="invalid_usage")
    r = usage.get("reasoning_tokens")
    if r is not None and (type(r) is not int or r < 0 or r > o):
        return dict(unknown, cost_status="invalid_usage")
    try:
        pi, pc, po = (Decimal(price[k]) for k in ("input_per_million", "cached_input_per_million", "output_per_million"))
        if any(not p.is_finite() or p < 0 for p in (pi, pc, po)):
            return unknown
        amount = ((i - c)*pi + c*pc + o*po) / Decimal(1000000)
    except (InvalidOperation, KeyError, TypeError):
        return unknown
    # reasoning은 o의 부분집합이므로 다시 더하지 않습니다.
    return dict(unknown, estimated_usd=str(amount), cost_status="estimated")


def sum_cost(attempts):
    """누락된 실패 시도도 분모에서 지우지 않습니다. 알려진 합계와 전체 추정을 구분합니다."""
    known = Decimal("0")
    missing = 0
    for item in attempts:
        if item.get("source_mode") != "api_live":
            continue
        value = item.get("estimated_usd")
        if value is None:
            missing += 1
        else:
            known += Decimal(value)
    return {"known_estimated_usd": str(known), "unknown_cost_attempts": missing,
            "total_estimated_usd": None if missing else str(known)}


def summarize_runs(runs):
    result = {}
    for mode in ("api_live", "simulated", "app_cache", "not_run"):
        subset = [r for r in runs if r["source_mode"] == mode]
        attempts = [a for r in subset for a in r.get("attempts", [])]
        result[mode] = {"runs": len(subset), "new_api_send_count": sum(r.get("new_api_send_count", 0) for r in subset),
                        "validated_runs": sum(r["run_status"] == "validated" for r in subset),
                        "human_unreviewed": sum(r.get("evidence_ok") is None for r in subset)}
        if mode == "api_live":
            result[mode].update(sum_cost(attempts))
    return result
