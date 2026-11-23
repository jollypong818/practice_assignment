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
    # BEGIN D26-02-I01
    # 모델에 보낼 본문 바로 위에 출처 ID와 원문 위치를 표시합니다.
    # f-string의 중괄호에는 변수 값이 들어가고, \n은 실제 줄바꿈입니다.
    # 이 함수는 표시 형식만 바꾸며 검색·생성·사실 검증을 수행하지 않습니다.
    citation_id = hit["citation_id"]
    locator = hit["source_locator"]
    body = hit["body"]
    return f"[{citation_id}] {locator}\n{body}"
    # END D26-02-I01

def select_hits(hits: list[dict], max_items: int = 2) -> list[dict]:
    """입력 순서를 유지해 앞의 최대 max_items건만 고릅니다."""
    # BEGIN D26-02-I02
    # 이번 단계에서는 검색 결과의 순서를 바꾸지 않고 앞부분을 선택합니다.
    # 중복·길이 제한은 실습 06의 build_context에서 다루므로 여기서 추가하지 않습니다.
    return hits[:max_items]
    # END D26-02-I02

def make_context(hits: list[dict], max_items: int = 2) -> tuple[str, list[int]]:
    """선택한 목록에서 Context와 포함 ID를 동시에 만듭니다."""
    # BEGIN D26-02-I03
    # Context에 넣지 않은 후보의 ID를 허용 출처로 모으면 안 됩니다.
    # 두 출력 모두 select_hits가 반환한 동일 목록에서 만듭니다.
    # 본문을 바꾸거나 한 청크의 마지막 문장을 잘라내지 않습니다.
    selected = select_hits(hits, max_items)
    blocks = []
    included_ids = []
    for hit in selected:
        blocks.append(format_hit(hit))
        included_ids.append(hit["citation_id"])
    return "\n\n".join(blocks), included_ids
    # END D26-02-I03

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
    show_success("02 응용", path)

if __name__ == "__main__":
    main()
