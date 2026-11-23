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
    assert m.apply_nfc('가')=='가'
    assert '10분' in m.normalize_prose('10분  초과')
    assert m.check_phrases('과제 안내',['기한'])['missing']==['기한']
    a=m.make_audit('출석   안내','출석 안내',['안내'])
    assert len(a['clean_hash'])==64
