"""Day26 실습. 실행 위치와 관계없이 현재 역할 폴더의 지원 모듈을 사용합니다."""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))
from coursekit.io import save_json, show_success
from coursekit.data import example_hit, load_hits
from coursekit.reporting import execution_record

COMPONENT_INPUTS = {
    "Document": "page_content와 metadata를 담아 생성",
    "Retriever": "query·category·candidate_k가 있는 dict",
    "Prompt": "question·context가 있는 dict",
    "Chat Model": "ChatPromptValue 또는 메시지 목록",
}

def component_outputs() -> dict[str, str]:
    """강의에서 다룬 네 구성요소의 출력 자료형을 대응시킵니다."""
    # BEGIN D26-03-A01
    # TODO D26-03-A01: 네 구성요소의 반환값을 구분해 dict로 반환합니다.
    # 힌트: Prompt는 ChatPromptValue, Chat Model은 AIMessage입니다.
    # 함수의 docstring·README·expected/EXPECTED.md에서 입력과 완료 조건을 확인하세요.
    # 구현 후 아래 NotImplementedError를 제거하세요. 정답은 이 아래에 숨겨져 있지 않습니다.
    raise NotImplementedError("D26-03-A01 TODO 미완성")
    # END D26-03-A01

def access_kinds() -> dict[str, str]:
    """데이터를 읽는 경우와 invoke로 작업을 실행하는 경우를 구분합니다."""
    # BEGIN D26-03-A02
    # TODO D26-03-A02: Document는 data, 실행 구성요소는 invoke로 표시합니다.
    # 힌트: 값 읽기와 실행을 구분합니다. 여기서는 실제 API 호출을 하지 않습니다.
    # 함수의 docstring·README·expected/EXPECTED.md에서 입력과 완료 조건을 확인하세요.
    # 구현 후 아래 NotImplementedError를 제거하세요. 정답은 이 아래에 숨겨져 있지 않습니다.
    raise NotImplementedError("D26-03-A02 TODO 미완성")
    # END D26-03-A02

def repair_document_call() -> dict[str, str]:
    """Document.invoke로 답변을 얻는다는 설명을 올바른 읽기 표현으로 고칩니다."""
    # BEGIN D26-03-A03
    # TODO D26-03-A03: 잘못된 Document 호출과 올바른 본문 읽기·생성 역할을 기록합니다.
    # 힌트: doc.page_content로 값을 읽고 모델 생성은 Chat Model이 담당합니다.
    # 함수의 docstring·README·expected/EXPECTED.md에서 입력과 완료 조건을 확인하세요.
    # 구현 후 아래 NotImplementedError를 제거하세요. 정답은 이 아래에 숨겨져 있지 않습니다.
    raise NotImplementedError("D26-03-A03 TODO 미완성")
    # END D26-03-A03

def make_prompt_input(question: str, context: str) -> dict[str, str]:
    """Document 목록 대신 Prompt가 받을 두 문자열의 dict를 작성합니다."""
    # BEGIN D26-03-A04
    # TODO D26-03-A04: question과 context 문자열을 두 Key의 dict로 반환합니다.
    # 힌트: documents 목록을 그대로 전달하지 않습니다.
    # 함수의 docstring·README·expected/EXPECTED.md에서 입력과 완료 조건을 확인하세요.
    # 구현 후 아래 NotImplementedError를 제거하세요. 정답은 이 아래에 숨겨져 있지 않습니다.
    raise NotImplementedError("D26-03-A04 TODO 미완성")
    # END D26-03-A04

def main():
    outputs = component_outputs()
    access = access_kinds()
    report = {
        "execution": execution_record("concept_review"),
        "components": [{"component": name, "input": value,
                        "output": outputs[name], "access": access[name]}
                       for name, value in COMPONENT_INPUTS.items()],
        "observation": "입력·출력 대응표; Prompt·모델 invoke는 실행하지 않음",
    }
    report["document_correction"] = repair_document_call()
    report["prompt_input"] = make_prompt_input(
        "15분 늦으면 어떻게 기록되나요?", "[201] attendance_v2.md#sec-1\n" + example_hit()["body"])
    path = save_json(HERE, "object_contracts.json", report)
    show_success("03 심화", path)

if __name__ == "__main__":
    main()
