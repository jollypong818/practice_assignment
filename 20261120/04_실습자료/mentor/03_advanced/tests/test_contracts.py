"""PostgreSQL 미연결 상태에서 데이터 모델과 요청 계약을 검증합니다."""
import pytest
from app.models.report import Base,DETAIL_MODELS,ReportEmbedding,Report,PromptVersion
from app.schemas.report import ReportCreate,SimilarRequest
from app.services.report_service import validate_details
from app.services.errors import DomainError
from app.main import app


def test_er_d_has_ten_physical_tables():
    assert len(Base.metadata.tables)==10
    assert set(DETAIL_MODELS)=={'EXPERIMENT','DAILY_WORK','RESEARCH_PLAN','DATA_PROCESSING','PROMPT','MEETING'}
    for name,model in DETAIL_MODELS.items():
        cols=set(model.__table__.columns.keys())
        assert {'report_id','title','author','content','create_at','update_at'}<=cols
    assert ReportEmbedding.__table__.c.embedding.type is not None


def test_required_http_contract():
    routes=app.openapi()['paths']
    base=['/health','/api/v1/categories','/api/v1/reports','/api/v1/reports/{report_id}',
          '/api/v1/search/similar','/api/v1/reports/{report_id}/summarize','/api/v1/agent/run']
    assert all(p in routes for p in base)
    assert 'post' in routes['/api/v1/reports']
    assert 'get' in routes['/api/v1/reports']
    assert {'get','put','delete'}<=set(routes['/api/v1/reports/{report_id}'])


def test_api_422_for_empty_overview():
    valid={'category_code':'EXPERIMENT','title':'단위테스트','author':'검수자',
           'content':'결과를 충분히 설명한 본문','overview':'공백이 너무 많은 개요','details':{}}
    bad={**valid,'overview':'         X         '}
    with pytest.raises(Exception): ReportCreate.model_validate(bad)


def test_search_input_limits():
    with pytest.raises(Exception): SimilarRequest(query=' ',keyword_limit=100)
    with pytest.raises(Exception): SimilarRequest(query='가중치',keyword_limit=101)


@pytest.mark.parametrize('code,details',[ 
 ('EXPERIMENT',{'experiment_date':'2026-11-20','hypothesis':'성능 개선','result_summary':'검증 결과'}),
 ('DAILY_WORK',{'work_date':'2026-11-20','progress':'작업 완료','blockers':''}),
 ('RESEARCH_PLAN',{'research_goal':'품질 개선','methodology':'비교','target_date':'2026-12-01'}),
 ('DATA_PROCESSING',{'dataset_name':'요청 로그','processing_steps':'정제','quality_notes':''}),
 ('PROMPT',{'purpose':'요약','prompt_text':'주어진 문서를 요약하라.'}),
 ('MEETING',{'meeting_at':'2026-11-20T10:00:00+09:00','attendees':'담당자','decisions':'합의'}),
 ])
def test_category_details(code,details):
    content=details.get('prompt_text') if code=='PROMPT' else '기본 원문'
    assert validate_details(code,details,content)


def test_invalid_prompt_content_mismatch():
    with pytest.raises(DomainError):
        validate_details('PROMPT',{'purpose':'요약','prompt_text':'명령 A'},'다른 본문')


def test_missing_date_error():
    with pytest.raises(DomainError):
        validate_details('EXPERIMENT',{'experiment_date':'not-a-date','hypothesis':'가설','result_summary':'결과'},'본문')
