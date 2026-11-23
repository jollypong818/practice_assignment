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
SPEC = importlib.util.spec_from_file_location("d26_mentor_4_A", MODULE_PATH)
m = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = m
SPEC.loader.exec_module(m)

def test_document_keeps_body_and_six_metadata_fields():
    from langchain_core.documents import Document
    hit = example_hit()
    original = deepcopy(hit)
    docs = m.hits_to_documents([hit])
    assert len(docs) == 1 and isinstance(docs[0], Document)
    doc = docs[0]
    assert doc.page_content == hit["body"]
    keys = {"citation_id", "chunk_id", "doc_id", "source_version", "source_locator", "category"}
    assert set(doc.metadata) == keys
    assert all(doc.metadata[k] == hit[k] for k in keys)
    assert type(doc.metadata["citation_id"]) is int
    assert hit == original

def test_empty_and_missing_locator_are_different():
    assert m.hits_to_documents([]) == []
    hit = example_hit()
    del hit["source_locator"]
    with pytest.raises(KeyError, match="source_locator"):
        m.hits_to_documents([hit])

def test_input_order_and_realistic_new_ids_are_preserved():
    hits = load_hits()[:2]
    hits[0]["citation_id"], hits[1]["citation_id"] = 5002, 5001
    docs = m.hits_to_documents(hits)
    assert [d.metadata["citation_id"] for d in docs] == [5002, 5001]
    assert [d.page_content for d in docs] == [h["body"] for h in hits]

def test_boundary_demo_does_not_destroy_the_original():
    hit = example_hit()
    original = deepcopy(hit)
    assert m.inspect_boundary_cases(hit) == {"empty_count": 0, "missing_key": "source_locator"}
    assert hit == original


def test_observation_rejects_partial_extra_or_changed_metadata():
    # 학습 TODO의 정답 여부와 별개로 제공 runner의 관찰 판정을 검사합니다.
    hit = example_hit()
    keys = {"citation_id", "chunk_id", "doc_id", "source_version", "source_locator", "category"}
    complete = {key: hit[key] for key in keys}
    assert m.metadata_is_preserved(hit, complete) is True
    assert m.metadata_is_preserved(hit, {"citation_id": hit["citation_id"]}) is False
    assert m.metadata_is_preserved(hit, {**complete, "extra": True}) is False
    assert m.metadata_is_preserved(hit, {**complete, "source_version": "v0"}) is False
