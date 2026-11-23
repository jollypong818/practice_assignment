"""실습 05 · Prompt 구성과 Chat Model 호출을 구분합니다."""
from pathlib import Path
import argparse
import sys

HERE = Path(__file__).resolve().parent
# 어느 폴더에서 실행해도 이 역할 폴더의 coursekit을 사용합니다.
sys.path.insert(0, str(HERE.parents[1]))

from coursekit.data import example_hit, load_hits
from coursekit.checkpoints import make_prompt
from coursekit.llm import create_chat_model
from coursekit.fixtures import fixture_chat_model, fixture_generation
from coursekit.reporting import execution_record, message_record
from coursekit.io import save_json, show_success


def make_inputs(question: str, context: str) -> dict:
    """입력: 질문·근거 문자열 / 출력: question, context 두 Key를 가진 dict."""
    # BEGIN D26-05-A01
    # question은 사용자가 묻는 값이고 context는 검색 후 선택한 원문입니다.
    # 두 값을 구분해 두면 질문을 바꿀 때 원문을 덮어쓰지 않습니다.
    # Key의 철자는 make_prompt()에서 사용하는 {question}, {context}와 맞춥니다.
    return {"question": question, "context": context}
    # END D26-05-A01


def invoke_pair(prompt, chat_model, inputs: dict):
    """dict → ChatPromptValue → AIMessage. 반환: (prompt_value, message)."""
    # BEGIN D26-05-A02
    # 이 호출은 변수 값을 채워 메시지를 만들며 LLM API를 호출하지 않습니다.
    # 입력에 context가 없으면 여기서 KeyError가 발생하여 다음 줄로 가지 않습니다.
    prompt_value = prompt.invoke(inputs)
    # 위에서 완성한 메시지를 모델에 전달하는 이 지점이 실제 API 호출 경계입니다.
    # --offline에서는 같은 자리에 고정 응답용 Runnable이 들어갑니다.
    message = chat_model.invoke(prompt_value)
    # 요청 메시지와 모델 응답을 따로 보관해야 입력·출력을 비교할 수 있습니다.
    return prompt_value, message
    # END D26-05-A02


def inspect_missing_context(prompt) -> dict:
    """의도적으로 빠진 입력을 검사합니다. 모델 API는 이 함수에 등장하지 않습니다."""
    # BEGIN D26-05-A03
    try:
        # Context가 빈 문자열인 경우와 Key 자체가 없는 경우는 다릅니다.
        # 여기서는 Key를 생략하여 Prompt 입력 검사의 실패 지점을 관찰합니다.
        prompt.invoke({"question": "15분 늦으면 어떻게 기록되나요?"})
    except KeyError:
        # 예상한 오류를 교육용 관찰 기록으로 남깁니다. 정상 답변이 아닙니다.
        return {"stage": "prompt_input", "exception_type": "KeyError",
                "model_invoked": False}
    # 입력 오류가 조용히 무시된다면 실습 계약이 바뀐 것이므로 확인해야 합니다.
    raise AssertionError("context가 없는 입력은 Prompt 단계에서 실패해야 합니다.")
    # END D26-05-A03


def inspect_timeout(failing_model, inputs: dict) -> dict:
    """제공된 고정 오류 사례만 관찰합니다. 실제 API 장애를 재현하지 않습니다."""
    # BEGIN D26-05-A04
    try:
        # 이 실습에서는 fixture_generation("timeout")이 전달됩니다.
        # 예외 발생을 확인하기 위한 호출이며 실제 LLM 요청이 아닙니다.
        failing_model.invoke(inputs)
    except TimeoutError:
        # 문서에 정보가 없다는 답변과 응답 자체를 받지 못한 상황을 구분합니다.
        return {"stage": "model_call", "exception_type": "TimeoutError",
                "source_mode": "fixed_timeout_example", "llm_executed": False,
                "answer_received": False}
    raise AssertionError("제공된 Timeout 예시는 TimeoutError를 발생시켜야 합니다.")
    # END D26-05-A04


def context_of(hit: dict) -> str:
    """앞 장에서 배운 출처 포함 블록 형식입니다. 이번 실습의 제공 코드입니다."""
    return f'[{hit["citation_id"]}] {hit["source_locator"]}\n{hit["body"]}'


def main():
    parser = argparse.ArgumentParser(description="Prompt → Chat Model 입력·출력 관찰")
    parser.add_argument("--offline", action="store_true", help="고정 응답 예시만 사용; 실제 모델 미실행")
    args = parser.parse_args()
    attendance = example_hit()
    prompt = make_prompt()
    cases = [("attendance_15", "15분 늦으면 어떻게 기록되나요?", attendance)]
    assignment = next(hit for hit in load_hits() if hit["doc_id"] == "DOC-ASSIGN")
    cases.append(("assignment_deadline", "내 과제의 정확한 마감 날짜는?", assignment))
    # 모델 생성·호출 전에 로컬 TODO와 입력을 먼저 확인합니다.
    prepared = [(case_id, make_inputs(question, context_of(hit)), hit)
                for case_id, question, hit in cases]
    observations = {}
    observations["missing_context"] = inspect_missing_context(prompt)
    observations["timeout_example"] = inspect_timeout(
        fixture_generation("timeout"), prepared[0][1])
    # 기본 경로는 실제 모델입니다. 환경 문제가 있어도 자동으로 예시로 전환하지 않습니다.
    chat_model = fixture_chat_model() if args.offline else create_chat_model()
    records = []
    for case_id, inputs, hit in prepared:
        prompt_value, message = invoke_pair(prompt, chat_model, inputs)
        records.append({
            "case_id": case_id,
            "question": inputs["question"],
            "context": inputs["context"],
            "prompt_value_type": type(prompt_value).__name__,
            "prompt_messages": [{"type": m.type, "content": m.content}
                                for m in prompt_value.to_messages()],
            "response": message_record(message),
            "evidence": {"citation_id": hit["citation_id"],
                         "doc_id": hit["doc_id"], "source_locator": hit["source_locator"],
                         "body": hit["body"]},
            "human_evidence_review": "pending",
        })
    result = {
        "exercise": "05_prompt_model",
        "execution": execution_record("offline_fixture" if args.offline else "live", llm=not args.offline),
        "real_model_calls": 0 if args.offline else len(records),
        "fixed_example_calls": len(records) if args.offline else 0,
        "observations": observations,
        "cases": records,
        "review_note": "문장·출처의 정답 여부는 자동 판정하지 않았습니다. reports/review.md에 원문 대조를 기록하세요.",
    }
    path = save_json(HERE, "prompt_model.json", result)
    show_success("05 Prompt·Chat Model 관찰 기록", path)
    print("실제 LLM 실행:", not args.offline, "| 원문 대조: 수강생 확인 필요")


if __name__ == "__main__":
    main()
