"""모든 난이도의 공통 실행 골격. 학생이 작성할 과제 함수는 외부에서 주입합니다.

앞 실습의 정답을 강제하지 않고 오늘의 TODO만 실행해도 결과를 확인할 수 있습니다.
--offline은 고정 데이터/고정 점수이며 실제 검색 성능 검증으로 해석하지 않습니다.
"""
from coursekit.io import load_json

CASES=[
 {'id':'F01','ambiguous':True,'gold_in_candidates':False,'gold_in_context':False,
  'valid_source':None,'authorized':True,'current':True,'ready':True},
 {'id':'F02','ambiguous':False,'gold_in_candidates':False,'gold_in_context':False,
  'valid_source':None,'authorized':True,'current':True,'ready':True},
 {'id':'F03','ambiguous':False,'gold_in_candidates':True,'gold_in_context':False,
  'valid_source':None,'authorized':True,'current':True,'ready':True},
 {'id':'F04','ambiguous':False,'gold_in_candidates':True,'gold_in_context':True,
  'valid_source':False,'authorized':True,'current':True,'ready':True},
 {'id':'F05','ambiguous':False,'gold_in_candidates':True,'gold_in_context':True,
  'valid_source':True,'authorized':True,'current':True,'ready':True},
 {'id':'F06','ambiguous':False,'gold_in_candidates':False,'gold_in_context':False,
  'valid_source':None,'authorized':False,'current':True,'ready':True},
 {'id':'F07','ambiguous':False,'gold_in_candidates':False,'gold_in_context':False,
  'valid_source':None,'authorized':True,'current':False,'ready':True},
]

# fns: 앞에서부터 순차적으로 주입받는 TODO 함수들.
def run_01(offline,fns):
    f1,f2,*more=fns
    rows=[]
    for case in CASES:
        stage=f1(case)
        row={'case_id':case['id'],'stage':stage,'improvement':f2(stage)}
        if len(more)>=1:row['reason']=more[0](case,stage)
        if len(more)>=2:row['audit']=more[1](case,row)
        rows.append(row)
    return {'execution_mode':'fixed_diagnostic_cases','rows':rows,
            'note':'일반 검색 알고리즘 또는 실제 LLM 모델을 호출하지 않은 진단 예시'}


def run_02(offline,fns):
    from coursekit.rewrite import rewrite_query
    from coursekit.fixtures import get_question
    f1,f2,*more=fns
    questions=[get_question('Q02'),get_question('Q04'),
               {'id':'Q-ambiguous','question':'그거는 어떻게 해?','category':'시설','history':[]}]
    rows=[]
    for case in questions:
        result=f1(case['question'],case['history'],offline)
        row=f2(case['question'],result)
        if len(more)>=1:row['semantic_guard']=more[0](case['question'],result)
        if len(more)>=2:row['audit']=more[1](case,row)
        rows.append(row)
    return {'execution_mode':'offline_fixture' if offline else 'live_llm_api',
            'rows':rows,'note':'실제 LLM 출력은 비결정적일 수 있습니다. 모호한 요청은 확인 필요로 표시'}


def run_03(offline,fns):
    from coursekit.fixtures import fixture_search,get_question
    from coursekit.live import make_live_search
    f1,f2,*more=fns
    case=get_question('Q01')
    base=case['question']
    if offline:extras=['회의실 예약 철회는 어떻게 하나요?','회의실 예약 취소 조건은?','회의실 사용 후 청소']
    else:
        from coursekit.config import require_cuda
        require_cuda()  # 불필요한 유료 LLM 호출 전에 GPU 환경 확인
        from coursekit.multi_query import generate_queries_live
        extras=generate_queries_live(base)
    queries=f1(base,extras)
    search=fixture_search if offline else make_live_search()
    pairs,errors=[],[]
    for q in queries:
        try:docs=search(q,case['category'],5,'learner')
        except Exception as exc:
            if len(more)<2:raise
            # 심화: 일부 Query가 실패했을 때도 실패 사실을 남깁니다.
            errors.append({'query':q,'error_type':type(exc).__name__})
            continue
        pairs.append((q,docs))
    if not pairs and errors:raise RuntimeError('모든 Multi-query 검색이 실패했습니다.')
    merged=f2(pairs)
    row={'queries':queries,'query_errors':errors,'per_query':[
            {'query':q,'ids':[d.metadata['chunk_id'] for d in docs]} for q,docs in pairs],
         'merged_ids':[d.metadata['chunk_id'] for d in merged],
         'found_by_query':{d.metadata['chunk_id']:d.metadata.get('found_by_query',[]) for d in merged}}
    if len(more)>=1:row['query_checks']=more[0](queries)
    if len(more)>=2:row['merged_check']=more[1](pairs,merged)
    return {'execution_mode':'offline_fixture' if offline else 'live_e5_cuda_postgresql','row':row}


def run_04(offline,fns):
    from coursekit.fixtures import fixture_search,get_question
    from coursekit.live import make_live_search
    from langchain_core.runnables import RunnableLambda
    f1,f2,*more=fns
    case=get_question('Q01')
    payload=f1(case)
    search=fixture_search if offline else make_live_search()
    retriever=RunnableLambda(lambda req:search(req['query'],req['category'],req['candidate_k'],'learner'))
    docs=f2(retriever,payload)
    row={'candidate_ids':[d.metadata['chunk_id'] for d in docs],
         'candidate_k':payload['candidate_k'],'context_k':payload['context_k'],
         'category':payload['category']}
    if len(more)>=1:row['metadata_ok']=more[0](docs,payload)
    if len(more)>=2:row['policy_check']=more[1](docs,payload)
    return {'execution_mode':'offline_fixture' if offline else 'live_e5_cuda_postgresql','row':row}


def run_05(offline,fns):
    from coursekit.fixtures import fixture_search,get_question,fixed_rank_scores
    from coursekit.live import make_live_search
    from coursekit.reranking import live_scorer
    f1,f2,*more=fns
    case=get_question('Q01')
    # 고정 순위 시연: 의도적으로 정답 청크가 초기 Top-2 밖에 있는 Fixture.
    search=(lambda q,c,k,role:fixture_search(q,c,k,role,question_id=case['id'])) if offline else make_live_search()
    docs=search(case['question'],case['category'],5,'learner')
    pairs=f1(case['question'],docs)
    scorer=(lambda items:fixed_rank_scores(case['question'],docs)) if offline else live_scorer
    ranked=f2(case['question'],docs,scorer)
    row={'pairs':pairs[:2], 'before_ids':[d.metadata['chunk_id'] for d in docs],
         'after_ids':[d.metadata['chunk_id'] for d in ranked],
         'rerank_scores':[d.metadata.get('rerank_score') for d in ranked]}
    if len(more)>=1:row['score_checks']=more[0](ranked)
    if len(more)>=2:row['audit']=more[1](docs,ranked)
    return {'execution_mode':'offline_fixture' if offline else 'live_e5_cuda_postgresql_crossencoder',
            'row':row,'note':'고정 점수는 실제 CrossEncoder 모델 점수가 아닙니다.'}


def run_06(offline,fns):
    from coursekit.fixtures import get_question
    from coursekit.runtime import create_dependencies
    f1,f2,*more=fns
    case=get_question('Q02')
    req=f1(case)
    dependencies=create_dependencies(offline)
    chain=f2(dependencies,offline)
    result=chain.invoke(req)
    row={'status':result['status'],'result':result['result'],
         'sources':result['sources'],'trace':result['trace']}
    if len(more)>=1:row['trace_check']=more[0](result)
    if len(more)>=2:row['audit']=more[1](result)
    return {'execution_mode':'offline_fixture' if offline else 'live_e5_cuda_postgresql_llm',
            'row':row}


def run_07(offline,fns):
    from coursekit.fixtures import fixture_search,get_question,fixed_rank_scores
    from coursekit.live import make_live_search
    from coursekit.reranking import rerank_documents,live_scorer
    from coursekit.evaluation import time_stage
    f1,f2,*more=fns
    case=get_question('Q01')
    search=(lambda q,c,k,role:fixture_search(q,c,k,role,question_id=case['id'])) if offline else make_live_search()
    docs,search_ms=time_stage(lambda:search(case['question'],case['category'],5,'learner'),cuda=False)
    scorer=(lambda pairs:fixed_rank_scores(case['question'],docs)) if offline else live_scorer
    ranked,rerank_ms=time_stage(lambda:rerank_documents(case['question'],docs,scorer,top_n=5),cuda=not offline)
    before=[d.metadata['chunk_id'] for d in docs];after=[d.metadata['chunk_id'] for d in ranked]
    report=f1(before,after,case['gold_chunk_ids'])
    row={'comparison':report,'interpretation':f2(report),'search_ms':search_ms,'rerank_ms':rerank_ms}
    if len(more)>=1:row['controlled_conditions']=more[0](case,docs,ranked)
    if len(more)>=2:row['audit']=more[1](row,offline)
    return {'execution_mode':'offline_fixture' if offline else 'live_e5_cuda_postgresql_crossencoder',
            'row':row,'note':'관련 문서 포함 여부는 평가 기초 비교이며, 상세 평가는 Day28에서 학습.'}


def run_08(offline,fns):
    from fastapi.testclient import TestClient
    from coursekit.fixtures import get_question
    f1,f2,*more=fns
    chain=f1(offline)
    app=f2(chain)
    tests=[get_question('Q01'),get_question('Q06')]
    rows=[]
    with TestClient(app) as client:
        for case in tests:
            payload={'query':case['question'],'history':case['history'],'category':case['category'],
                     'use_rewrite':False if case['id']=='Q06' else True,
                     'candidate_k':5,'context_k':2,'use_rerank':True,'use_multiquery':False}
            response=client.post('/api/v1/rag/answer',json=payload)
            body=response.json()
            row={'question_id':case['id'],'http_status':response.status_code,'body':body}
            if len(more)>=1:row['response_check']=more[0](response)
            if len(more)>=2:row['audit']=more[1](payload,response)
            rows.append(row)
        # 잘못된 k는 서비스 호출 전에 422가 되어야 합니다.
        invalid={**payload,'candidate_k':0}
        response=client.post('/api/v1/rag/answer',json=invalid)
        row={'question_id':'INVALID_K','http_status':response.status_code,'body':response.json()}
        if len(more)>=1:row['response_check']=more[0](response)
        if len(more)>=2:row['audit']=more[1](invalid,response)
        rows.append(row)
    # 강제 실패는 고정 예제로만 실행합니다. 실제 LLM 장애를 일으키지 않습니다.
    if offline:
        from langchain_core.runnables import RunnableLambda
        from coursekit.pipeline import StageError
        def broken(_):raise StageError('rerank','model_unavailable_fixture')
        error_app=f2(RunnableLambda(broken))
        with TestClient(error_app) as client:
            error_payload={'query':'회의실 예약 취소 방법?','category':'시설'}
            response=client.post('/api/v1/rag/answer',json=error_payload)
            row={'question_id':'FIXED_RERANK_ERROR','http_status':response.status_code,'body':response.json()}
            if len(more)>=1:row['response_check']=more[0](response)
            if len(more)>=2:row['audit']=more[1](error_payload,response)
            rows.append(row)
    return {'execution_mode':'offline_fixture' if offline else 'live_e5_cuda_postgresql_llm',
            'rows':rows,'note':'FastAPI 200·422·502 구분. 502는 고정 오류 Fixture만 사용합니다.'}

STAGE_RUNNERS={1:run_01,2:run_02,3:run_03,4:run_04,5:run_05,6:run_06,7:run_07,8:run_08}
