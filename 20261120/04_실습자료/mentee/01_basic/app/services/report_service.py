"""Report Service: 6종 보고서 공통 CRUD/버전/동기화. Repository는 DB, Service는 업무 규칙."""
from datetime import datetime,date,timezone
from sqlalchemy import select,func
from sqlalchemy.orm import Session
from app.core.config import settings,at_least
from app.models.report import (Report,ReportCategory,ReportEmbedding,PromptVersion,
                               DETAIL_MODELS, DETAIL_FIELDS, PromptReport)
from app.repositories import report_repository as repo
from app.integrations import embedding_client as emb
from app.integrations import llm_client
from app.services.errors import DomainError
from app.schemas.report import ReportCreate,ReportUpdate,PromptVersionCreate,DETAIL_SCHEMAS
from pydantic import ValidationError

INPUT_FIELDS={
    'EXPERIMENT':{'experiment_date','hypothesis','result_summary'},
    'DAILY_WORK':{'work_date','progress','blockers'},
    'RESEARCH_PLAN':{'research_goal','methodology','target_date'},
    'DATA_PROCESSING':{'dataset_name','processing_steps','quality_notes'},
    'PROMPT':{'purpose','prompt_text'},
    'MEETING':{'meeting_at','attendees','decisions'},
}
OPTIONAL={'DAILY_WORK':{'blockers'},'DATA_PROCESSING':{'quality_notes'}}
DATE_FIELDS={'experiment_date','work_date','target_date'}
TIME_FIELDS={'meeting_at'}


def validate_details(code:str,details:dict,content:str|None=None)->dict:
    """TODO B-05 · validate_details() — mentor와 동일한 함수 계약을 완성하세요."""
    # TODO B-05: 6개 카테고리의 details 필수·선택 필드 및 날짜·시각·공백을 검증하고 정확한 자료형으로 변환하세요. Prompt는
    # TODO B-05: content==prompt_text 검증.
    # 입력·반환형과 예외·상태코드는 요구사항 명세서/API 계약을 참조합니다.
    # 정답 구현 후 아래 예외를 지우고 로직을 작성하세요.
    raise NotImplementedError("B-05 · validate_details() TODO 미완성")


def encode_overview(overview:str)->list[float]:
    """TODO B-10 · encode_overview() — mentor와 동일한 함수 계약을 완성하세요."""
    # TODO B-10: Embedding Client로 passage 개요 1건을 E5-small 384차원 벡터로 생성하고 실패 시 503으로
    # TODO B-10: 구분하세요.
    # 입력·반환형과 예외·상태코드는 요구사항 명세서/API 계약을 참조합니다.
    # 정답 구현 후 아래 예외를 지우고 로직을 작성하세요.
    raise NotImplementedError("B-10 · encode_overview() TODO 미완성")


def categories(db:Session)->dict:
    """TODO B-04 · categories() — mentor와 동일한 함수 계약을 완성하세요."""
    # TODO B-04: report_categories를 PK 오름차순으로 읽어 category_id/code/name/description의
    # TODO B-04: items 리스트를 반환하세요.
    # 입력·반환형과 예외·상태코드는 요구사항 명세서/API 계약을 참조합니다.
    # 정답 구현 후 아래 예외를 지우고 로직을 작성하세요.
    raise NotImplementedError("B-04 · categories() TODO 미완성")


def create_report(db:Session,data:ReportCreate)->dict:
    """TODO B-05 · create_report() — mentor와 동일한 함수 계약을 완성하세요."""
    # TODO B-05: details 검증과 벡터 생성을 먼저 수행하고 Transaction 안에서 reports+해당
    # TODO B-05: Detail+Embedding 저장. Prompt이면 PromptVersion v1도 생성하세요. 오류 시 rollback.
    # 선행 작업: embedding_client.encode()와 encode_overview()를 먼저 완성하세요.
    # 입력·반환형과 예외·상태코드는 요구사항 명세서/API 계약을 참조합니다.
    # 정답 구현 후 아래 예외를 지우고 로직을 작성하세요.
    raise NotImplementedError("B-05 · create_report() TODO 미완성")


def get_report(db:Session,rid:int)->dict:
    """TODO B-06 · get_report() — mentor와 동일한 함수 계약을 완성하세요."""
    # TODO B-06: Repository에서 공통 보고서와 올바른 상세 행을 가져와 API JSON으로 반환하세요.
    # 입력·반환형과 예외·상태코드는 요구사항 명세서/API 계약을 참조합니다.
    # 정답 구현 후 아래 예외를 지우고 로직을 작성하세요.
    raise NotImplementedError("B-06 · get_report() TODO 미완성")


def list_reports(db:Session,title:str|None,limit:int,offset:int,
                 category_code:str|None=None,updated_after:datetime|None=None):
    """TODO B-07 · list_reports() — mentor와 동일한 함수 계약을 완성하세요."""
    # TODO B-07: Repository의 title 필터·최신 수정일 정렬·limit/offset 페이징을 호출하세요.
    # 입력·반환형과 예외·상태코드는 요구사항 명세서/API 계약을 참조합니다.
    # 정답 구현 후 아래 예외를 지우고 로직을 작성하세요.
    raise NotImplementedError("B-07 · list_reports() TODO 미완성")


def update_report(db:Session,rid:int,data:ReportUpdate)->dict:
    """TODO B-08 · update_report() — mentor와 동일한 함수 계약을 완성하세요."""
    # TODO B-08: 상세 속성·revision·update_at을 수정하세요. 개요가 바뀌면 새 벡터가 필요합니다.
    # 같은 개요도 ready·현재 모델·개요 해시·색인 revision이 모두 맞을 때만 기존 벡터를 재사용합니다.
    # 조건이 맞지 않으면 다시 생성하고, 잠금을 얻은 뒤 보고서/벡터 상태를 다시 확인하세요.
    # TODO B-08: read/modify 충돌과 Transaction 실패를 처리하세요.
    # 입력·반환형과 예외·상태코드는 요구사항 명세서/API 계약을 참조합니다.
    # 정답 구현 후 아래 예외를 지우고 로직을 작성하세요.
    raise NotImplementedError("B-08 · update_report() TODO 미완성")


def delete_report(db:Session,rid:int)->None:
    """TODO B-09 · delete_report() — mentor와 동일한 함수 계약을 완성하세요."""
    # TODO B-09: reports에서 보고서를 제거하고 FK CASCADE로 상세·Vector·버전을 함께 삭제하세요. 없는 ID면 404.
    # 입력·반환형과 예외·상태코드는 요구사항 명세서/API 계약을 참조합니다.
    # 정답 구현 후 아래 예외를 지우고 로직을 작성하세요.
    raise NotImplementedError("B-09 · delete_report() TODO 미완성")


def summarize_report(db:Session,rid:int,style:str='brief',max_sentences:int=3)->dict:
    """TODO B-13 · summarize_report() — mentor와 동일한 함수 계약을 완성하세요."""
    # TODO B-13: RDB의 상세 content를 조회해 실제 LLM Client를 호출하고
    # TODO B-13: report_id/source_revision/summary/model/status를 반환하세요.
    # 입력·반환형과 예외·상태코드는 요구사항 명세서/API 계약을 참조합니다.
    # 정답 구현 후 아래 예외를 지우고 로직을 작성하세요.
    raise NotImplementedError("B-13 · summarize_report() TODO 미완성")

