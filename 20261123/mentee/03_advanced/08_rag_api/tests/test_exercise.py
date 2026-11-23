"""로컬 계약 검사. 실제 DB·모델 다운로드·유료 API를 실행하지 않습니다."""
from pathlib import Path
import importlib.util
import sys
import pytest

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE.parents[1]))
spec = importlib.util.spec_from_file_location("d26_8_03_advanced", HERE / "tasks.py")
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)


def test_request_wiring_and_valid_sources():
    from fastapi.testclient import TestClient
    payload = m.make_request(m.NORMAL_QUERY, "학사", candidate_k=2, context_k=1)
    assert payload == {"query": m.NORMAL_QUERY, "category": "학사", "candidate_k": 2, "context_k": 1}
    app = m.wire_app(m.fixture_retriever(), m.fixture_generation())
    with TestClient(app) as client:
        response = client.post("/rag/answer", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["result"]["status"] == "answered"
    assert body["result"]["source_ids"] == [source["citation_id"] for source in body["sources"]]
    assert body["result"]["source_ids"] == [201]


def test_request_validation_happens_before_retrieval():
    from fastapi.testclient import TestClient
    from langchain_core.runnables import RunnableLambda
    calls = []
    def unexpected(request):
        calls.append(request)
        raise AssertionError("422 요청은 검색을 호출하면 안 됩니다.")
    app = m.wire_app(RunnableLambda(unexpected), m.fixture_generation())
    base = m.make_request(m.NORMAL_QUERY, "학사")
    with TestClient(app) as client:
        for patch in [{"candidate_k": 0}, {"candidate_k": True}, {"context_k": 4},
                      {"query": "   "}, {"category": "전체"}, {"extra": 1}]:
            assert client.post("/rag/answer", json={**base, **patch}).status_code == 422
    assert calls == []


def test_failure_boundary_and_source_allowlist():
    from fastapi.testclient import TestClient
    from langchain_core.runnables import RunnableLambda
    def broken(request):
        raise RuntimeError("테스트용 검색 실패")
    payload = m.make_request(m.NORMAL_QUERY, "학사")
    cases = [
        (RunnableLambda(broken), m.fixture_generation(), "retrieval_error"),
        (m.fixture_retriever(), m.fixture_generation("timeout"), "generation_error"),
        (m.fixture_retriever(), m.fixture_generation("unknown_source"), "answer_validation_error"),
    ]
    for retriever, generation, expected in cases:
        with TestClient(m.wire_app(retriever, generation)) as client:
            response = client.post("/rag/answer", json=payload)
        assert response.status_code == 502
        assert response.json() == {"detail": expected}


def test_offline_smoke_never_requires_live_components(monkeypatch):
    def guarded(offline):
        assert offline is True
        return m.fixture_retriever(), m.fixture_generation()
    monkeypatch.setattr(m, "prepare_components", guarded)
    result = m.run_smoke(offline=True)
    assert result["source_mode"] == "fixture_api_smoke"
    assert result["checks_passed"] is True
    assert [row["http_status"] for row in result["api_cases"]] == [200, 200, 422]
    assert result["api_cases"][2]["retrieval_attempts"] == 0
    assert result["api_cases"][2]["generation_attempts"] == 0


def test_one_parameter_comparison_preserves_original():
    original = m.make_request(m.NORMAL_QUERY, "학사", candidate_k=3, context_k=2)
    changed = m.comparison_request(original)
    assert original["context_k"] == 2
    assert changed == {**original, "context_k": 1}
    report = m.run_smoke(offline=True, compare_k=True)
    assert len(report["api_cases"]) == 4
    base, _, _, compare = report["api_cases"]
    assert base["candidate_ids"] == compare["candidate_ids"]
    assert len(compare["included_ids"]) <= 1
    assert len(base["included_ids"]) <= 2
    assert report["checks_passed"] is True


def test_empty_context_skips_generation_and_timeout_is_separate():
    rows = {row["case"]: row for row in m.failure_examples()}
    empty, timeout = rows["empty_context"], rows["timeout"]
    assert empty["http_status"] == 200
    assert empty["response"]["result"]["status"] == "insufficient_context"
    assert empty["generation_attempts"] == 0
    assert empty["response"]["sources"] == []
    assert timeout["http_status"] == 502
    assert timeout["response"] == {"detail": "generation_error"}
    assert timeout["generation_attempts"] == 1
    assert all(row["source_mode"] == "fixed_failure_example" for row in rows.values())
