"""Agent Router. 수정/삭제는 Tool Calling에 노출하지 않습니다."""
from fastapi import APIRouter,Depends,Query
from sqlalchemy.orm import Session
from typing import Literal
from app.db.session import get_db
from app.schemas.report import AgentRequest
from app.services.agent_service import run_agent,list_runs

router=APIRouter(prefix='/api/v1/agent',tags=['Agent'])

@router.post('/run')
def run(body:AgentRequest,db:Session=Depends(get_db)):
    return run_agent(db,body.model_dump())

@router.get('/runs')
def runs(limit:int=Query(20,ge=1,le=100),offset:int=Query(0,ge=0),
         status:Literal['completed','failed']|None=None):
    return list_runs(limit,offset,status)
