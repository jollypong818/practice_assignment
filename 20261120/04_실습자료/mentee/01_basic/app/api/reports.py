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
    """TODO B-04 · categories() — mentor와 동일한 함수 계약을 완성하세요."""
    # TODO B-04: ReportService의 카테고리 목록 조회 함수를 호출하고 items 배열을 반환하세요.
    # 입력·반환형과 예외·상태코드는 요구사항 명세서/API 계약을 참조합니다.
    # 정답 구현 후 아래 예외를 지우고 로직을 작성하세요.
    raise NotImplementedError("B-04 · categories() TODO 미완성")

@router.post('/reports',status_code=201)
def create_report(body:ReportCreate,db:Session=Depends(get_db)):
    """TODO B-05 · create_report() — mentor와 동일한 함수 계약을 완성하세요."""
    # TODO B-05: ReportService에 Pydantic 요청 객체를 전달하여 보고서+상세+Vector 저장 결과를 반환하세요. HTTP
    # TODO B-05: 201 계약을 유지합니다.
    # 입력·반환형과 예외·상태코드는 요구사항 명세서/API 계약을 참조합니다.
    # 정답 구현 후 아래 예외를 지우고 로직을 작성하세요.
    raise NotImplementedError("B-05 · create_report() TODO 미완성")

@router.get('/reports')
def list_reports(title:str|None=None,limit:int=Query(20,ge=1,le=100),
                 offset:int=Query(0,ge=0),category_code:CategoryCode|None=None,
                 updated_after:datetime|None=None,db:Session=Depends(get_db)):
    """TODO B-07 · list_reports() — mentor와 동일한 함수 계약을 완성하세요."""
    # TODO B-07: Title/limit/offset을 서비스에 전달하세요. Basic 범위에서는 추가 Category/updated_after
    # TODO B-07: 필터를 거절합니다.
    # 입력·반환형과 예외·상태코드는 요구사항 명세서/API 계약을 참조합니다.
    # 정답 구현 후 아래 예외를 지우고 로직을 작성하세요.
    raise NotImplementedError("B-07 · list_reports() TODO 미완성")

@router.get('/reports/{report_id}')
def get_report(report_id:int=Path(ge=1),db:Session=Depends(get_db)):
    """TODO B-06 · get_report() — mentor와 동일한 함수 계약을 완성하세요."""
    # TODO B-06: 경로 report_id로 조회한 응답을 반환하세요. 미존재 ID는 DomainError 404를 유지합니다.
    # 입력·반환형과 예외·상태코드는 요구사항 명세서/API 계약을 참조합니다.
    # 정답 구현 후 아래 예외를 지우고 로직을 작성하세요.
    raise NotImplementedError("B-06 · get_report() TODO 미완성")

@router.put('/reports/{report_id}')
def update_report(body:ReportUpdate,report_id:int=Path(ge=1),db:Session=Depends(get_db)):
    """TODO B-08 · update_report() — mentor와 동일한 함수 계약을 완성하세요."""
    # TODO B-08: 전체 교체 요청을 Service에 전달하고 revision/embedding_updated를 반환하세요.
    # 입력·반환형과 예외·상태코드는 요구사항 명세서/API 계약을 참조합니다.
    # 정답 구현 후 아래 예외를 지우고 로직을 작성하세요.
    raise NotImplementedError("B-08 · update_report() TODO 미완성")

@router.delete('/reports/{report_id}',status_code=204)
def delete_report(report_id:int=Path(ge=1),db:Session=Depends(get_db)):
    """TODO B-09 · delete_report() — mentor와 동일한 함수 계약을 완성하세요."""
    # TODO B-09: 삭제를 실행한 뒤 본문 없는 HTTP 204 Response를 반환하세요.
    # 입력·반환형과 예외·상태코드는 요구사항 명세서/API 계약을 참조합니다.
    # 정답 구현 후 아래 예외를 지우고 로직을 작성하세요.
    raise NotImplementedError("B-09 · delete_report() TODO 미완성")

@router.post('/reports/{report_id}/summarize')
def summarize(report_id:int=Path(ge=1),body:SummaryRequest=Body(default_factory=SummaryRequest),
              db:Session=Depends(get_db)):
    """TODO B-13 · summarize() — mentor와 동일한 함수 계약을 완성하세요."""
    # TODO B-13: 원문 요약 Service를 실제 LLM과 연결하고 결과 JSON을 반환하세요.
    # 입력·반환형과 예외·상태코드는 요구사항 명세서/API 계약을 참조합니다.
    # 정답 구현 후 아래 예외를 지우고 로직을 작성하세요.
    raise NotImplementedError("B-13 · summarize() TODO 미완성")
