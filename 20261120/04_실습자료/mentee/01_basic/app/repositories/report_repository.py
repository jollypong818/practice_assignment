"""Repository: 영속 저장·조회만 담당. 외부 API/Embedding 요청은 여기서 하지 않습니다."""
from datetime import date,datetime,timezone
from typing import Any
from sqlalchemy import select,text
from sqlalchemy.orm import Session
from app.models.report import (ReportCategory,Report,ReportEmbedding,DETAIL_MODELS,DETAIL_FIELDS,
                               PromptVersion)
from app.services.errors import DomainError


def category_for_code(db:Session,code:str)->ReportCategory:
    """TODO B-05 · category_for_code() — mentor와 동일한 함수 계약을 완성하세요."""
    # TODO B-05: code에 대응하는 ReportCategory 1건을 조회하고 없으면 422 에러를 발생시키세요.
    # 입력·반환형과 예외·상태코드는 요구사항 명세서/API 계약을 참조합니다.
    # 정답 구현 후 아래 예외를 지우고 로직을 작성하세요.
    raise NotImplementedError("B-05 · category_for_code() TODO 미완성")

def get_report_and_detail(db:Session,rid:int,lock:bool=False):
    """TODO B-06 · get_report_and_detail() — mentor와 동일한 함수 계약을 완성하세요."""
    # TODO B-06: 공통 Report + Category + 일치하는 상세 모델을 조회하세요. 잠금이 필요하면 with_for_update를
    # TODO B-06: 적용하고 없는 ID는 404.
    # 입력·반환형과 예외·상태코드는 요구사항 명세서/API 계약을 참조합니다.
    # 정답 구현 후 아래 예외를 지우고 로직을 작성하세요.
    raise NotImplementedError("B-06 · get_report_and_detail() TODO 미완성")

def plain_value(obj:Any):
    """TODO B-06 · plain_value() — mentor와 동일한 함수 계약을 완성하세요."""
    # TODO B-06: datetime은 UTC로 변환한 ISO 8601 문자열(Z), date는 YYYY-MM-DD로 반환하세요.
    # 시간대 없는 datetime은 DATA_INTEGRITY_ERROR(500)로 구분하고 그 외 값은 그대로 반환합니다.
    # 입력·반환형과 예외·상태코드는 요구사항 명세서/API 계약을 참조합니다.
    # 정답 구현 후 아래 예외를 지우고 로직을 작성하세요.
    raise NotImplementedError("B-06 · plain_value() TODO 미완성")

def serialize_report(report:Report,category:ReportCategory,detail)->dict:
    """TODO B-06 · serialize_report() — mentor와 동일한 함수 계약을 완성하세요."""
    # TODO B-06: report/category/detail을 API-03의 단일 응답 형식으로 묶으세요.
    # TODO B-06: title/content/author는 상세 테이블에서 가져오세요.
    # created_at/updated_at와 details의 시각도 plain_value()로 UTC 직렬화하세요.
    # 입력·반환형과 예외·상태코드는 요구사항 명세서/API 계약을 참조합니다.
    # 정답 구현 후 아래 예외를 지우고 로직을 작성하세요.
    raise NotImplementedError("B-06 · serialize_report() TODO 미완성")

def read_report(db:Session,rid:int)->dict:
    """TODO B-06 · read_report() — mentor와 동일한 함수 계약을 완성하세요."""
    # TODO B-06: get_report_and_detail과 serialize_report를 연결해 단일 보고서를 반환하세요.
    # 입력·반환형과 예외·상태코드는 요구사항 명세서/API 계약을 참조합니다.
    # 정답 구현 후 아래 예외를 지우고 로직을 작성하세요.
    raise NotImplementedError("B-06 · read_report() TODO 미완성")


def list_reports(db:Session, title:str|None,limit:int,offset:int,
                 category_code:str|None=None,updated_after:datetime|None=None)->dict:
    """TODO B-07 · list_reports() — mentor와 동일한 함수 계약을 완성하세요."""
    # TODO B-07: report_read_view를 이용해 6종 통합 제목 조회·정렬·페이지/total을 반환하세요. SQL 값은 바인딩하세요.
    # 입력·반환형과 예외·상태코드는 요구사항 명세서/API 계약을 참조합니다.
    # 정답 구현 후 아래 예외를 지우고 로직을 작성하세요.
    raise NotImplementedError("B-07 · list_reports() TODO 미완성")
