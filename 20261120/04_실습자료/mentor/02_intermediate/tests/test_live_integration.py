"""실제 DB 통합 테스트. RUN_LIVE_TESTS=1일 때만 수행; 유료 LLM 호출 없음."""
import os
import pytest
pytestmark=pytest.mark.live


def test_pgvector_live_sql():
    if os.getenv('RUN_LIVE_TESTS')!='1':
        pytest.skip('실제 DB 테스트가 비활성화되어 있습니다. RUN_LIVE_TESTS=1 설정 후 실행하세요.')
    from sqlalchemy import text
    from app.db.session import get_session_factory
    with get_session_factory()() as db:
        total=db.execute(text('SELECT COUNT(*) FROM reports')).scalar_one()
        vector=db.execute(text('SELECT COUNT(*) FROM report_embeddings')).scalar_one()
        dims=db.execute(text('SELECT COUNT(*) FROM report_embeddings WHERE vector_dims(embedding)<>384')).scalar_one()
    assert total>=180, '시드 적재 후 각 30개가 있는지 확인'
    assert vector>=180, '실제 E5 초기 인덱싱 완료 후 실행하세요'
    assert dims==0
