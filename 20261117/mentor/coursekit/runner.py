"""PPT 34~35·77의 제한 실행기. 수업 제공 코드이며 학습 함수는 hooks로 실제 연결합니다."""
from dataclasses import dataclass
from copy import deepcopy
from pathlib import Path
from time import perf_counter, sleep
from datetime import datetime, timezone
import random
import uuid

from .config import SetupError
from .budget import SendLedger, BudgetStopped
from .request import default_create, request_versions, check_request_for_send
from .response import StreamState, accept_event, completed_text, validate_received, get
from .metrics import read_usage, estimate_cost, sum_cost
from .errors import normalize_error, classify_error, parse_retry_after, retry_delay
from .fixtures import SimClient, VirtualClock
from .io import environment, digest


@dataclass(frozen=True)
class RetryPolicy:
    max_generations: int = 2
    max_sends_per_generation: int = 2
    max_sends_total: int = 4
    elapsed_budget_s: float = 60.0

    def __post_init__(self):
        if not (1 <= self.max_generations <= 2 and 1 <= self.max_sends_per_generation <= 2
                and 1 <= self.max_sends_total <= 4 and 0 < self.elapsed_budget_s <= 120):
            raise ValueError("교안의 작업별 예산(2×2, 총4회·시간)을 넘길 수 없습니다")


def make_client(settings, source, case_id):
    if source == "simulated":
        return SimClient(case_id)
    try:
        from openai import OpenAI
    except ImportError:
        raise SetupError("openai SDK가 없습니다. requirements.txt를 설치하세요") from None
    # OS의 다른 base_url 설정을 조용히 따라가지 않습니다. 키를 승인되지 않은 서버로 보내지 않습니다.
    return OpenAI(api_key=settings.api_key, base_url="https://api.openai.com/v1", timeout=settings.timeout_s, max_retries=0)


def not_run(case_id, reason, model=None):
    return {"run_id": str(uuid.uuid4()), "case_id": case_id, "source_mode":"not_run",
            "run_status":"not_run", "reason":reason, "model":model, "answer_object":None,
            "evidence_ok":None,"attempts":[],"new_api_send_count":0,"simulated_send_count":0,
            "usage":None,"estimated_usd":None,"request_ms":None,"first_text_ms":None,
            "e2e_ms":None,"environment":environment()}


def run_request(request, provided_ids, *, source, settings, case_id, stream=False,
                policy=None, client=None, hooks=None, clock=None, sleeper=None, ledger_path=None):
    """네트워크 I/O timeout은 엄밀한 전체 작업 deadline이 아닙니다.
    시도 전·대기 후·스트림 이벤트마다 협조적으로 전체 예산을 검사합니다.
    숨은 SDK 재시도 없이 전송 직전에 예산을 예약하고 모든 첫 실패를 보존합니다.
    """
    check_request_for_send(request)
    policy = policy or RetryPolicy()
    hooks = hooks or {}
    create = hooks.get("create", default_create)
    gate = hooks.get("gate", completed_text)
    on_event = hooks.get("event", accept_event)
    classify = hooks.get("classify", classify_error)
    delay = hooks.get("delay", retry_delay)
    usage_reader = hooks.get("usage", read_usage)
    cost_calculator = hooks.get("cost", estimate_cost)
    if source not in {"live", "simulated"}:
        raise ValueError("source 오류")
    virtual = VirtualClock() if source == "simulated" else None
    clock = clock or (virtual.now if virtual else perf_counter)
    sleeper = sleeper or (virtual.sleep if virtual else sleep)
    mode = "api_live" if source == "live" else "simulated"
    result = {"run_id": str(uuid.uuid4()), "case_id":case_id, "source_mode":mode,
              "run_status":"not_run", "model":request["model"], "request":deepcopy(request),
              "provided_ids":sorted(provided_ids), "versions":request_versions(request),
              "attempts":[],"answer_object":None,"raw":None,"evidence_ok":None,
              "environment":environment(), "new_api_send_count":0, "simulated_send_count":0,
              "measurement_origin":"client_observed" if source=="live" else "virtual_clock_fixture",
              "started_at":datetime.now(timezone.utc).isoformat()}
    original_request = deepcopy(request)
    outgoing = deepcopy(request)
    start = clock()
    owned = client is None
    try:
        if client is None:
            client = make_client(settings, source, case_id)
    except SetupError as exc:
        return not_run(case_id, str(exc), request["model"])
    ledger = SendLedger(ledger_path or Path.home()/".day22_llm_lab"/"send_ledger_20261117.json", settings.max_live_sends)
    sends = 0
    exhausted = False
    try:
        for generation in range(1, policy.max_generations + 1):
            transport_success = False
            report = None
            for transmission in range(1, policy.max_sends_per_generation + 1):
                if sends >= policy.max_sends_total:
                    result.update(run_status="attempt_limit", stop_reason="total_send_limit")
                    exhausted = True
                    break
                if clock() - start >= policy.elapsed_budget_s:
                    result.update(run_status="deferred", stop_reason="elapsed_budget")
                    exhausted = True
                    break
                if source == "live":
                    try:
                        ledger.reserve(result["run_id"], sends + 1)
                    except BudgetStopped as exc:
                        result.update(run_status="budget_exhausted", reason=str(exc))
                        exhausted = True
                        break
                sends += 1
                sent_at = clock()
                state = StreamState()
                response = None
                error = None
                attempt = {"source_mode":mode,"generation_no":generation,"send_attempt":sends,
                           "transport_attempt":transmission,"api_status":None,"usage":None,
                           "response_id":None,"request_id":None,"request_ms":None,
                           "first_text_ms":None,"raw":None,"partial_text":None,
                           "estimated_usd":None,"cost_status":"unknown","wait_s":None,
                           "error":None,"validation_error":None,
                           "request_hash":digest(outgoing), "is_format_repair":generation > 1}
                try:
                    if not stream:
                        response = create(client, outgoing, False)
                    else:
                        # context manager가 예외·중단에도 스트림 자원을 정리합니다.
                        print(f"[Streaming · {mode} · 미검증 중간 출력]", flush=True)
                        with create(client, outgoing, True) as events:
                            for event in events:
                                on_event(state, event, clock, sent_at)
                                delta = get(event, "delta")
                                if get(event, "type") == "response.output_text.delta" and isinstance(delta, str):
                                    print(delta, end="", flush=True)
                                if clock() - start >= policy.elapsed_budget_s:
                                    state.error = "stream_deadline"
                                    break
                        response = state.final
                        attempt["partial_text"] = "".join(state.parts)
                        attempt["first_text_ms"] = state.first_text_ms
                        if state.error or response is None:
                            attempt["error"] = state.error or "stream_interrupted"
                except Exception as exc:
                    # 정책 코드는 공급자 오류 분류만 저장합니다. traceback/Authorization은 저장하지 않습니다.
                    error = normalize_error(exc)
                    if stream and state.events_seen > 0:
                        attempt["partial_text"] = "".join(state.parts)
                        attempt["first_text_ms"] = state.first_text_ms
                        error.kind = "stream_interrupted"
                    classified = classify(error)
                    attempt.update(error=classified["kind"], http_status=error.status,
                                   request_id=error.request_id)
                if stream:
                    print("\n[수신 종료 · 최종 상태와 출력 계약을 확인합니다]", flush=True)
                attempt["request_ms"] = round((clock() - sent_at) * 1000, 3)
                if response is not None:
                    attempt.update(api_status=get(response,"status"), response_id=get(response,"id"),
                                   request_id=get(response,"_request_id"),
                                   actual_model=get(response,"model"),
                                   response_service_tier=get(response,"service_tier"))
                    usage = usage_reader(response)
                    attempt["usage"] = usage
                    tier = get(response,"service_tier") or request.get("service_tier")
                    model_for_price = get(response,"model") or request["model"]
                    # fixture 모델명은 실제 단가 매칭값이 아니므로 요청 후보의 계산 예시만 남깁니다.
                    cost = cost_calculator(usage, request["model"] if source=="simulated" else model_for_price, service_tier=tier)
                    if source == "simulated":
                        attempt.update(example_estimated_usd=cost["estimated_usd"],
                                       cost_status="fixture_not_billed",price_version=cost.get("price_version"))
                    else:
                        attempt.update(cost)
                    if attempt["error"] is None:
                        validate_start = clock()
                        report = validate_received(response, provided_ids, gate=gate, structured="text" in request)
                        attempt["validate_ms"] = round((clock()-validate_start)*1000,3)
                        attempt.update(raw=report["raw"],validation_error=report["validation_error"])
                result["attempts"].append(attempt)
                if error is not None:
                    result.update(run_status=attempt["error"], answer_object=None, validation_error=None)
                    if not classified["retryable"] or transmission == policy.max_sends_per_generation:
                        result["stop_reason"] = "non_retryable" if not classified["retryable"] else "transport_limit"
                        break
                    if sends >= policy.max_sends_total:
                        result["stop_reason"] = "total_send_limit"
                        break
                    retry_header = error.headers.get("retry-after")
                    hinted = parse_retry_after(retry_header)
                    attempt["retry_after_status"] = "missing" if retry_header is None else "valid" if hinted is not None else "invalid"
                    remaining = policy.elapsed_budget_s - (clock() - start)
                    wait = delay(transmission, hinted, remaining, 0.0 if source=="simulated" else random.uniform(0,0.25))
                    if wait is None:
                        result.update(run_status="deferred", stop_reason="retry_after_exceeds_budget")
                        break
                    attempt["wait_s"] = wait
                    sleeper(wait)
                    continue
                if attempt["error"] is not None:
                    result.update(run_status="stream_interrupted",stop_reason=attempt["error"],answer_object=None)
                    break
                if report is None:
                    result.update(run_status="response_error",answer_object=None)
                    break
                result.update(report)
                transport_success = True
                break
            if exhausted or not transport_success:
                break
            if result["run_status"] not in {"json_error", "schema_error"}:
                break
            if generation >= policy.max_generations:
                result["stop_reason"] = "format_limit"
                break
            # 실패 원문과 내부 오류 전체를 보내지 않고 안전한 오류 분류만 덧붙입니다.
            outgoing = deepcopy(original_request)
            outgoing["input"].append({"role":"user","content":
                "형식 수정 요청: " + result["run_status"] + ". 같은 근거만 사용하고 지정된 JSON Schema와 길이 규칙을 지키세요."})
        if sends == 0:
            result["source_mode"] = "not_run"
        result["new_api_send_count"] = sends if source=="live" else 0
        result["simulated_send_count"] = sends if source=="simulated" else 0
        attempts = result["attempts"]
        result["request_ms"] = round(sum(a["request_ms"] for a in attempts),3) if attempts else None
        result["first_text_ms"] = attempts[0]["first_text_ms"] if attempts else None
        result["e2e_ms"] = round((clock()-start)*1000,3)
        result["usage"] = attempts[-1]["usage"] if attempts else None
        result.update(sum_cost(attempts) if source=="live" and sends else {
            "known_estimated_usd":None,"unknown_cost_attempts":0,"total_estimated_usd":None})
        result["estimated_usd"] = result["total_estimated_usd"]
        return result
    finally:
        if owned:
            client.close()
