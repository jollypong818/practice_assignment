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
    assert [(r['char_start'],r['char_end']) for r in m.make_windows('x'*71,40,10)]==[(0,40),(30,70),(60,71)]
    with pytest.raises(ValueError):m.check_params(20,20)
    assert m.make_windows('',40,10)==[]
