"""실행 위치가 달라도 같은 data/와 실습별 outputs/를 사용합니다."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

def load_json(relative):
    """data/ 기준 경로에서 UTF-8 JSON을 읽습니다."""
    return json.loads((DATA / relative).read_text(encoding="utf-8"))

def save_json(here, name, data):
    """현재 실습의 outputs/에만 저장합니다. 원문과 expected는 덮어쓰지 않습니다."""
    path = Path(here) / "outputs" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return path

def show_success(label, path):
    print(f"[{label}] 파일 저장: {path}")
    print("파일 생성과 실제 DB·LLM 실행은 다릅니다. 결과의 실행 모드를 확인하세요.")
