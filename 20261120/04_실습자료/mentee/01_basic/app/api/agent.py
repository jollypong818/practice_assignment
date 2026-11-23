"""Agent Router. 수정/삭제는 Tool Calling에 노출하지 않습니다."""
from fastapi import APIRouter,Depends,Query
from sqlalchemy.orm import Session
from typing import Literal
from app.db.session import get_db
from app.schemas.report import AgentRequest
from app.services.agent_service import run_agent

router=APIRouter(prefix='/api/v1/agent',tags=['Agent'])

@router.post('/run')
def run(body:AgentRequest,db:Session=Depends(get_db)):
    """TODO B-14 · run() — mentor와 동일한 함수 계약을 완성하세요."""
    # TODO B-14: 명시적 action과 필요한 report_id 또는 query를 확인하는 Agent Service를 호출하세요.
    # 입력·반환형과 예외·상태코드는 요구사항 명세서/API 계약을 참조합니다.
    # 정답 구현 후 아래 예외를 지우고 로직을 작성하세요.
    raise NotImplementedError("B-14 · run() TODO 미완성")
