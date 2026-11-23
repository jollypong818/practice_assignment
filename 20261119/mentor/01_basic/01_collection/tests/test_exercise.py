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
    p=DATA/'raw'/'assignment.txt'
    raw=m.read_raw(p); r=m.build_record('DOC-ASSIGN',p,raw)
    assert r['size_bytes']==len(raw) and len(r['raw_sha256'])==64
    with pytest.raises(FileNotFoundError):m.read_raw(p.with_name('not-found.txt'))
