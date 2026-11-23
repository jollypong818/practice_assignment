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
    s='10분 초과는 결석';g={'char_start':0,'char_end':len(s),'text':s}
    m.check_content(g,s)
    with pytest.raises(ValueError):m.check_content({**g,'text':'삭제'},s)
    with pytest.raises(ValueError):m.check_bounds({**g,'char_end':100},s)
