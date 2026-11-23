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
    doc,chunks=m.prepare('DOC-ASSIGN')
    assert chunks and all(c['doc_id']==doc['doc_id'] for c in chunks)
    assert all(c['embedding_text'].startswith('passage: ') for c in chunks)
