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
    v1,a=m.prepare_revision('DOC-ATTEND','v1');v2,b=m.prepare_revision('DOC-ATTEND','v2')
    assert v1['source_version']=='v1' and v2['source_version']=='v2'
    assert a and b and a[0]['chunk_id']!=b[0]['chunk_id']
    # v1과 v2의 파서·절 경계는 동일하고, 바뀐 정책 문장만 새 판으로 관리합니다.
    assert [c['unit_id'] for c in a] == ['sec-1','sec-2']
    assert [c['unit_id'] for c in b] == ['sec-1','sec-2']
    assert '10분' in a[0]['body'] and '15분' in b[0]['body']
    assert '출석 기록에 오류가 있다면' in b[1]['body']
    assert all('# 출석 안내' not in c['body'] for c in b)
    with pytest.raises(ValueError):m.prepare_revision('DOC-ATTEND','v9')
