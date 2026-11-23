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
    assert m.choose_policy('code')=='preserve_structure'
    assert m.clean_block('    x=1','code')=='    x=1'
    assert m.check_critical('10분 초과','초과',['10분'])['passed'] is False
    assert m.check_idempotent(m.clean_block('a  b','prose'),'prose')
    assert len(m.clean_fingerprint('가'))==64
