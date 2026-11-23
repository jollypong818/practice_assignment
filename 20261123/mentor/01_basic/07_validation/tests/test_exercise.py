"""로컬 계약 검사. 실제 DB·모델 다운로드·유료 API를 실행하지 않습니다."""
from pathlib import Path
import importlib.util
import sys
import pytest

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE.parents[1]))
spec = importlib.util.spec_from_file_location("d26_7_01_basic", HERE / "main.py")
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)


def test_common_cases_and_actual_included_boundary():
    from coursekit.checkpoints import hits_to_documents
    from coursekit.data import load_hits
    docs = hits_to_documents(load_hits())
    ids = m.allowed_source_ids(docs[:1])
    assert ids == {201}
    assert m.allowed_source_ids([]) == set()
    docs[0].metadata["citation_id"] = 701
    assert m.allowed_source_ids(docs[:1]) == {701}  # hard-code 201 불가
    records = {row["case"]: row for row in [m.inspect_case(case, {201}) for case in m.common_cases()]}
    assert records["normal"]["outcome"] == "accepted"
    assert records["normal"]["human_review_required"] is True
    assert records["insufficient"]["outcome"] == "accepted"
    assert records["insufficient"]["result"]["source_ids"] == []
    assert records["unknown_source"]["error"] == "answer_validation_error"


def test_raw_receipt_checks_precede_parsed_answer():
    from langchain_core.messages import AIMessage
    from coursekit.fixtures import fixture_bundle
    bundle = fixture_bundle()
    bundle["raw"] = AIMessage(content=[{"type": "refusal", "refusal": "고정 거절 예시"}],
                              response_metadata={"status": "completed"})
    row = m.inspect_case({"name": "refusal", "bundle": bundle}, {201})
    assert row["error"] == "provider_refusal"
    row = m.inspect_case({"name": "invalid_bundle", "bundle": {}}, {201})
    assert row["error"] == "invalid_bundle"


def test_report_is_labelled_fixture():
    report = m.run()
    assert report["source_mode"] == "validation_fixtures"
    assert report["included_ids"] == [201]
    assert report["context"].startswith("[201]")
