"""Keyword + Semantic Search Router. not_found는 200이라는 명세를 유지합니다."""
from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.report import SimilarRequest
from app.services.search_service import find_similar

router=APIRouter(prefix='/api/v1/search',tags=['Search'])

@router.post('/similar')
def similar(body:SimilarRequest,db:Session=Depends(get_db)):
    """TODO B-12 · similar() — mentor와 동일한 함수 계약을 완성하세요."""
    # TODO B-12: POST 검색 JSON의 query/category_code/후보 개수를 Hybrid Search Service에
    # TODO B-12: 전달하세요.
    # 입력·반환형과 예외·상태코드는 요구사항 명세서/API 계약을 참조합니다.
    # 정답 구현 후 아래 예외를 지우고 로직을 작성하세요.
    raise NotImplementedError("B-12 · similar() TODO 미완성")
