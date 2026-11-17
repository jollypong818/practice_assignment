"""PPT 48~51·78. 한 프로세스의 교육용 승인 응답 캐시. 운영용 공유 캐시가 아닙니다."""
from copy import deepcopy
from .io import digest, read_json, write_json
from .request import VALIDATOR_VERSION
from .contracts import inspect_answer
import uuid


def cache_key(request, scope, validator_version=VALIDATOR_VERSION):
    basis = {"scope":scope,"model":request["model"],"request":request,
             "format":request.get("text",{}).get("format"),"validator_version":validator_version}
    return digest(basis)


def make_entry(result, review, *, ttl_s=600):
    if ttl_s <= 0 or ttl_s > 3600:
        raise ValueError("수업 TTL은 1~3600초입니다")
    if result.get("source_mode") not in {"api_live","simulated"} or result.get("run_status") != "validated":
        return None
    answer = result.get("answer_object") or {}
    if answer.get("status") != "answered":
        return None
    if (review.get("decision") != "approve" or review.get("run_hash") != digest(result)
        or review.get("run_id") != result["run_id"] or not review.get("note", "").strip()):
        return None
    return {"key":cache_key(result["request"], result["scope"]), "scope":result["scope"],
            "human_approved":True,"raw":result["raw"],"origin_run_id":result["run_id"],
            "origin_source_mode":result["source_mode"], "model":result["model"],
            "expires_at":review["reviewed_at_epoch"] + ttl_s,
            "validator_version":VALIDATOR_VERSION, "review":deepcopy(review)}


def read_cache(cache, key, now, provided_ids, *, expected_source, scope):
    entry = cache.get(key)
    if entry is None or now >= entry["expires_at"]:
        return None
    if not entry["human_approved"] or entry["scope"] != scope or entry["origin_source_mode"] != expected_source:
        return None
    if entry["validator_version"] != VALIDATOR_VERSION:
        return None
    report = inspect_answer(entry["raw"], provided_ids)
    if report["error"] or report["answer_object"]["status"] != "answered":
        return None
    return {"run_id":str(uuid.uuid4()),"source_mode":"app_cache","run_status":"validated",
            "answer_object":report["answer_object"],"raw":entry["raw"],"evidence_ok":True,
            "origin_run_id":entry["origin_run_id"],"origin_source_mode":entry["origin_source_mode"],
            "usage":{"input_tokens":0,"output_tokens":0,"cached_tokens":0,"reasoning_tokens":0,"total_tokens":0},
            "usage_origin":"no_new_api_send", "new_api_send_count":0,"simulated_send_count":0,
            "estimated_usd":"0","known_estimated_usd":"0","total_estimated_usd":"0",
            "unknown_cost_attempts":0,"attempts":[],"model":entry["model"],
            "request_ms":0.0,"first_text_ms":None,"e2e_ms":None}
