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
    r={'doc_id':'DOC','source_version':'v1','pipeline_version':'p1','unit_id':'u1','source_locator':'x','category':'학사','char_start':0,'char_end':3,'page_number':None,'citation_id':201}
    r['chunk_id']=m.stable_id(r)
    assert list(m.citation_map([r]))==[201]
    assert m.audit([r],{'DOC':('v1','p1')},{'DOC'},'학사')['citations']
    assert m.audit([r],{'DOC':('v1','p1')},set(),'학사')['excluded_permission']==1
    with pytest.raises(ValueError):m.citation_map([r,{**r,'citation_id':201}])
