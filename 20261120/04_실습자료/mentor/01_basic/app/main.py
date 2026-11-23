"""보고서 처리 Agent 애플리케이션 진입점. 실행: python -m app.main"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy import text
from app.api import reports,search,agent
from app.db.session import get_session_factory
from app.services.errors import DomainError
from app.core.config import at_least

app=FastAPI(title='Report Agent | 2026-11-20',version='1.0.0')
app.include_router(reports.router)
app.include_router(search.router)
app.include_router(agent.router)

@app.exception_handler(DomainError)
def on_domain_error(request:Request,exc:DomainError):
    return JSONResponse(status_code=exc.status,
      content={'error':{'code':exc.code,'message':exc.message,'details':{}}})

if at_least('advanced'):
    from sqlalchemy.exc import SQLAlchemyError,OperationalError
    @app.exception_handler(SQLAlchemyError)
    def on_database_error(request:Request,exc:SQLAlchemyError):
        # 연결 장애와 처리 오류를 구분하되 SQL·인증·접속정보는 반환하지 않습니다.
        unavailable=isinstance(exc,OperationalError)
        return JSONResponse(status_code=503 if unavailable else 500,content={'error':{
            'code':'DB_UNAVAILABLE' if unavailable else 'INTERNAL_ERROR',
            'message':'데이터베이스 처리를 완료하지 못했습니다.','details':{}}})

if at_least('intermediate'):
    from fastapi.exceptions import RequestValidationError
    @app.exception_handler(RequestValidationError)
    def on_request_error(request:Request,exc:RequestValidationError):
        # 잘못된 입력 원문·API 키·인증 값 등을 응답에 그대로 넣지 않습니다.
        return JSONResponse(status_code=422,
          content={'error':{'code':'VALIDATION_ERROR','message':'요청 값을 확인하세요.','details':{}}})

@app.get('/health',tags=['System'])
def health():
    try:
        with get_session_factory()() as db:
            db.execute(text('SELECT 1')).scalar_one()
            exists=db.execute(text("SELECT EXISTS(SELECT 1 FROM pg_extension WHERE extname='vector')")).scalar_one()
            if not exists:raise RuntimeError('pgvector extension missing')
        return {'status':'ok','db':'ready','vector':'ready'}
    except Exception:
        return JSONResponse(status_code=503,
           content={'error':{'code':'DB_UNAVAILABLE','message':'DB 또는 pgvector를 확인하세요.','details':{}}})


def main():
    import uvicorn
    # 공통 main()은 완성. Core 구현은 app/api, services, repositories에 분리.
    uvicorn.run('app.main:app',host='127.0.0.1',port=8000,reload=False)

if __name__=='__main__':main()
