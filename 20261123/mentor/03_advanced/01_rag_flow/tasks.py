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
    # BEGIN D26-01-A01
    # 검색 후보를 먼저 얻고 이번 답변에 넣을 근거를 고릅니다.
    # Prompt는 그 근거와 질문·규칙을 메시지로 만들고, Generator가 답을 생성합니다.
    # 마지막 확인은 반환값 검사와 원문 위치 연결입니다. 실제 함수 실행을 흉내 낸 것이 아닌 역할 정리표입니다.
    return [
        "Retriever", "Context Builder", "Prompt", "Generator",
        "Validator · Source 연결",
    ]
    # END D26-01-A01

def evidence_fields(hit: dict) -> dict:
    """출처와 근거 본문을 비교 기록에 넣을 공통 필드로 반환합니다."""
    # BEGIN D26-01-A02
    # 같은 출석 문서를 비교하므로 근거와 출처는 같은 값으로 보존합니다.
    # 질문의 숫자가 바뀌었다고 원문의 15분 기준을 바꾸면 안 됩니다.
    return {
        "citation_id": hit["citation_id"], "doc_id": hit["doc_id"],
        "source_version": hit["source_version"],
        "source_locator": hit["source_locator"], "evidence": hit["body"],
    }
    # END D26-01-A02

def attendance_judgment(minutes: int, prior_approval: bool = False) -> str:
    """강의의 가상 사례를 조건문으로 대조합니다. 실제 기관의 출석 판정기가 아닙니다."""
    # BEGIN D26-01-A03
    # 15분은 “15분까지”에 포함되며 20분은 그 범위를 초과합니다.
    # 사전 승인은 출석으로 자동 확정하는 조건이 아닙니다. 원문대로 운영실 확인으로 남깁니다.
    # 조건문 결과는 원문을 이해하기 위한 교육용 대조이며 LLM 출력이 아닙니다.
    if type(minutes) is not int or minutes < 0:
        raise ValueError("minutes는 0 이상의 정수여야 합니다.")
    if type(prior_approval) is not bool:
        raise TypeError("prior_approval은 bool이어야 합니다.")
    if prior_approval:
        return "운영실 확인"
    if minutes == 0:
        return "정시 입실: 이 실습의 지각 비교 대상 아님"
    return "지각" if minutes <= 15 else "결석"
    # END D26-01-A03

def comparison(hit: dict) -> list[dict]:
    """15분·20분·사전 승인 20분의 세 사례를 같은 원문과 연결합니다."""
    # BEGIN D26-01-A04
    # 세 사례는 질문 조건만 바뀌고 원문·버전·출처는 같습니다.
    # 각 행을 원문과 함께 읽으면 숫자의 경계와 예외를 따로 확인할 수 있습니다.
    cases = [(15, False), (20, False), (20, True)]
    rows = []
    for minutes, approved in cases:
        rows.append({
            "minutes": minutes, "prior_approval": approved,
            "judgment": attendance_judgment(minutes, approved),
            **evidence_fields(hit),
        })
    return rows
    # END D26-01-A04

def main():
    report = {
        "execution": execution_record("concept_review"),
        "stages": [{"stage": name, **STAGE_CARDS[name]} for name in stage_order()],
        "cases": comparison(example_hit()),
        "observation": "원문의 조건을 Python 조건문으로 대조한 교육용 기록; LLM 호출 아님",
    }
    path = save_json(HERE, "rag_flow.json", report)
    show_success("01 Advanced", path)

if __name__ == "__main__":
    main()
