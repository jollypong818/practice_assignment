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
    # TODO D26-01-B01: 다섯 단계의 이름을 처리 순서대로 반환합니다.
    # 힌트: 검색 → 근거 선택 → 메시지 작성 → 생성 → 확인 순서입니다.
    # 함수의 docstring·README·expected/EXPECTED.md에서 입력과 완료 조건을 확인하세요.
    # 구현 후 아래 NotImplementedError를 제거하세요. 정답은 이 아래에 숨겨져 있지 않습니다.
    raise NotImplementedError("D26-01-B01 TODO 미완성")
    # END D26-01-B01

def evidence_note(hit: dict) -> dict:
    """출석 문서와 사람이 읽은 판단을 함께 기록합니다. 모델 호출 결과가 아닙니다."""
    # BEGIN D26-01-B02
    # TODO D26-01-B02: 입력 Hit의 출처·본문과 15분 질문의 판단·예외를 한 dict로 묶습니다.
    # 힌트: source_locator와 body를 그대로 읽고, 문서의 “까지”와 사전 승인 조건을 확인하세요.
    # 함수의 docstring·README·expected/EXPECTED.md에서 입력과 완료 조건을 확인하세요.
    # 구현 후 아래 NotImplementedError를 제거하세요. 정답은 이 아래에 숨겨져 있지 않습니다.
    raise NotImplementedError("D26-01-B02 TODO 미완성")
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
