"""자신의 심화 구현을 검사합니다. 실제 모델 품질 테스트가 아닙니다."""
from pathlib import Path
import sys
import pytest
HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE))
sys.path.insert(0,str(HERE.parents[1]))
from coursekit.io import DATA, read_json
from validation import make_model, validate_answer

@pytest.mark.parametrize("fid",["valid_answer","valid_insufficient","broken_json","string_id","bool_id","extra_field","unknown_source","example_leak","outside_context","duplicate_source","blank_answer","semantic_counterexample"])
def test_own_validator(fid):
    item=next(x for x in read_json(DATA/"validation_fixtures.json") if x["fixture_id"]==fid)
    obj,error=validate_answer(item["raw_text"],item["provided_ids"])
    assert error==item["expected_error"]
    assert (obj is not None)==(error is None)

def test_schema_required_and_extra():
    schema=make_model().model_json_schema()
    assert schema["additionalProperties"] is False
    assert set(schema["required"])=={"status","answer","source_ids","missing_information"}
