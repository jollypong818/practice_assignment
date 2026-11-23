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
    rows=load_json(DATA/'manifest.json');r=m.run_audit(rows)
    assert r['total']==6 and r['repeat_equal']
    assert r['status_counts']['parsed']==4
    assert r['status_counts']['needs_ocr']==1
    pdf=next(d for d in rows if d['doc_id']=='DOC-CAREER')
    p=m.dispatch(pdf);m.check_pdf(pdf,p)
    assert len(p['units'])==2
