"""GPU/DB/LLM은 --offline이 아닌 명시적인 실제 실행 경로에서만 준비합니다."""
from coursekit.config import require_cuda
from coursekit.pipeline import create_rag_pipeline
from coursekit.reranking import rerank_documents


def create_dependencies(offline=False):
    if offline:
        from coursekit.fixtures import fixture_search,rewrite_fixture,fixed_rank_scores
        from coursekit.rewrite import rewrite_query
        def search(q,cat,k,role):return fixture_search(q,cat,k,role)
        def rewrite(q,history):return rewrite_query(q,history,offline=True)
        def rerank(q,docs,k):
            return rerank_documents(q,docs,lambda pairs:fixed_rank_scores(q,docs),top_n=k)
        def generate(q,ctx):raise AssertionError('offline은 실제 LLM을 호출하지 않습니다.')
        return rewrite,search,rerank,generate
    require_cuda()  # 의도하지 않은 CPU fallback 방지
    from coursekit.live import make_live_search
    from coursekit.llm import create_generation
    from coursekit.rewrite import make_rewrite_chain,rewrite_query
    from coursekit.reranking import live_scorer
    search=make_live_search()
    rewrite_chain=make_rewrite_chain()
    generation=create_generation()
    def rewrite(q,h):return rewrite_query(q,h,chain=rewrite_chain)
    def rerank(q,docs,k):return rerank_documents(q,docs,lambda pairs:live_scorer(pairs),top_n=k)
    return rewrite,search,rerank,lambda q,ctx:generation.invoke({'question':q,'context':ctx})


def create_demo_chain(offline=False,multiquery_fn=None):
    if multiquery_fn is None:
        if offline:
            multiquery_fn=lambda query: ['회의실 예약 철회는 어떻게 하나요?', '회의실 예약 취소 조건은?']
        else:
            from coursekit.multi_query import generate_queries_live
            multiquery_fn=generate_queries_live
    return create_rag_pipeline(*create_dependencies(offline),
                               multiquery_fn=multiquery_fn,offline=offline)
