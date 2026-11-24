"""Cross-Encoder 점수 계산은 sentence-transformers, LangChain은 실행 연결을 담당."""
from functools import lru_cache
import math
from coursekit.config import RERANK_ID,require_cuda
from coursekit.documents import valid_document

@lru_cache(maxsize=1)
def _model():
    from sentence_transformers import CrossEncoder
    return CrossEncoder(RERANK_ID,device=require_cuda())

def live_scorer(pairs,batch_size=4):
    """CUDA 기본; 실제 점수는 확률이 아니라 모델 출력입니다."""
    if not 1<=batch_size<=16:raise ValueError('batch_size: 1~16')
    if not pairs:return []
    import numpy as np
    scores=_model().predict(pairs,batch_size=batch_size,show_progress_bar=False)
    return [float(x) for x in np.asarray(scores).reshape(-1)]


def rerank_documents(query,documents,score_fn,*,top_n=2):
    if type(top_n) is not int or not 1<=top_n<=20:raise ValueError('top_n: 1~20')
    if not query.strip():raise ValueError('rerank query 비어 있음')
    for doc in documents:valid_document(doc)
    if not documents:return []
    pairs=[(query,doc.page_content) for doc in documents]
    scores=list(score_fn(pairs))
    if len(scores)!=len(documents):raise ValueError('CrossEncoder 점수 개수 불일치')
    if any(not math.isfinite(float(s)) for s in scores):raise ValueError('NaN/Inf CrossEncoder 점수')
    scored=[]
    for i,(doc,score) in enumerate(zip(documents,scores)):
        clone=doc.model_copy(deep=True) if hasattr(doc,'model_copy') else doc.copy(deep=True)
        clone.metadata['pre_rank']=i+1
        clone.metadata['rerank_score']=float(score)
        scored.append(clone)
    scored.sort(key=lambda d:(-d.metadata['rerank_score'],d.metadata['pre_rank']))
    for i,doc in enumerate(scored):doc.metadata['post_rank']=i+1
    return scored[:top_n]
