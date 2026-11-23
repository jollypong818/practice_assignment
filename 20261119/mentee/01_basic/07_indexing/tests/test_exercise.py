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
    doc,chunk=m.select_index_chunk('DOC-ASSIGN')
    assert chunk['doc_id']==doc['doc_id']
    assert chunk['embedding_text'].startswith('passage: ')
    r=m.format_hit((201,'C','body','a#1','DOC','v1',.2))
    assert r['citation_id']==201 and r['cosine_distance']==.2
    with pytest.raises(ValueError):m.format_hit((0,'C','body','a#1','DOC','v1',.2))
