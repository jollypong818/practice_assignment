"""실제 OpenAI Responses API 호출. Mock·Fixture 성공을 실 API 성공으로 표시하지 않습니다."""
import json, os, time
from contextvars import ContextVar
from functools import lru_cache
from app.core.config import settings
from app.services.errors import DomainError

_last_usage:ContextVar[dict|None]=ContextVar('llm_usage',default=None)

def get_last_usage()->dict|None:
    return _last_usage.get()

@lru_cache(maxsize=1)
def get_client():
    if not os.getenv('OPENAI_API_KEY'):
        raise DomainError(503,'LLM_UNAVAILABLE','OPENAI_API_KEY가 설정되지 않았습니다.')
    if not settings.llm_model:
        raise DomainError(503,'LLM_UNAVAILABLE','LLM_MODEL이 설정되지 않았습니다.')
    from openai import OpenAI
    return OpenAI(timeout=settings.llm_timeout,max_retries=0)


def call_llm(instructions:str,prompt:str,structured:bool=False,retries:int=0)->str:
    """TODO B-13 · call_llm() — mentor와 동일한 함수 계약을 완성하세요."""
    # TODO B-13: 인증된 OpenAI Responses Client를 호출하고 완료 상태와 output_text를 확인하세요.
    # TODO B-13: API/Timeout 오류는 구조화된 DomainError로 변환합니다.
    # 입력·반환형과 예외·상태코드는 요구사항 명세서/API 계약을 참조합니다.
    # 정답 구현 후 아래 예외를 지우고 로직을 작성하세요.
    raise NotImplementedError("B-13 · call_llm() TODO 미완성")


def summarize(content:str,style:str,max_sentences:int,allow_structured:bool,retries:int=0):
    """TODO B-13 · summarize() — mentor와 동일한 함수 계약을 완성하세요."""
    # TODO B-13: 보고서 원문을 불신 입력으로 두고 brief 요약 지시를 구성해 call_llm 호출. structured는
    # TODO B-13: Intermediate에서만 허용합니다.
    # 입력·반환형과 예외·상태코드는 요구사항 명세서/API 계약을 참조합니다.
    # 정답 구현 후 아래 예외를 지우고 로직을 작성하세요.
    raise NotImplementedError("B-13 · summarize() TODO 미완성")
