"""공통 파일 경로와 기록용 유틸리티. 상대경로 대신 __file__ 기준을 사용합니다."""
from __future__ import annotations
from pathlib import Path
import json
import sys

ROLE_ROOT = Path(__file__).resolve().parents[1]
DATA = ROLE_ROOT / "data"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save_json(directory: Path, name: str, payload) -> Path:
    out = directory / "outputs" / name
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
    return out


def show_success(exercise: str, output: Path) -> None:
    print(f"[{exercise}] 완료: {output}")
    print("실행 결과의 원문·출처·한계를 expected/EXPECTED.md와 대조하세요.")


def require_implemented(fun, *args, **kwargs):
    """학습용 TODO를 제거하지 않고 남겼을 때 읽기 쉬운 오류를 표시합니다."""
    try:
        return fun(*args, **kwargs)
    except NotImplementedError as exc:
        print(f"TODO 미완성: {exc}", file=sys.stderr)
        raise
