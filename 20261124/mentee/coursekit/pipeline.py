"""Day27 2-step RAG: Rewrite → Retrieve → Rerank → Context → Generation. Stage별 계약."""
from time import perf_counter
from coursekit.documents import context_from_documents,source_index,docs_to_ids
from coursekit.multi_query import unique_queries,search_multiple
from coursekit.llm import offline_answer,validate_generation,NO_ANSWER

class StageError(RuntimeError):
    def __init__(self,stage,code):
        self.stage=stage
        self.code=code
        super().__init__(f'{stage}:{code}')


def create_rag_pipeline(rewrite_fn,search_fn,rank_fn,generation_fn,
                        *,multiquery_fn=None,offline=False):
    """Dependency Injection: mock / real 모델의 실행 경로를 명시적으로 선택합니다."""
    from langchain_core.runnables import RunnableLambda
    def run(name,fn):
        def wrapped(state):
            start=perf_counter()
            try:
                result=fn(state)
            except StageError:raise
            except Exception as exc:
                # Error 원문(DB 접속정보/API 응답 등)은 외부로 노출하지 않습니다.
                raise StageError(name,type(exc).__name__) from exc
            finally:
                state.setdefault('timing_ms',{})[name]=round((perf_counter()-start)*1000,3)
            # 마지막 Generation도 trace에 기록합니다. 부품 내부의 처리 시간 측정입니다.
            if isinstance(result,dict) and 'trace' in result:
                result['trace']['timing_ms']=dict(state['timing_ms'])
            return result
        return RunnableLambda(wrapped)

    def start(req):
        from coursekit.api import RagRequest
        trusted_role=req.get('trusted_role','learner')
        req=RagRequest.model_validate({k:v for k,v in req.items() if k!='trusted_role'}).model_dump()
        # principal role은 사용자 JSON에 넣지 않습니다. 인증된 서버 코드가 지정합니다.
        return dict(req, trusted_role=trusted_role, search_query=req['query'],queries=[], candidates=[],ranked=[],
                    included=[],context='',status='running',timing_ms={},source_mode='offline_fixture' if offline else 'live')

    def rewrite(s):
        if not s['use_rewrite']:return s
        plan=rewrite_fn(s['query'],s['history'])
        if plan.status=='clarification_required':
            s['status']='clarification_required';s['reason']=plan.reason
        else:s['search_query']=plan.search_query
        return s

    def queries(s):
        if s['status']!='running':return s
        additional=multiquery_fn(s['search_query']) if s['use_multiquery'] else []
        s['queries']=unique_queries(s['search_query'],additional,max_queries=3)
        return s

    def retrieve(s):
        if s['status']!='running':return s
        data=search_multiple(s['queries'],search_fn,category=s['category'],
                             role=s['trusted_role'],candidate_k=s['candidate_k'],max_queries=3)
        s['candidates']=data['documents']
        s['candidate_ids']=docs_to_ids(data['documents'])
        s['query_count']=data['query_count']
        return s

    def rerank(s):
        if s['status']!='running':return s
        if s['use_rerank'] and s['candidates']:
            s['ranked']=rank_fn(s['search_query'],s['candidates'],min(len(s['candidates']),20))
        else:s['ranked']=s['candidates'][:]
        s['ranked_ids']=docs_to_ids(s['ranked'])
        return s

    def context(s):
        if s['status']!='running':return s
        s['context'],s['included']=context_from_documents(s['ranked'],context_k=s['context_k'],max_chars=650)
        s['included_ids']=docs_to_ids(s['included'])
        return s

    def generate(s):
        if s['status']=='clarification_required':
            return {'status':'clarification_required','result':{'status':'insufficient_context',
                     'answer':NO_ANSWER,'source_ids':[],
                     'missing_information':s['reason']},'sources':[],'trace':make_trace(s)}
        if not s['context']:
            result={'status':'insufficient_context','answer':NO_ANSWER,'source_ids':[],
                    'missing_information':'현재 검색 범위에 답할 Context가 부족합니다.'}
        elif offline:
            result=offline_answer(s['query'],s['context'],s['included'])
        else:
            query=s['query']+'\n[검색용 독립 질문] '+s['search_query']
            result=validate_generation(generation_fn(query,s['context']),
                                       {d.metadata['citation_id'] for d in s['included']})
        index=source_index(s['included'])
        if not set(result['source_ids']).issubset(index):raise StageError('generation','source_not_in_context')
        sources=[index[cid] for cid in result['source_ids']]
        return {'status':result['status'],'result':result,'sources':sources,'trace':make_trace(s)}

    def make_trace(s):
        # 생성에 쓰인 원본/검색 질문, 실제 Context IDs를 보존합니다. Key/전체 본문은 기록하지 않습니다.
        return {'original_question':s['query'],'search_query':s['search_query'],
                'queries':s['queries'],'candidate_ids':s.get('candidate_ids',[]),
                'ranked_ids':s.get('ranked_ids',[]),'included_ids':s.get('included_ids',[]),
                'query_count':s.get('query_count',0),
                'timing_ms':s.get('timing_ms',{}),'source_mode':s['source_mode']}

    # LCEL의 | 연결은 실행 순서만 준비합니다. invoke 호출에서 실제 Stage를 실행합니다.
    chain=(RunnableLambda(start)
           |run('rewrite',rewrite)
           |run('multiquery',queries)
           |run('retrieval',retrieve)
           |run('rerank',rerank)
           |run('context',context)
           |run('generation',generate))
    return chain
