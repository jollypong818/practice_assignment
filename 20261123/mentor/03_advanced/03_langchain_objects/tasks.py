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
    # Document는 데이터를 담는 객체이고 Retriever는 여러 Document를 반환하는 역할입니다.
    # Prompt는 질문·Context를 메시지로 구성할 뿐 답변을 생성하지 않습니다.
    # Chat Model을 실행해야 모델 응답을 담은 AIMessage를 얻습니다.
    return {
        "Document": "본문·출처를 보관하는 데이터 객체",
        "Retriever": "list[Document]",
        "Prompt": "ChatPromptValue",
        "Chat Model": "AIMessage",
    }
    # END D26-03-A01

def access_kinds() -> dict[str, str]:
    """데이터를 읽는 경우와 invoke로 작업을 실행하는 경우를 구분합니다."""
    # BEGIN D26-03-A02
    # doc.page_content는 보관된 값을 읽습니다. Document 자체는 답변 생성기가 아닙니다.
    # 같은 invoke라도 Retriever는 검색, Prompt는 메시지 구성, Chat Model은 답변 요청을 합니다.
    # 이 실습은 대응표만 작성하므로 실제 invoke를 호출하지 않습니다.
    return {
        "Document": "data",
        "Retriever": "invoke",
        "Prompt": "invoke",
        "Chat Model": "invoke",
    }
    # END D26-03-A02

def repair_document_call() -> dict[str, str]:
    """Document.invoke로 답변을 얻는다는 설명을 올바른 읽기 표현으로 고칩니다."""
    # BEGIN D26-03-A03
    # Document는 데이터 보관 역할입니다. 메서드 이름을 임의로 붙여 모델로 바뀌지 않습니다.
    # 본문 읽기와 답변 생성은 서로 다른 구성요소의 작업으로 설명합니다.
    return {
        "incorrect": "doc.invoke(question)",
        "correct_read": "doc.page_content",
        "data_role": "본문과 Metadata를 보관",
        "generation_role": "Chat Model의 invoke",
    }
    # END D26-03-A03

def make_prompt_input(question: str, context: str) -> dict[str, str]:
    """Document 목록 대신 Prompt가 받을 두 문자열의 dict를 작성합니다."""
    # BEGIN D26-03-A04
    # 문서를 Context 문자열로 만드는 과정은 별도로 수행해야 합니다. 이 함수에는 준비된 문자열을 받습니다.
    # question·context Key는 Prompt의 자리표시자 이름과 같아야 합니다.
    # 여기서는 Python dict만 만들며 ChatPromptTemplate 생성과 invoke는 실습 05에서 합니다.
    return {"question": question, "context": context}
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
