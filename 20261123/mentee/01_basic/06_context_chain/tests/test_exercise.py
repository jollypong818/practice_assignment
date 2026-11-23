"""로컬 입력·출력 계약만 검사합니다. 실제 모델/DB/네트워크를 호출하지 않습니다."""
from pathlib import Path
import importlib.util
import sys
import pytest

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE.parents[1]))


@pytest.fixture
def exercise():
    spec = importlib.util.spec_from_file_location("day26_06_B", HERE / "main.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


from copy import deepcopy
from langchain_core.runnables import RunnableLambda
from coursekit.data import load_hits
from coursekit.checkpoints import hits_to_documents, make_prompt
from coursekit.fixtures import fixture_bundle


def documents():
    return hits_to_documents([hit for hit in load_hits() if hit["category"] == "학사"])


def test_context_keeps_only_included_sources(exercise):
    docs = documents()
    original = deepcopy(docs)
    prepared = exercise.prepare_context(docs, "질문", max_items=1)
    assert prepared["provided_ids"] == [201]
    assert prepared["included_docs"] == [docs[0]]
    assert prepared["inputs"] == {"question": "질문", "context": prepared["context"]}
    assert "[201]" in prepared["context"] and "[202]" not in prepared["context"]
    assert docs == original
    with pytest.raises(ValueError):
        exercise.prepare_context(docs, "질문", max_items=0)


def test_chain_passes_prompt_value_and_preserves_bundle(exercise):
    calls = []
    bundle = fixture_bundle()
    def structured(value):
        calls.append(value)
        return bundle
    prepared = exercise.prepare_context(documents(), "15분 늦으면 어떻게 기록되나요?")
    result = exercise.run_generation(make_prompt(), RunnableLambda(structured), prepared["inputs"])
    assert result is bundle and set(result) == {"raw", "parsed", "parsing_error"}
    assert len(calls) == 1 and type(calls[0]).__name__ == "ChatPromptValue"
    assert prepared["context"] in calls[0].to_messages()[-1].content
    assert prepared["provided_ids"] == [201, 202]


def test_empty_documents_have_no_allowed_source(exercise):
    prepared = exercise.prepare_context([], "질문")
    assert prepared["context"] == "" and prepared["included_docs"] == []
    assert prepared["provided_ids"] == []
