"""보고서 Router: Path/Query/JSON/HTTP Status와 Service 호출만 담당합니다."""
from datetime import datetime
from fastapi import APIRouter,Depends,Query,Path,Body,Response
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.report import (ReportCreate,ReportUpdate,SummaryRequest,PromptVersionCreate,
                                PromptActivation,ReindexRequest,CategoryCode)
from app.services import report_service
from app.core.config import at_least
from app.services.errors import DomainError

router=APIRouter(prefix='/api/v1',tags=['Reports & Categories'])

@router.get('/categories')
def categories(db:Session=Depends(get_db)):
    return report_service.categories(db)

@router.post('/reports',status_code=201)
def create_report(body:ReportCreate,db:Session=Depends(get_db)):
    return report_service.create_report(db,body)

@router.get('/reports')
def list_reports(title:str|None=None,limit:int=Query(20,ge=1,le=100),
                 offset:int=Query(0,ge=0),category_code:CategoryCode|None=None,
                 updated_after:datetime|None=None,db:Session=Depends(get_db)):
    if not at_least('intermediate') and (category_code is not None or updated_after is not None):
        raise DomainError(422,'VALIDATION_ERROR','추가 필터는 Intermediate 기능입니다.')
    return report_service.list_reports(db,title,limit,offset,category_code,updated_after)

@router.get('/reports/{report_id}')
def get_report(report_id:int=Path(ge=1),db:Session=Depends(get_db)):
    return report_service.get_report(db,report_id)

@router.put('/reports/{report_id}')
def update_report(body:ReportUpdate,report_id:int=Path(ge=1),db:Session=Depends(get_db)):
    return report_service.update_report(db,report_id,body)

@router.delete('/reports/{report_id}',status_code=204)
def delete_report(report_id:int=Path(ge=1),db:Session=Depends(get_db)):
    report_service.delete_report(db,report_id)
    return Response(status_code=204)

@router.post('/reports/{report_id}/summarize')
def summarize(report_id:int=Path(ge=1),body:SummaryRequest=Body(default_factory=SummaryRequest),
              db:Session=Depends(get_db)):
    return report_service.summarize_report(db,report_id,body.style,body.max_sentences)

@router.post('/prompts/{report_id}/versions',status_code=201)
def prompt_add_version(body:PromptVersionCreate,report_id:int=Path(ge=1),db:Session=Depends(get_db)):
    return report_service.prompt_add_version(db,report_id,body.prompt_text)

@router.get('/prompts/{report_id}/versions')
def prompt_list_versions(report_id:int=Path(ge=1),db:Session=Depends(get_db)):
    return report_service.prompt_list_versions(db,report_id)

@router.put('/prompts/{report_id}/active-version')
def prompt_activate(body:PromptActivation,report_id:int=Path(ge=1),db:Session=Depends(get_db)):
    return report_service.prompt_activate(db,report_id,body.version_no)

@router.post('/reports/{report_id}/reindex')
def reindex(body:ReindexRequest,report_id:int=Path(ge=1),db:Session=Depends(get_db)):
    return report_service.reindex_report(db,report_id,body.force)
