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
    raw=(DATA/'raw'/'assignment.txt').read_bytes()
    assert '과제 안내' in m.decode_text(raw)
    unit=m.make_unit('DOC-ASSIGN','v1',m.decode_text(raw))
    assert unit['page_number'] is None and unit['unit_id']=='text-1'
    with pytest.raises(UnicodeDecodeError):m.decode_text(b'\xff')
