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
    # TODO D26-01-I01: 다섯 단계의 처리 순서를 반환합니다.
    # 힌트: STAGE_CARDS의 이름을 사용합니다.
    # 함수의 docstring·README·expected/EXPECTED.md에서 입력과 완료 조건을 확인하세요.
    # 구현 후 아래 NotImplementedError를 제거하세요. 정답은 이 아래에 숨겨져 있지 않습니다.
    raise NotImplementedError("D26-01-I01 TODO 미완성")
    # END D26-01-I01

def find_hit(hits: list[dict], doc_id: str) -> dict:
    """주어진 예시 목록에서 문서 ID가 같은 Hit 한 건을 선택합니다."""
    # BEGIN D26-01-I02
    # TODO D26-01-I02: 목록에서 요청한 doc_id의 Hit를 반환하고 없으면 LookupError를 발생시킵니다.
    # 힌트: 각 Hit의 doc_id를 순서대로 비교합니다.
    # 함수의 docstring·README·expected/EXPECTED.md에서 입력과 완료 조건을 확인하세요.
    # 구현 후 아래 NotImplementedError를 제거하세요. 정답은 이 아래에 숨겨져 있지 않습니다.
    raise NotImplementedError("D26-01-I02 TODO 미완성")
    # END D26-01-I02

def deadline_note(hit: dict) -> dict:
    """과제 문서의 존재와 정확한 마감 날짜의 존재를 구분해 기록합니다."""
    # BEGIN D26-01-I03
    # TODO D26-01-I03: 문서 발견 여부와 정확한 날짜의 유무를 나누어 기대 판단을 작성합니다.
    # 힌트: “담당자가 공지한 날짜”는 실제 날짜 값이 아닙니다.
    # 함수의 docstring·README·expected/EXPECTED.md에서 입력과 완료 조건을 확인하세요.
    # 구현 후 아래 NotImplementedError를 제거하세요. 정답은 이 아래에 숨겨져 있지 않습니다.
    raise NotImplementedError("D26-01-I03 TODO 미완성")
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
