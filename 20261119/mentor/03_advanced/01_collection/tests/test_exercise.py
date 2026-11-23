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
    rows=m.validate_manifest(load_json(DATA/'manifest.json'))
    items=[m.collect_one(r) for r in rows]
    assert m.reconcile(items)['by_status']['unsupported']==1
    assert m.fingerprint(items)==m.fingerprint([m.collect_one(r) for r in rows])
    assert m.compare_version(items[0],{'raw_sha256':'X'})=='changed'
    with pytest.raises(ValueError):m.validate_manifest(rows+[rows[0]])
