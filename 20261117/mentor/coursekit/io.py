"""UTF-8 파일·고정 입력·해시. 비밀을 자동 수집하지 않습니다."""
from pathlib import Path
import json
import hashlib
import platform
from importlib.metadata import version, PackageNotFoundError

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value):
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def write_json(path, value):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def environment():
    result = {"python": platform.python_version(), "platform": platform.system()}
    for name in ("openai", "pydantic", "python-dotenv", "httpx"):
        try:
            result[name] = version(name)
        except PackageNotFoundError:
            result[name] = "not_installed"
    return result


def selected_knowledge(case, rows=None):
    rows = read_json(DATA / "knowledge_v1.json") if rows is None else rows
    by_id = {item["id"]: item for item in rows}
    if len(by_id) != len(rows):
        raise ValueError("스냅샷 ID 중복")
    ids = case["selected_ids"]
    if any(type(i) is not int or i not in by_id for i in ids):
        raise ValueError("선택 ID 오류")
    return [dict(by_id[i]) for i in dict.fromkeys(ids)]


def load_case(case_id):
    cases = read_json(DATA / "cases.json")
    if case_id not in cases:
        raise ValueError("지원하지 않는 case_id")
    return cases[case_id]


def input_parts(case_id):
    case = load_case(case_id)
    selected = selected_knowledge(case)
    instructions = (DATA / "instructions_v1.txt").read_text(encoding="utf-8")
    return case, selected, instructions
