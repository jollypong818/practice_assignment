from __future__ import annotations
import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "knowledge_search_v2.json"
VALID_CATEGORIES = {"course", "development", "support"}
E5_MODEL_ID = "intfloat/multilingual-e5-small"
DIMS = 384
TABLE_NAME = "day23_search_docs"
INSUFFICIENT = "제공된 지식으로는 답할 수 없습니다."

def load_knowledge():
    # 강의 HTML의 원문 스냅샷을 변경하지 않고 읽습니다.
    rows = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return [dict(row) for row in rows]

def passage_text(row):
    # 이번 E5 검색 계약: 제목 + 공백 + 본문에 passage 접두어.
    return "passage: " + row["title"] + " " + row["content"]

def query_text(question):
    return "query: " + question

def validate_snapshot(rows):
    """공통 읽기 경계 검증. 요구되는 TODO의 세부 응용은 실습 코드에서 구현합니다."""
    ids = []
    for row in rows:
        if type(row.get("id")) is not int or row["id"] <= 0:
            raise ValueError("id는 양의 정수여야 합니다")
        ids.append(row["id"])
        for k in ("title", "content", "category", "source_version"):
            if not isinstance(row.get(k), str) or not row[k].strip():
                raise ValueError("필수 문자열 누락: " + k)
        if row["category"] not in VALID_CATEGORIES:
            raise ValueError("잘못된 category")
    if len(ids) != len(set(ids)):
        raise ValueError("지식 ID 중복")
    return True
