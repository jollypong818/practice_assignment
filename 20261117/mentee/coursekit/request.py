"""PPT 16~19장: 공급자 계약은 최소 형식, 로컬 계약은 Day21 그대로."""
from typing import Literal
from pydantic import BaseModel, ConfigDict
import json
from .io import read_json, ROOT, digest


class WireAnswer(BaseModel):
    model_config = ConfigDict(extra="forbid")
    status: Literal["answered", "insufficient_context"]
    answer: str
    source_ids: list[int]
    missing_information: str


OUTPUT_FORMAT = {"type": "json_schema", "name": "knowledge_answer", "strict": True,
                 "schema": WireAnswer.model_json_schema()}
VALIDATOR_VERSION = "day21-v1"


def build_request(model, instructions, question, selected, *, structured=True):
    if not isinstance(question, str) or not question.strip():
        raise ValueError("빈 질문")
    profiles = read_json(ROOT / "config" / "models.json")
    if model not in {p["model"] for p in profiles.values()}:
        raise ValueError("허용 모델이 아닙니다")
    if len(selected) > 3:
        raise ValueError("이번 수업의 문맥은 최대 3건입니다")
    ids = [row["id"] for row in selected]
    if any(type(i) is not int or i <= 0 for i in ids) or len(set(ids)) != len(ids):
        raise ValueError("지식 ID 오류")
    user_input = json.dumps({"question": question, "knowledge": selected}, ensure_ascii=False)
    if len(user_input.encode("utf-8")) > 20000 or len(instructions.encode("utf-8")) > 20000:
        raise ValueError("수업 입력 크기 상한 초과. Token 상한과는 별개입니다")
    request = {
        "model": model, "instructions": instructions,
        "input": [{"role": "user", "content": user_input}],
        "reasoning": {"effort": "none"}, "max_output_tokens": 1200,
        "store": False,
        # 단가표 적용 대상을 명시합니다. Priority/Flex/Batch 비용과 섞지 않습니다.
        "service_tier": "default",
    }
    if structured:
        request["text"] = {"format": OUTPUT_FORMAT}
    return request


def request_versions(request):
    return {"prompt_hash": digest(request["instructions"]),
            "context_hash": digest(request["input"]),
            "wire_schema_hash": digest(request.get("text")),
            "validator_version": VALIDATOR_VERSION}


def default_create(client, request, stream=False):
    # 교육용 안전 래퍼 안에서 실제 SDK 호출을 수행합니다. SDK 자동 재시도는 0입니다.
    return client.responses.create(**request, stream=stream)


def check_request_for_send(request):
    allowed = {"model", "instructions", "input", "reasoning", "max_output_tokens", "store", "text", "service_tier"}
    if set(request) - allowed or request.get("store") is not False:
        raise ValueError("허용하지 않는 요청 옵션 또는 store 설정")
    if type(request.get("max_output_tokens")) is not int or not 1 <= request["max_output_tokens"] <= 1200:
        raise ValueError("수업 출력 상한을 초과했습니다")
    if request.get("service_tier") != "default":
        raise ValueError("수업 단가표는 Standard default에 한정됩니다")
    if "text" in request and request["text"] != {"format": OUTPUT_FORMAT}:
        raise ValueError("수업 Wire Schema가 변경되었습니다. 의도한 수정인지 확인하세요")
