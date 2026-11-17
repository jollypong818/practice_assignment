"""다음 교시를 독립 시작하기 위한 완성 체크포인트(PPT 47~53, 77~79).
06_output_validation에서는 이 코드가 아니라 자신의 TODO 함수를 실행합니다.
"""
import json
from typing import Annotated, Literal
from pydantic import BaseModel, ConfigDict, Field, ValidationError

INSUFFICIENT = "제공된 지식으로는 답할 수 없습니다."
SourceID = Annotated[int, Field(strict=True, gt=0)]


class KnowledgeAnswer(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    status: Literal["answered", "insufficient_context"]
    answer: str = Field(min_length=1, max_length=500)
    source_ids: list[SourceID] = Field(max_length=3)
    missing_information: str = Field(max_length=200)


def reject_constant(value):
    raise ValueError("비표준 JSON 상수")


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("중복 JSON 키")
        result[key] = value
    return result


def strict_json(raw):
    # 과도한 응답·중복 키·NaN을 거부하는 제공 보호 코드. 의미 검사와 다릅니다.
    if not isinstance(raw, str):
        raise ValueError("응답은 문자열이어야 합니다")
    if len(raw.encode("utf-8")) > 20000:
        raise ValueError("응답이 20,000 bytes를 초과했습니다")
    return json.loads(raw, parse_constant=reject_constant, object_pairs_hook=unique_object)


def parse_answer(raw):
    try:
        data = strict_json(raw)
    except (ValueError, RecursionError):
        return None, "json_error"
    try:
        return KnowledgeAnswer.model_validate(data), None
    except ValidationError:
        return None, "schema_error"


def check_rules(obj, provided_ids):
    ids = obj.source_ids
    if len(ids) != len(set(ids)):
        return "duplicate_source"
    if not set(ids) <= set(provided_ids):
        return "unknown_source"
    if obj.status == "answered":
        if not ids or obj.missing_information != "":
            return "status_rule"
    else:
        if ids or not obj.missing_information.strip():
            return "status_rule"
    if not obj.answer.strip():
        return "blank_answer"
    if obj.status == "insufficient_context" and obj.answer != INSUFFICIENT:
        return "status_rule"
    return None


def validate_answer(raw, provided_ids):
    obj, error = parse_answer(raw)
    if error is not None:
        return None, error
    error = check_rules(obj, provided_ids)
    return (None, error) if error else (obj, None)


def inspect_answer(raw, provided_ids, validator=validate_answer):
    """미평가는 None입니다. 참조를 통과해도 근거 평가를 자동으로 True로 만들지 않습니다."""
    obj, error = validator(raw, provided_ids)
    return {
        "json_ok": error != "json_error",
        "schema_ok": None if error == "json_error" else error != "schema_error",
        "reference_ok": None if error in {"json_error", "schema_error"} else error is None,
        "evidence_ok": None,
        "error": error,
        "answer_object": None if obj is None else obj.model_dump(),
        "auto_status": "passed_needs_human_review" if error is None else "failed",
    }
