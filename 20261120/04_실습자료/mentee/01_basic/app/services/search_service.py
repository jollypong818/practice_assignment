"""Hybrid Search: keyword 후보를 먼저 검토하고, 없다면 의미 검색의 임계값을 적용합니다."""
from sqlalchemy import select,text
from sqlalchemy.orm import Session
from app.models.report import Report,ReportEmbedding,ReportCategory
from app.core.config import settings,at_least
from app.integrations import embedding_client as emb
from app.services.errors import DomainError


def safe_like(s:str)->str:
    return s.replace('\\','\\\\').replace('%','\\%').replace('_','\\_')


def find_similar(db:Session,query:str,category_code:str|None=None,
                 keyword_limit:int=20,semantic_limit:int=20)->dict:
    """TODO B-12 · find_similar() — mentor와 동일한 함수 계약을 완성하세요."""
    # TODO B-12: 제목·개요·본문 Keyword 검색, ready·revision 일치 E5 Semantic 검색을 결합하세요. 1건 또는
    # TODO B-12: not_found; 필터와 0~1 유사도 반환 규칙을 준수하세요.
    # 입력·반환형과 예외·상태코드는 요구사항 명세서/API 계약을 참조합니다.
    # 정답 구현 후 아래 예외를 지우고 로직을 작성하세요.
    raise NotImplementedError("B-12 · find_similar() TODO 미완성")
