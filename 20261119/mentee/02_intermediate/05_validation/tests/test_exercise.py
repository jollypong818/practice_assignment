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
    assert m.coverage(20,[(0,8),(10,20)])==.9
    assert m.make_report(20,[(0,8),(6,14),(12,20)],['A','B','C'])['valid']
    assert m.make_report(20,[(0,8),(0,8),(8,20)],['A','A','C'])['errors']['duplicate_ids']==['A']
