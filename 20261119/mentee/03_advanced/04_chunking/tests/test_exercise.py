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
    doc=by_doc('DOC-ATTEND');u=parse_one(doc)['units'][0]
    r=m.check_repeat(doc,u); assert r['stable'] and r['chunks']
    assert all(m.embedding_input(c,True).startswith('passage: ') for c in r['chunks'])
    assert m.check_model_lengths(r['chunks'],None)['status']=='not_run' 
