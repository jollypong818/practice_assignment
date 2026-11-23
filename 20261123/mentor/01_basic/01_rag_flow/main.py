"""Day26 실습. 실행 위치와 관계없이 현재 역할 폴더의 지원 모듈을 사용합니다."""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))
from coursekit.io import save_json, show_success
from coursekit.data import example_hit, load_hits
from coursekit.reporting import execution_record

# 입력·출력 설명은 제공됩니다. TODO에서는 올바른 처리 순서를 연결합니다.
STAGE_CARDS = {
    "Generator": {"input": "모델 입력", "output": "생성된 답변"},
    "Prompt": {"input": "규칙·질문·Context", "output": "모델이 읽을 메시지"},
    "Retriever": {"input": "질문·검색 조건", "output": "관련 청크 후보"},
    "Validator · Source 연결": {"input": "생성 결과·허용 ID", "output": "검증 결과·원문 위치"},
    "Context Builder": {"input": "후보 목록", "output": "선택한 근거·포함 ID"},
}

def stage_order() -> list[str]:
    """STAGE_CARDS의 이름 다섯 개를 처리 순서대로 반환합니다."""
    # BEGIN D26-01-B01
    # 검색 후보를 먼저 얻고 이번 답변에 넣을 근거를 고릅니다.
    # Prompt는 그 근거와 질문·규칙을 메시지로 만들고, Generator가 답을 생성합니다.
    # 마지막 확인은 반환값 검사와 원문 위치 연결입니다. 실제 함수 실행을 흉내 낸 것이 아닌 역할 정리표입니다.
    return [
        "Retriever", "Context Builder", "Prompt", "Generator",
        "Validator · Source 연결",
    ]
    # END D26-01-B01

def evidence_note(hit: dict) -> dict:
    """출석 문서와 사람이 읽은 판단을 함께 기록합니다. 모델 호출 결과가 아닙니다."""
    # BEGIN D26-01-B02
    # 숫자 15만 떼어 적으면 “까지”와 “초과”의 경계가 사라집니다. 본문 전체를 근거로 남깁니다.
    # 판단은 강의 문서를 읽어 정리한 교육용 기록이며 실제 LLM 생성 결과가 아닙니다.
    # 출처 ID·문서·버전·위치는 입력값을 그대로 보존합니다.
    return {
        "citation_id": hit["citation_id"],
        "doc_id": hit["doc_id"],
        "source_version": hit["source_version"],
        "source_locator": hit["source_locator"],
        "evidence": hit["body"],
        "question": "15분 늦으면 어떻게 기록되나요?",
        "judgment": "지각",
        "exception_to_check": "사전 승인을 받은 경우 운영실 확인",
    }
    # END D26-01-B02

def main():
    order = stage_order()
    report = {
        "execution": execution_record("concept_review"),
        "stages": [{"stage": name, **STAGE_CARDS[name]} for name in order],
        "case": evidence_note(example_hit()),
        "observation": "사람이 강의 원문을 읽고 작성한 역할·근거 확인표",
    }
    path = save_json(HERE, "rag_flow.json", report)
    show_success("01 Basic", path)

if __name__ == "__main__":
    main()
