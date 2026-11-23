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
    if body.get('agent_mode')=='tool_calling':
        raise DomainError(422,'VALIDATION_ERROR','Tool Calling은 Advanced 기능입니다.')
    action=body.get('action'); rid=body.get('report_id');query=(body.get('query') or '').strip()
    if action=='get_report':
        if not rid:raise DomainError(422,'VALIDATION_ERROR','report_id가 필요합니다.')
        data=report_service.get_report(db,rid);tools=['get_report']
    elif action=='find_report':
        if not query:raise DomainError(422,'VALIDATION_ERROR','query가 필요합니다.')
        data=search_service.find_similar(db,query);tools=['find_similar_report']
    elif action=='summarize_report':
        if not rid:raise DomainError(422,'VALIDATION_ERROR','report_id가 필요합니다.')
        data=summarize(db,rid);tools=['summarize_report']
    elif action=='search_and_summarize' and at_least('intermediate'):
        if not query:raise DomainError(422,'VALIDATION_ERROR','query가 필요합니다.')
        found=search_service.find_similar(db,query);tools=['find_similar_report']
        if found['status']=='found':
            data={'search':found,'summary':summarize(db,found['best_match']['report_id'])}
            tools.append('summarize_report')
        else:
            # 불필요한 유료 LLM API 호출을 하지 않습니다.
            data={'search':found,'summary':None}
    else:
        raise DomainError(422,'VALIDATION_ERROR','지원하지 않는 Agent action입니다.')
    result={'action':action,'status':'completed','tool_calls':tools,'data':data}
    if at_least('advanced'):record_run(action,'completed',len(tools))
    return result
