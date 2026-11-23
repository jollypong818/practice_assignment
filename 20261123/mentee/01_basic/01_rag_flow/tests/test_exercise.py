"""현재 폴더의 구현만 검사합니다. API·DB·다운로드는 실행하지 않습니다."""
import importlib.util
from pathlib import Path
import sys
from copy import deepcopy
import pytest

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE.parents[1]))
from coursekit.data import example_hit, load_hits

MODULE_PATH = HERE / "main.py"
SPEC = importlib.util.spec_from_file_location("d26_mentee_1_B", MODULE_PATH)
m = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = m
SPEC.loader.exec_module(m)

def test_stage_sequence_connects_inputs_and_outputs():
    assert m.stage_order() == [
        "Retriever", "Context Builder", "Prompt", "Generator", "Validator · Source 연결"]

def test_evidence_keeps_the_actual_source_values():
    hit = example_hit()
    hit["citation_id"] = 901
    original = deepcopy(hit)
    row = m.evidence_note(hit)
    assert row["citation_id"] == 901
    assert row["evidence"] == hit["body"]
    assert row["source_version"] == "v2"
    assert row["source_locator"] == hit["source_locator"]
    assert row["judgment"] == "지각"
    assert "승인" in row["exception_to_check"] and "운영실" in row["exception_to_check"]
    assert hit == original
