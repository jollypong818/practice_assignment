"""공급자 완료 게이트와 스트리밍 상태. 중간 텍스트를 성공 답변으로 승격하지 않습니다."""
from dataclasses import dataclass, field
from .contracts import inspect_answer


def get(obj, key, default=None):
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def output_text(response):
    direct = get(response, "output_text")
    if isinstance(direct, str):
        return direct
    # 기록된 dict와 실제 SDK 객체를 같은 검사기에 전달할 수 있습니다.
    return "".join(get(part, "text", "") for item in (get(response, "output", []) or [])
                   if get(item, "type") == "message"
                   for part in (get(item, "content", []) or [])
                   if get(part, "type") == "output_text" and isinstance(get(part, "text"), str))


def completed_text(response):
    for item in get(response, "output", []) or []:
        if get(item, "type") == "message":
            for part in get(item, "content", []) or []:
                if get(part, "type") == "refusal":
                    return None, "refused"
    status = get(response, "status")
    if status != "completed":
        return None, status if status in {"incomplete", "failed", "cancelled", "queued", "in_progress"} else "response_error"
    raw = output_text(response)
    if not raw.strip():
        return None, "empty_output"
    return raw, None


@dataclass
class StreamState:
    parts: list = field(default_factory=list)
    first_text_ms: float | None = None
    final: object | None = None
    error: str | None = None
    events_seen: int = 0


def accept_event(state, event, clock, started):
    state.events_seen += 1
    kind = get(event, "type")
    if kind == "response.output_text.delta":
        delta = get(event, "delta", "")
        if not isinstance(delta, str):
            state.error = "stream_protocol_error"
            return
        if delta and state.first_text_ms is None:
            state.first_text_ms = (clock() - started) * 1000
        state.parts.append(delta)
    elif kind in {"response.completed", "response.failed", "response.incomplete"}:
        if state.final is not None:
            state.error = "duplicate_terminal_event"
        state.final = get(event, "response")
    elif kind == "error":
        state.error = "stream_error"
    # created·output_text.done은 전체 응답의 성공 판정에 사용하지 않습니다.


def validate_received(response, provided_ids, *, gate=completed_text, structured=True):
    raw, error = gate(response)
    if error:
        return {"run_status": error, "raw": output_text(response), "answer_object": None,
                "validation_error": error, "evidence_ok": None}
    if not structured:
        return {"run_status": "completed_text", "raw": raw, "answer_object": None,
                "validation_error": None, "evidence_ok": None}
    report = inspect_answer(raw, provided_ids)
    return {"run_status": "validated" if report["error"] is None else report["error"],
            "raw": raw, "answer_object": report["answer_object"],
            "validation_error": report["error"], "evidence_ok": None,
            "auto_status": report["auto_status"]}
