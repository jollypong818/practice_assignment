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
    # BEGIN D26-01-I01
    # 검색 후보를 먼저 얻고 이번 답변에 넣을 근거를 고릅니다.
    # Prompt는 그 근거와 질문·규칙을 메시지로 만들고, Generator가 답을 생성합니다.
    # 마지막 확인은 반환값 검사와 원문 위치 연결입니다. 실제 함수 실행을 흉내 낸 것이 아닌 역할 정리표입니다.
    return [
        "Retriever", "Context Builder", "Prompt", "Generator",
        "Validator · Source 연결",
    ]
    # END D26-01-I01

def find_hit(hits: list[dict], doc_id: str) -> dict:
    """주어진 예시 목록에서 문서 ID가 같은 Hit 한 건을 선택합니다."""
    # BEGIN D26-01-I02
    # 이미 준비된 예시에서 문서 ID로 고르는 코드입니다. Embedding 검색이나 검색 성능을 구현한 것이 아닙니다.
    # 문서가 없을 때 다른 문서를 대신 반환하면 근거가 바뀌므로 명확히 실패시킵니다.
    for hit in hits:
        if hit["doc_id"] == doc_id:
            return hit
    raise LookupError(f"예시 목록에 문서가 없습니다: {doc_id}")
    # END D26-01-I02

def deadline_note(hit: dict) -> dict:
    """과제 문서의 존재와 정확한 마감 날짜의 존재를 구분해 기록합니다."""
    # BEGIN D26-01-I03
    # 관련 문서를 얻었다는 사실은 질문의 정답이 그 안에 있다는 뜻이 아닙니다.
    # 원문에 없는 날짜를 추정해 넣지 않습니다. 여기의 expected_status는 사람이 정리한 기대 판단입니다.
    return {
        "question": "내 과제의 정확한 마감 날짜는?",
        "citation_id": hit["citation_id"],
        "doc_id": hit["doc_id"],
        "source_version": hit["source_version"],
        "source_locator": hit["source_locator"],
        "evidence": hit["body"],
        "document_found": True,
        "exact_date_available": False,
        "expected_status": "insufficient_context",
        "reason": "문서는 담당자가 공지한 날짜를 따르라고만 안내하며 정확한 날짜는 제공하지 않습니다.",
    }
    # END D26-01-I03

def main():
    hit = find_hit(load_hits(), "DOC-ASSIGN")
    report = {
        "execution": execution_record("concept_review"),
        "stages": [{"stage": name, **STAGE_CARDS[name]} for name in stage_order()],
        "case": deadline_note(hit),
        "observation": "예시 문서 선택과 사람이 작성한 정보 부족 판단",
    }
    path = save_json(HERE, "rag_flow.json", report)
    show_success("01 Intermediate", path)

if __name__ == "__main__":
    main()
