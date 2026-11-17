"""파일 위치·UTF-8·실행 환경을 위한 제공 코드입니다."""
from pathlib import Path
import csv
import hashlib
import json
import re
import sys

ROLE_ROOT = Path(__file__).resolve().parents[1]
DATA = ROLE_ROOT / "data"


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def write_text(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def sha_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def write_csv(path, rows, fieldnames):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    # Excel에서 한글을 확인하기 쉽도록 BOM을 사용합니다. Python에서는 utf-8-sig로 읽습니다.
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for row in rows:
            w.writerow({k: "" if v is None else v for k, v in row.items()})


def check_name(value):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", value):
        raise ValueError("실험 이름은 영문·숫자·밑줄·하이픈(1~64자)을 사용하세요.")
    return value


def save_version(path, value):
    """같은 이름의 버전은 내용이 동일할 때만 재사용합니다."""
    path = Path(path)
    if path.exists() and read_json(path) != value:
        raise ValueError("기존 버전의 내용을 바꾸지 마세요. 새 파일명/버전을 사용하세요.")
    write_json(path, value)


def run(main):
    try:
        main()
    except NotImplementedError as exc:
        print(f"[미완성 TODO] {exc}\n골격의 TODO를 채운 뒤 해당 raise NotImplementedError 줄을 지우세요.", file=sys.stderr)
        raise SystemExit(2)
    except (ValueError, FileNotFoundError, KeyError) as exc:
        print(f"[확인 필요] {exc}", file=sys.stderr)
        raise SystemExit(2)
