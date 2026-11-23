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
    # BEGIN D26-03-I01
    # Document는 데이터를 담는 객체이고 Retriever는 여러 Document를 반환하는 역할입니다.
    # Prompt는 질문·Context를 메시지로 구성할 뿐 답변을 생성하지 않습니다.
    # Chat Model을 실행해야 모델 응답을 담은 AIMessage를 얻습니다.
    return {
        "Document": "본문·출처를 보관하는 데이터 객체",
        "Retriever": "list[Document]",
        "Prompt": "ChatPromptValue",
        "Chat Model": "AIMessage",
    }
    # END D26-03-I01

def access_kinds() -> dict[str, str]:
    """데이터를 읽는 경우와 invoke로 작업을 실행하는 경우를 구분합니다."""
    # BEGIN D26-03-I02
    # doc.page_content는 보관된 값을 읽습니다. Document 자체는 답변 생성기가 아닙니다.
    # 같은 invoke라도 Retriever는 검색, Prompt는 메시지 구성, Chat Model은 답변 요청을 합니다.
    # 이 실습은 대응표만 작성하므로 실제 invoke를 호출하지 않습니다.
    return {
        "Document": "data",
        "Retriever": "invoke",
        "Prompt": "invoke",
        "Chat Model": "invoke",
    }
    # END D26-03-I02

def repair_swapped_returns(swapped: dict[str, str]) -> dict[str, str]:
    """입력 표를 복사하고 Prompt와 Chat Model의 잘못된 출력만 고칩니다."""
    # BEGIN D26-03-I03
    # 수정 전·후를 비교하려면 원래 표를 덮어쓰지 말고 새 dict를 만듭니다.
    # 반환값 두 개를 바로잡으면 메시지 작성과 생성 결과가 구분됩니다.
    fixed = dict(swapped)
    outputs = component_outputs()
    fixed["Prompt"] = outputs["Prompt"]
    fixed["Chat Model"] = outputs["Chat Model"]
    return fixed
    # END D26-03-I03

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
    before = {**outputs, "Prompt": "AIMessage", "Chat Model": "ChatPromptValue"}
    report["before"] = before
    report["after"] = repair_swapped_returns(before)
    path = save_json(HERE, "object_contracts.json", report)
    show_success("03 응용", path)

if __name__ == "__main__":
    main()
