"""Day26 실습. 실행 위치와 관계없이 현재 역할 폴더의 지원 모듈을 사용합니다."""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))
from coursekit.io import save_json, show_success
from coursekit.data import example_hit, load_hits
from coursekit.reporting import execution_record

def format_hit(hit: dict) -> str:
    """Hit 한 건의 ID·위치·본문을 한 문자열 블록으로 반환합니다."""
    # BEGIN D26-02-A01
    # TODO D26-02-A01: [ID] 원문위치, 줄바꿈, 본문 순서로 한 블록을 만듭니다.
    # 힌트: citation_id·source_locator·body를 읽어 f-string으로 연결합니다.
    # 함수의 docstring·README·expected/EXPECTED.md에서 입력과 완료 조건을 확인하세요.
    # 구현 후 아래 NotImplementedError를 제거하세요. 정답은 이 아래에 숨겨져 있지 않습니다.
    raise NotImplementedError("D26-02-A01 TODO 미완성")
    # END D26-02-A01

def select_hits(hits: list[dict], max_items: int = 2) -> list[dict]:
    """입력 순서를 유지해 앞의 최대 max_items건만 고릅니다."""
    # BEGIN D26-02-A02
    # TODO D26-02-A02: 입력 순서대로 앞의 최대 max_items건을 선택합니다.
    # 힌트: 목록 슬라이스를 사용합니다.
    # 함수의 docstring·README·expected/EXPECTED.md에서 입력과 완료 조건을 확인하세요.
    # 구현 후 아래 NotImplementedError를 제거하세요. 정답은 이 아래에 숨겨져 있지 않습니다.
    raise NotImplementedError("D26-02-A02 TODO 미완성")
    # END D26-02-A02

def make_context(hits: list[dict], max_items: int = 2) -> tuple[str, list[int]]:
    """선택한 목록에서 Context와 포함 ID를 동시에 만듭니다."""
    # BEGIN D26-02-A03
    # TODO D26-02-A03: 선택 결과를 문자열로 연결하고 같은 Hit의 citation_id 목록을 반환합니다.
    # 힌트: 본문과 ID 수집을 같은 for 반복문 안에 둡니다.
    # 함수의 docstring·README·expected/EXPECTED.md에서 입력과 완료 조건을 확인하세요.
    # 구현 후 아래 NotImplementedError를 제거하세요. 정답은 이 아래에 숨겨져 있지 않습니다.
    raise NotImplementedError("D26-02-A03 TODO 미완성")
    # END D26-02-A03

def compare_empty_and_one(hit: dict) -> dict:
    """빈 목록과 한 건의 출력 차이를 나란히 기록합니다."""
    # BEGIN D26-02-A04
    # TODO D26-02-A04: 빈 목록과 한 건을 각각 호출해 두 결과를 저장합니다.
    # 힌트: 빈 경우도 make_context를 실제 호출하여 확인하세요.
    # 함수의 docstring·README·expected/EXPECTED.md에서 입력과 완료 조건을 확인하세요.
    # 구현 후 아래 NotImplementedError를 제거하세요. 정답은 이 아래에 숨겨져 있지 않습니다.
    raise NotImplementedError("D26-02-A04 TODO 미완성")
    # END D26-02-A04

def main():
    hit = example_hit()
    context, included_ids = make_context([hit])
    report = {
        "execution": execution_record("local_python"),
        "context": context,
        "included_ids": included_ids,
        "input_source": "lecture_fixture",
        "character_count": len(context),
    }
    report["comparison"] = compare_empty_and_one(hit)
    path = save_json(HERE, "hit_context.json", report)
    show_success("02 심화", path)

if __name__ == "__main__":
    main()
