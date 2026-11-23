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
    r=m.regression();assert r['fixed_passed']==2 and len(r['failure_reasons'])==2
    assert m.duplicated_ids([{'chunk_id':'X'},{'chunk_id':'X'}])==['X']
    assert m.coverage_stats([], 'text')['coverage']==0.0
