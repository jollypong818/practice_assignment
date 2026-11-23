"""현재 폴더의 구현만 검사합니다. API·DB·다운로드는 실행하지 않습니다."""
import importlib.util
from pathlib import Path
import sys
from copy import deepcopy
import pytest

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE.parents[1]))
from coursekit.data import example_hit, load_hits

MODULE_PATH = HERE / "tasks.py"
SPEC = importlib.util.spec_from_file_location("d26_mentor_1_A", MODULE_PATH)
m = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = m
SPEC.loader.exec_module(m)

def test_stage_sequence_connects_inputs_and_outputs():
    assert m.stage_order() == [
        "Retriever", "Context Builder", "Prompt", "Generator", "Validator · Source 연결"]

def test_boundary_and_approval_are_separate_conditions():
    assert m.attendance_judgment(15) == "지각"
    assert m.attendance_judgment(16) == "결석"
    assert m.attendance_judgment(20) == "결석"
    assert m.attendance_judgment(20, True) == "운영실 확인"
    with pytest.raises(ValueError):
        m.attendance_judgment(-1)

def test_comparison_preserves_the_same_evidence():
    hit = example_hit()
    hit["citation_id"] = 901
    original = deepcopy(hit)
    rows = m.comparison(hit)
    assert [(r["minutes"], r["prior_approval"]) for r in rows] == [(15, False), (20, False), (20, True)]
    assert [r["judgment"] for r in rows] == ["지각", "결석", "운영실 확인"]
    assert all(r["citation_id"] == 901 and r["evidence"] == hit["body"] for r in rows)
    assert all(r["source_locator"] == hit["source_locator"] for r in rows)
    assert hit == original
