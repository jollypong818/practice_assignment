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
SPEC = importlib.util.spec_from_file_location("d26_mentor_1_I", MODULE_PATH)
m = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = m
SPEC.loader.exec_module(m)

def test_stage_sequence_connects_inputs_and_outputs():
    assert m.stage_order() == [
        "Retriever", "Context Builder", "Prompt", "Generator", "Validator · Source 연결"]

def test_document_present_does_not_make_a_date_present():
    hits = load_hits()
    hit = m.find_hit(hits, "DOC-ASSIGN")
    row = m.deadline_note(hit)
    assert row["document_found"] is True
    assert row["exact_date_available"] is False
    assert row["expected_status"] == "insufficient_context"
    assert row["evidence"] == hit["body"]
    assert row["citation_id"] == hit["citation_id"]
    assert row["source_locator"] == hit["source_locator"]

def test_missing_document_is_not_replaced_with_another():
    with pytest.raises(LookupError):
        m.find_hit(load_hits(), "DOC-NOT-PROVIDED")
