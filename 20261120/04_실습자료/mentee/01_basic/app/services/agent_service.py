"""Agent Service: Basic = 명시적 Action Router, Advanced = 허용목록 Tool Calling."""
from collections import deque
from datetime import datetime,timezone
import json,uuid
from sqlalchemy.orm import Session
from app.core.config import at_least,settings
from app.repositories import report_repository as repo
from app.services import report_service,search_service
from app.services.errors import DomainError
from app.integrations.llm_client import get_client

# 요구사항 A-08: 별도 테이블 없이 제한된 프로세스 메모리에 보관. 재시작 시 사라집니다.
RUNS=deque(maxlen=100)


def record_run(action:str,status:str,tool_calls:int):
    RUNS.appendleft({'run_id':f'run-{uuid.uuid4().hex[:8]}','action':action,
                     'status':status,'tool_calls':tool_calls,
                     'created_at':datetime.now(timezone.utc).isoformat()})


def summarize(db:Session,rid:int):
    return report_service.summarize_report(db,rid,'brief',3)


def run_agent(db:Session,body:dict)->dict:
    """TODO B-14 · run_agent() — mentor와 동일한 함수 계약을 완성하세요."""
    # TODO B-14: get_report/find_report/summarize_report 명시적 action을 허용하고 해당 도구만
    # TODO B-14: 호출하세요. 필요한 인자가 없으면 422, Tool Calling은 Basic 범위에서 차단.
    # 입력·반환형과 예외·상태코드는 요구사항 명세서/API 계약을 참조합니다.
    # 정답 구현 후 아래 예외를 지우고 로직을 작성하세요.
    raise NotImplementedError("B-14 · run_agent() TODO 미완성")
