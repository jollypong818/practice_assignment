"""PPT 32~38, 75~77. 안전한 분류만 기록하고 예외 메시지 전체는 저장하지 않습니다."""
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import math


class ProviderError(Exception):
    def __init__(self, status=None, code=None, error_type=None, headers=None, kind=None, request_id=None):
        super().__init__("공급자 호출 오류 — 안전한 분류를 확인하세요")
        self.status = status
        self.code = code
        self.error_type = error_type
        self.headers = headers or {}
        self.kind = kind
        self.request_id = request_id


def normalize_error(exc):
    if isinstance(exc, ProviderError):
        return exc
    name = type(exc).__name__
    body = getattr(exc, "body", None)
    body = body if isinstance(body, dict) else {}
    body = body.get("error", body)
    body = body if isinstance(body, dict) else {}
    response = getattr(exc, "response", None)
    headers = getattr(response, "headers", {}) or {}
    kind = ("timeout" if name == "APITimeoutError" else
            "connection" if name == "APIConnectionError" else "unknown")
    return ProviderError(getattr(exc, "status_code", None), body.get("code"), body.get("type"),
                         {"retry-after": headers.get("retry-after")}, kind,
                         getattr(exc, "request_id", None))


def classify_error(error):
    if error.kind in {"timeout", "connection", "stream_interrupted"}:
        return {"kind": error.kind, "retryable": False}
    if error.status == 401:
        return {"kind": "auth_error", "retryable": False}
    if error.status == 403:
        return {"kind": "permission_error", "retryable": False}
    if error.status == 404:
        return {"kind": "model_or_resource_error", "retryable": False}
    if error.status == 400:
        return {"kind": "request_error", "retryable": False}
    codes = {error.code, error.error_type}
    if error.status == 429:
        if codes & {"insufficient_quota", "billing_hard_limit_reached", "billing_not_active", "usage_limit_reached"}:
            return {"kind": "quota_error", "retryable": False}
        if codes & {"rate_limit_exceeded", "rate_limit_error", "requests", "tokens"}:
            return {"kind": "rate_limit", "retryable": True}
        return {"kind": "unknown_429", "retryable": False}
    if error.status in {500, 502, 503, 504}:
        return {"kind": "server_error", "retryable": True}
    return {"kind": "unknown_error", "retryable": False}


def parse_retry_after(value, now=None):
    if value is None:
        return None
    now = datetime.now(timezone.utc) if now is None else now
    try:
        seconds = float(value)
        if math.isfinite(seconds) and seconds >= 0:
            return seconds
        return None
    except (TypeError, ValueError):
        pass
    try:
        moment = parsedate_to_datetime(str(value))
        if moment.tzinfo is None:
            moment = moment.replace(tzinfo=timezone.utc)
        return max(0.0, (moment - now).total_seconds())
    except (TypeError, ValueError, OverflowError):
        return None


def retry_delay(attempt, retry_after_s, remaining_s, jitter=0.0):
    # PPT 75의 보수적인 정책: 서버 최소 대기와 지수 대기 중 큰 값.
    if attempt < 1 or not math.isfinite(remaining_s) or remaining_s <= 0:
        return None
    if retry_after_s is not None and (not math.isfinite(retry_after_s) or retry_after_s < 0):
        return None
    if not 0 <= jitter <= 0.5:
        raise ValueError("jitter 범위 오류")
    wait = max(retry_after_s or 0.0, min(8.0, 2 ** min(attempt - 1, 3))) + jitter
    return None if wait >= remaining_s else wait
