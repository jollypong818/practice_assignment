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
    # BEGIN D26-02-B01
    # 모델에 보낼 본문 바로 위에 출처 ID와 원문 위치를 표시합니다.
    # f-string의 중괄호에는 변수 값이 들어가고, \n은 실제 줄바꿈입니다.
    # 이 함수는 표시 형식만 바꾸며 검색·생성·사실 검증을 수행하지 않습니다.
    citation_id = hit["citation_id"]
    locator = hit["source_locator"]
    body = hit["body"]
    return f"[{citation_id}] {locator}\n{body}"
    # END D26-02-B01

def make_context(hits: list[dict], max_items: int = 2) -> tuple[str, list[int]]:
    """앞에서 최대 max_items건을 골라 Context와 같은 선택의 ID 목록을 반환합니다."""
    # BEGIN D26-02-B02
    # 슬라이스는 실제 건수가 1건이면 1건만 고릅니다. 2건을 보장하는 명령이 아닙니다.
    # 같은 반복문에서 본문과 ID를 모아 둘의 출처가 어긋나지 않게 합니다.
    # 빈 목록에서는 join 결과가 빈 문자열이고 ID도 빈 목록입니다.
    selected_hits = hits[:max_items]
    blocks = []
    included_ids = []
    for hit in selected_hits:
        blocks.append(format_hit(hit))
        included_ids.append(hit["citation_id"])
    return "\n\n".join(blocks), included_ids
    # END D26-02-B02

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
    path = save_json(HERE, "hit_context.json", report)
    show_success("02 기본필수", path)

if __name__ == "__main__":
    main()
