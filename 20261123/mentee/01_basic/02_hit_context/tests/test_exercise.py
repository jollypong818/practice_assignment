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
SPEC = importlib.util.spec_from_file_location("d26_mentee_2_B", MODULE_PATH)
m = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = m
SPEC.loader.exec_module(m)

def test_context_and_ids_have_the_same_selected_source():
    hits = load_hits()
    original = deepcopy(hits)
    context, ids = m.make_context(hits, max_items=1)
    assert ids == [hits[0]["citation_id"]]
    assert context == f'[{hits[0]["citation_id"]}] {hits[0]["source_locator"]}\n{hits[0]["body"]}'
    assert hits[1]["body"] not in context
    assert hits == original

def test_format_hit_preserves_new_ids_and_conditions():
    hit = example_hit()
    hit["citation_id"] = 901
    text = m.format_hit(hit)
    assert text.startswith("[901] ")
    assert text.endswith(hit["body"])
    assert "15분까지" in text and "사전 승인" in text

def test_empty_and_one_are_not_padded_with_fake_hits():
    assert m.make_context([]) == ("", [])
    hit = example_hit()
    context, ids = m.make_context([hit], max_items=2)
    assert ids == [hit["citation_id"]]
    assert context == m.format_hit(hit)
