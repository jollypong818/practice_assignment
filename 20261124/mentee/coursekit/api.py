"""FastAPI 계약. role은 사용자 입력에서 받지 않으며 서버의 인증 결과만 신뢰합니다."""
from pydantic import BaseModel,ConfigDict,Field,field_validator
from typing import Literal
from fastapi import FastAPI,HTTPException,Depends
from coursekit.pipeline import StageError

class Turn(BaseModel):
    model_config=ConfigDict(extra='forbid',strict=True)
    role:Literal['user','assistant']
    content:str=Field(min_length=1,max_length=800)

class RagRequest(BaseModel):
    model_config=ConfigDict(extra='forbid',strict=True)
    query:str=Field(min_length=1,max_length=800)
    history:list[Turn]=Field(default_factory=list,max_length=8)
    category:Literal['학사','시설','지원']='시설'
    candidate_k:int=Field(default=5,ge=1,le=20)
    context_k:int=Field(default=2,ge=1,le=3)
    use_rewrite:bool=True
    use_multiquery:bool=False
    use_rerank:bool=True
    @field_validator('query')
    @classmethod
    def nonblank(cls,v):
        v=v.strip()
        if not v:raise ValueError('빈 질문')
        return v

    model_config=ConfigDict(extra='forbid',strict=True)

def create_app(chain,*,trusted_role='learner'):
    if trusted_role not in ('learner','staff'):raise ValueError('서버 인증 역할이 유효하지 않습니다.')
    app=FastAPI(title='Day27 LangChain RAG',version='0.1.0')
    # 실무에서는 인증 Middleware/Dependency에서 principal role을 받아야 합니다.
    # 본 수업은 learner로 고정합니다. 공개 요청 JSON에 role 필드가 없습니다.
    @app.post('/api/v1/rag/answer')
    def answer(req:RagRequest):
        body=req.model_dump()
        body['trusted_role']=trusted_role
        try:return chain.invoke(body)
        except StageError as exc:
            raise HTTPException(status_code=502,detail={'stage':exc.stage,'code':exc.code}) from exc
    return app
