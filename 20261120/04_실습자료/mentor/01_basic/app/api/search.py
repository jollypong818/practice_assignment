"""Keyword + Semantic Search Router. not_found는 200이라는 명세를 유지합니다."""
from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.report import SimilarRequest
from app.services.search_service import find_similar

router=APIRouter(prefix='/api/v1/search',tags=['Search'])

@router.post('/similar')
def similar(body:SimilarRequest,db:Session=Depends(get_db)):
    return find_similar(db,body.query,body.category_code,body.keyword_limit,body.semantic_limit)
