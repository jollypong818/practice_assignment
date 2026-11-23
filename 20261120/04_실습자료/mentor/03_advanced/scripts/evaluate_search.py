"""A-06: 실제 DB·E5 기반 Recall@5와 Hybrid@1 오탐/누락 평가.
실행: python scripts/evaluate_search.py
평가셋은 학습용 수동 관련 ID이며, 자동 생성된 모델 정답이 아닙니다.
"""
from pathlib import Path
import sys,csv,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from sqlalchemy import select
from app.db.session import get_session_factory
from app.core.config import settings
from app.models.report import Report,ReportEmbedding
from app.services.search_service import find_similar
from app.integrations.embedding_client import encode


def evaluate():
    cases=json.loads((ROOT/'tests/evaluation_cases.json').read_text(encoding='utf-8'))
    rows=[]
    with get_session_factory()() as db:
        for case in cases:
            query=case['query']; relevant=set(case['relevant_ids'])
            result=find_similar(db,query)
            best=result.get('best_match') or {}
            picked=best.get('report_id')
            vec=encode([query],kind='query')[0]
            expr=ReportEmbedding.embedding.cosine_distance(vec)
            topk=db.scalars(select(ReportEmbedding.report_id)
                .join(Report,Report.report_id==ReportEmbedding.report_id)
                .where(Report.index_status=='ready',ReportEmbedding.indexed_revision==Report.revision,
                       ReportEmbedding.model_name==settings.embedding_model)
                .order_by(expr,ReportEmbedding.report_id).limit(5)).all()
            hits=len(relevant.intersection(set(topk)))
            rows.append({'query':query,'relevant_ids':sorted(relevant),
              'picked_id':picked,'semantic_top5':list(topk),
              'recall_at_5':round(hits/len(relevant),3) if relevant else None,
              'hybrid_top1_correct':(picked in relevant) if relevant else (picked is None),
              # 다른 ID를 고르면 오탐이면서 정답을 놓친 사례로 기록합니다.
              'false_positive':bool(picked is not None and picked not in relevant),
              'false_negative':bool(relevant and picked not in relevant),
              'threshold':settings.search_min_similarity,
              'keyword_score':best.get('keyword_score'),
              'cosine_similarity':best.get('cosine_similarity'),
              'selection_reason':best.get('selection_reason','not_found')})
    output=ROOT/'outputs';output.mkdir(exist_ok=True)
    path=output/'search_evaluation.json'
    path.write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    csv_path=output/'search_evaluation.csv'
    fields=['query','relevant_ids','picked_id','semantic_top5','recall_at_5',
            'hybrid_top1_correct','false_positive','false_negative','threshold',
            'keyword_score','cosine_similarity','selection_reason']
    # Windows Excel에서도 한글을 읽기 쉽도록 UTF-8 BOM을 사용합니다.
    with csv_path.open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader()
        for row in rows:
            writer.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,list) else v
                             for k,v in row.items()})
    positive=[r for r in rows if r['recall_at_5'] is not None]
    avg=sum(r['recall_at_5'] for r in positive)/len(positive) if positive else 0
    print(f'평가 {len(rows)}개 · Mean Semantic Recall@5={avg:.3f} · Hybrid top1 성공 {sum(r["hybrid_top1_correct"] for r in rows)}/{len(rows)}')
    print('결과:',path,csv_path)
    print('주의: 검색 임계값과 학습 모델에 따라 점수는 달라집니다. 실패 사례를 사람이 읽어 해석하세요.')

if __name__=='__main__':evaluate()
