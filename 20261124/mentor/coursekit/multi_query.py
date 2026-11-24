"""Multi-query 후보 통합: chunk_id 동일성·원 출처·발견 질문을 보존."""
from coursekit.documents import valid_document


def unique_queries(base,additional,max_queries=3):
    if type(max_queries) is not int or not 1<=max_queries<=4:raise ValueError('max_queries 1~4')
    result=[]
    for q in [base,*additional]:
        if not isinstance(q,str):raise ValueError('질문은 문자열이어야 합니다.')
        q=q.strip()
        if q and q not in result:result.append(q)
        if len(result)>=max_queries:break
    return result


def merge_found(results):
    """[(query, [Document...]), ...] -> stable unique Documents with found_by_query list."""
    merged={}
    for query,docs in results:
        for doc in docs:
            valid_document(doc)
            key=doc.metadata['chunk_id']
            if key not in merged:
                clone=doc.model_copy(deep=True) if hasattr(doc,'model_copy') else doc.copy(deep=True)
                clone.metadata['found_by_query']=[query]
                merged[key]=clone
            elif query not in merged[key].metadata['found_by_query']:
                # 같은 ID의 본문이 달라진 경우 데이터 일관성 위반을 숨기지 않습니다.
                if merged[key].page_content!=doc.page_content:
                    raise ValueError(f'같은 chunk_id의 본문 불일치: {key}')
                merged[key].metadata['found_by_query'].append(query)
    return list(merged.values())


def search_multiple(queries, search_fn,*,category,role='learner',candidate_k=5,max_queries=3,partial_ok=False):
    unique=unique_queries(queries[0],queries[1:],max_queries=max_queries)
    results,errors=[],[]
    for query in unique:
        try:
            docs=search_fn(query,category,candidate_k,role)
        except Exception as exc:
            errors.append({'query':query,'error_type':type(exc).__name__})
            if not partial_ok:raise
            continue
        results.append((query,docs))
    return {'queries':unique,'documents':merge_found(results),
            'errors':errors,'query_count':len(unique),'completed_count':len(results)}


# LLM Multi-query 확장: 각 쿼리 후보를 모델에서 생성할 수 있지만 정답/품질은 보장하지 않습니다.
from pydantic import BaseModel, ConfigDict, Field

class MultiQueryPlan(BaseModel):
    model_config=ConfigDict(extra='forbid',strict=True)
    additional_queries:list[str]=Field(max_length=2)

def make_multiquery_chain(model=None):
    from langchain_core.prompts import ChatPromptTemplate
    from coursekit.llm import create_chat_model
    model=create_chat_model() if model is None else model
    prompt=ChatPromptTemplate.from_messages([
        ('system','검색 품질 향상을 위해 원 질문의 의미를 유지하는 검색 표현을 최대 2개 생성하세요. '
                  '날짜·부정·권한·문서 조건을 임의로 만들지 마세요. JSON 스키마를 지키세요.'),
        ('human','검색 질문: {query}')
    ])
    return prompt|model.with_structured_output(MultiQueryPlan,method='json_schema',strict=True)

def generate_queries_live(base,chain=None):
    chain=make_multiquery_chain() if chain is None else chain
    plan=chain.invoke({'query':base})
    if not isinstance(plan,MultiQueryPlan):raise TypeError('MultiQueryPlan Structured Output 필요')
    # 질문이 너무 길거나 비어 있으면 별도 검색하지 않습니다. 
    return [q.strip() for q in plan.additional_queries if isinstance(q,str) and q.strip() and len(q)<=800]
