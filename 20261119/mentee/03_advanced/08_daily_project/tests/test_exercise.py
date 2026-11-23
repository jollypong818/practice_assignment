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
    rows=m.read_manifest();prepared,statuses=m.prepare_all(rows)
    report=m.make_final_report(rows,statuses,prepared)
    assert report['source_mode']=='prepared_only_not_embedded'
    assert report['by_status']=={'needs_ocr':1,'parsed':4,'unsupported':1}
    assert len(prepared)==4 and report['prepared_chunk_count']>0


def test_v2_parser_and_pointer_regression_with_stubbed_db(monkeypatch):
    """개정 문서 Parser·공개 포인터 흐름을 단위 검사합니다.

    FakeConn은 실제 PostgreSQL Transaction 또는 pgvector 연결 검사가 아닙니다.
    """
    from contextlib import contextmanager
    import coursekit.db as db
    import coursekit.live as live

    class FakeResult:
        def __init__(self, version):self.version=version
        def fetchone(self):return (self.version,)

    class FakeConn:
        def __init__(self):self.current='v1'
        def execute(self, statement, params):
            assert 'SELECT current_version' in statement
            assert params==('DOC-ATTEND',)
            return FakeResult(self.current)
        @contextmanager
        def transaction(self):
            before=self.current
            try:
                yield
            except Exception:
                self.current=before
                raise

    recorded=[]
    def fake_stage(conn,doc,source_uri,chunks,vectors):
        assert doc['source_version']=='v2'
        assert source_uri=='versions/attendance_v2.md'
        assert len(chunks)==len(vectors)
        recorded.append(chunks)
    def fake_publish(conn,doc_id,version,pipeline):
        assert doc_id=='DOC-ATTEND' and version=='v2'
        conn.current=version
    monkeypatch.setattr(db,'stage_version',fake_stage)
    monkeypatch.setattr(db,'publish_version',fake_publish)
    monkeypatch.setattr(live,'encode_passages',lambda model,chunks:[None]*len(chunks))

    result=m.regression_v2(FakeConn(),object())
    assert result=={'before':'v1','after_failure':'v1','after_retry':'v2'}
    assert len(recorded)==2  # 실패한 시도와 정상 재시도
    for chunks in recorded:
        assert [c['unit_id'] for c in chunks]==['sec-1','sec-2']
        assert chunks[0]['section_title']=='지각과 결석'
        assert chunks[1]['section_title']=='출석 문의'
        assert '15분' in chunks[0]['body']
        assert '출석 기록에 오류가 있다면' in chunks[1]['body']
