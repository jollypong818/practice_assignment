"""고정 교육 사례. Embedding 검색이나 LLM 추론을 수행하는 구현이 아닙니다.

실제 경로와 같은 자료형을 반환하여 전달·오류 처리만 확인합니다.
정답 성능/검색 성능/응답 시간 측정 자료로 쓰지 않습니다.
"""
import json
import re
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableLambda
from coursekit.data import load_hits
from coursekit.checkpoints import WireAnswer, NO_ANSWER, hits_to_documents

def _inputs(value):
    if isinstance(value, dict):
        return value["question"], value["context"]
    # Prompt | fixture_generation()도 같은 전달 경로를 따라갈 수 있게 합니다.
    messages = value.to_messages()
    human = next(m.content for m in reversed(messages) if m.type == "human")
    if not isinstance(human, str) or not human.startswith("질문:\n") or "\n\n자료:\n" not in human:
        raise ValueError("교육용 Prompt 형식이 다릅니다. 질문/자료 경계를 확인하세요.")
    return human[len("질문:\n"):].split("\n\n자료:\n", 1)

def _example_answer(question, context):
    # 고정된 강의 질문을 위한 간단한 선택 규칙입니다. 일반 질의를 이해하지 않습니다.
    blocks = re.split(r"(?m)(?=^\[\d+\] )", context)
    found = []
    for block in blocks:
        match = re.match(r"\[(\d+)\] ([^\n]+)\n(.*)", block, re.S)
        if match:
            found.append((int(match.group(1)), match.group(2), match.group(3)))
    answer, cid = None, None
    for source_id, locator, body in found:
        if ("늦" in question or "입실" in question or "출석" in question) and "15분까지" in body:
            if "승인" in question:
                answer = "사전 승인을 받은 경우에는 운영실에 확인합니다."
            elif "20분" in question:
                answer = "일반 기준으로 15분을 초과하므로 결석입니다. 사전 승인을 받은 경우에는 운영실에 확인합니다."
            else:
                answer = "수업 시작 후 15분까지는 지각으로 기록합니다. 사전 승인을 받은 경우에는 운영실에 확인합니다."
            cid = source_id
            break
        if "과제" in question and ("보관" in question or "어디" in question) and "개인 폴더" in body:
            answer, cid = "과제 파일은 개인 폴더에 보관합니다.", source_id
            break
        if "회의실" in question and "예약 승인" in body:
            answer, cid = "회의실은 예약 승인 후 이용합니다.", source_id
            break
    if answer is None:
        return {"status": "insufficient_context", "answer": NO_ANSWER, "source_ids": [],
                "missing_information": "질문에 답하는 구체적인 정보가 제공된 자료에 없습니다."}
    return {"status": "answered", "answer": answer, "source_ids": [cid], "missing_information": ""}

def fixture_bundle(data=None, status="completed"):
    if data is None:
        data = {"status": "answered", "answer": "15분까지는 지각입니다. 사전 승인을 받은 경우 운영실에 확인합니다.",
                "source_ids": [201], "missing_information": ""}
    raw = AIMessage(content=[{"type": "text", "text": json.dumps(data, ensure_ascii=False)}],
                    response_metadata={"status": status, "source_mode": "fixed_fixture"})
    try:
        parsed, error = WireAnswer.model_validate(data), None
    except ValueError as exc:
        parsed, error = None, exc
    return {"raw": raw, "parsed": parsed, "parsing_error": error}

def fixture_generation(scenario="normal"):
    if scenario not in {"normal", "timeout", "incomplete", "refusal", "unknown_source", "parsing_error"}:
        raise ValueError("알 수 없는 교육 시나리오")
    def run(value):
        if scenario == "timeout":
            raise TimeoutError("고정 교육 예시: 모델 호출 시간 초과")
        question, context = _inputs(value)
        data = _example_answer(question, context)
        if scenario == "unknown_source":
            data = {"status": "answered", "answer": "허용하지 않은 ID의 고정 예시", "source_ids": [999999], "missing_information": ""}
        bundle = fixture_bundle(data, status="incomplete" if scenario == "incomplete" else "completed")
        if scenario == "refusal":
            bundle["raw"] = AIMessage(content=[{"type": "refusal", "refusal": "고정 거절 예시"}], response_metadata={"status": "completed"})
            bundle["parsed"] = None
            bundle["parsing_error"] = ValueError("고정 provider refusal 예시")
        if scenario == "parsing_error":
            bundle["parsed"], bundle["parsing_error"] = None, ValueError("고정 parsing 실패 예시")
        return bundle
    return RunnableLambda(run)

def fixture_chat_model():
    def run(value):
        question, context = _inputs(value)
        return fixture_bundle(_example_answer(question, context))["raw"]
    return RunnableLambda(run)

def fixture_retriever():
    def retrieve(req):
        k = req.get("candidate_k", 3)
        if type(k) is not int or not 1 <= k <= 20:
            raise ValueError("candidate_k must be 1..20")
        # corpus 순서를 그대로 사용합니다. 질의 유사도로 순위를 계산하지 않습니다.
        hits = [h for h in load_hits() if h["category"] == req["category"]][:k]
        return hits_to_documents(hits)
    return RunnableLambda(retrieve)
