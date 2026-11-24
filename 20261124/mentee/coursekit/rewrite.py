"""Query Rewrite: 원문 질문 보존, 모호 질문은 확인 요청, LLM 오류는 숨기지 않습니다."""
from pydantic import BaseModel, ConfigDict, Field
from typing import Literal
from coursekit.fixtures import rewrite_fixture

class RewriteResult(BaseModel):
    model_config=ConfigDict(extra='forbid',strict=True)
    status: Literal['ready','clarification_required']
    search_query: str=Field(max_length=800)
    reason: str=Field(max_length=200)

RULES=('당신은 검색 질문 Rewrite 구성요소입니다. 마지막 질문을 검색 가능한 독립 질문으로 바꾸세요. '
       'History에서 명확한 사실만 복원하고 조건·부정·날짜를 추측하지 마세요. '
       '대상이 불분명하면 status=clarification_required, search_query는 빈 문자열로 반환하세요. '
       '그렇지 않으면 status=ready, search_query에 독립 질문을 쓰세요.')

def make_rewrite_chain(model=None):
    from langchain_core.prompts import ChatPromptTemplate
    from coursekit.llm import create_chat_model
    model=create_chat_model() if model is None else model
    prompt=ChatPromptTemplate.from_messages([('system',RULES),('human','History:\n{history}\n\n최종 질문: {original_question}')])
    return prompt | model.with_structured_output(RewriteResult,method='json_schema',strict=True)


def rewrite_query(original_question,history,*,offline=False,chain=None):
    if not original_question.strip():raise ValueError('질문은 비어 있을 수 없습니다.')
    if offline:
        search=rewrite_fixture(original_question,history)
        return RewriteResult(status='ready',search_query=search,reason='교육용 고정 Rewrite') if search else RewriteResult(status='clarification_required',search_query='',reason='대화에서 대상을 확인할 수 없습니다.')
    chain=make_rewrite_chain() if chain is None else chain
    response=chain.invoke({'original_question':original_question,'history':str(history)})
    if not isinstance(response,RewriteResult):raise TypeError('LLM Structured Output 타입 불일치')
    if response.status=='ready' and not response.search_query.strip():raise ValueError('ready인데 검색 질문이 비었습니다.')
    if response.status=='clarification_required' and response.search_query:raise ValueError('확인 요청에는 검색 질문을 생성하지 않습니다.')
    return response
