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
    return run_agent(db,body.model_dump())
