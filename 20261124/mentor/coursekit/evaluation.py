"""Day27 기초 비교. 공식 Retrieval 평가 지표 상세는 Day28에 학습합니다."""
from time import perf_counter
from coursekit.documents import docs_to_ids

def present_at_k(ids,gold,k=2):
    if k<=0:raise ValueError('k>0')
    return bool(set(ids[:k]) & set(gold)) if gold else None

def compare_lists(before,after,gold,k=2):
    return {'before':list(before),'after':list(after),
            'gold':list(gold),'k':k,'before_contains_gold':present_at_k(before,gold,k),
            'after_contains_gold':present_at_k(after,gold,k)}

def time_stage(fn,*,cuda=False):
    if cuda:
        import torch
        if torch.cuda.is_available():torch.cuda.synchronize()
    start=perf_counter()
    result=fn()
    if cuda:
        import torch
        if torch.cuda.is_available():torch.cuda.synchronize()
    return result,round((perf_counter()-start)*1000,3)
