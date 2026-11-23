"""정상/경계 사례를 검증합니다. mentee는 TODO를 채우기 전 실패가 정상입니다."""
from pathlib import Path
import sys
import pytest
HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE))
sys.path.insert(0,str(HERE.parents[1]))
from coursekit.io import DATA,load_json
from coursekit.documents import by_doc,parse_one
import tasks as m


def test_contract():
    base={'doc_id':'DOC','source_version':'v1','pipeline_version':'p1','source_locator':'x','category':'학사','chunk_id':'C','char_start':0,'char_end':9,'page_number':None}
    m.validate_locator(base)
    with pytest.raises(ValueError):m.validate_locator({**base,'page_number':0})
    assert m.select_current([base],{'DOC':('v1','p1')})==[base]
