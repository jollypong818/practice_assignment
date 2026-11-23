"""A-07: 실제 PostgreSQL 연결에서만 실행하는 원자성 회귀 테스트.
실행: RUN_LIVE_TESTS=1 pytest -q -m live  (Windows Git Bash)
시드 데이터를 수정하지 않고 임시 보고서를 만들었다가 의도적으로 롤백합니다.
"""
import os
from datetime import date
import pytest
from sqlalchemy import select
pytestmark=pytest.mark.live


def test_rollback_keeps_database_clean():
    if os.getenv('RUN_LIVE_TESTS')!='1':
        pytest.skip('실제 PostgreSQL 연결 설정 후 명시적으로 실행하세요.')
    from app.db.session import get_session_factory
    from app.models.report import Report,ExperimentReport,ReportEmbedding
    import app.integrations.embedding_client as emb
    factory=get_session_factory()
    try:
        with factory() as db:
            with db.begin():
                row=Report(category_id=1,overview='Rollback 전용 테스트 개요이며 실제 적재되지 않아야 합니다.',
                           index_status='pending',revision=1)
                db.add(row);db.flush()
                rid=row.report_id
                detail=ExperimentReport(report_id=rid,title='Rollback 검증',content='DB 트랜잭션 실패 검증',
                   author='테스트',experiment_date=date(2026,11,20),
                   hypothesis='의도적 예외 뒤에는 저장되지 않는다',result_summary='Rollback 예상')
                db.add(detail);db.flush()
                # 진짜 E5가 아닌 기존 Vector를 참조해 임시 INSERT만 시험합니다.
                sample=db.scalar(select(ReportEmbedding).limit(1))
                if sample is None:pytest.fail('E5 인덱싱을 먼저 실행해야 합니다.')
                db.add(ReportEmbedding(report_id=rid,embedding=sample.embedding,
                   model_name=sample.model_name,overview_hash=emb.overview_hash(row.overview),indexed_revision=1))
                db.flush()
                raise RuntimeError('의도적인 테스트 롤백')
    except RuntimeError as e:
        assert str(e)=='의도적인 테스트 롤백'
    with factory() as db:
        assert db.get(Report,rid) is None
        assert db.get(ExperimentReport,rid) is None
        assert db.get(ReportEmbedding,rid) is None
