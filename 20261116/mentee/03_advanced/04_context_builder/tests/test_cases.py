"""자신의 심화 구현을 검사합니다. 실제 모델 품질 테스트가 아닙니다."""
from pathlib import Path
import sys
import json
import pytest
HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE))
sys.path.insert(0,str(HERE.parents[1]))
from coursekit.io import DATA, read_json
from context_builder import select_context, calculate_budget


def test_order_and_budget():
    rows=read_json(DATA/"knowledge_v1.json")
    chosen,text=select_context(rows,[102,102,101])
    assert [x["id"] for x in chosen]==[102,101]
    assert json.loads(text)==chosen
    assert calculate_budget()["available_for_context"]==4936

@pytest.mark.parametrize("mode",["missing","duplicate"])
def test_invalid_snapshot(mode):
    rows=read_json(DATA/"knowledge_v1.json")
    with pytest.raises(ValueError):
        select_context(rows+[rows[0]] if mode=="duplicate" else rows,[999] if mode=="missing" else [101])
