"""정상/경계 사례를 검증합니다. mentee는 TODO를 채우기 전 실패가 정상입니다."""
from pathlib import Path
import sys
import pytest
HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE))
sys.path.insert(0,str(HERE.parents[1]))
from coursekit.io import DATA,load_json
from coursekit.documents import by_doc,parse_one
import main as m


def test_contract():
    a=m.attach_metadata({'chunk_id':'C1','body':'x'}, {'doc_id':'DOC','source_version':'v1','category':'학사','source_locator':'a#1'})
    assert m.select_category([a],'시설')==[]
    assert m.select_category([a],'학사')[0]['doc_id']=='DOC' 
