"""Hybrid Search: keyword 후보를 먼저 검토하고, 없다면 의미 검색의 임계값을 적용합니다."""
from sqlalchemy import select,text
from sqlalchemy.orm import Session
from app.models.report import Report,ReportEmbedding,ReportCategory
from app.core.config import settings,at_least
from app.integrations import embedding_client as emb
from app.services.errors import DomainError


def safe_like(s:str)->str:
    return s.replace('\\','\\\\').replace('%','\\%').replace('_','\\_')


def find_similar(db:Session,query:str,category_code:str|None=None,
                 keyword_limit:int=20,semantic_limit:int=20)->dict:
    if not query.strip():raise DomainError(422,'VALIDATION_ERROR','검색어는 필수입니다.')
    query=query.strip()
    if category_code is not None:
        existing=db.scalar(select(ReportCategory.category_id).where(ReportCategory.code==category_code))
        if existing is None:raise DomainError(422,'VALIDATION_ERROR','유효하지 않은 카테고리입니다.')
    try:
        qvec=emb.encode([query],kind='query')[0]  # 실제 모델 필요. 더미 벡터를 쓰지 않습니다.
    except Exception as e:raise DomainError(503,'EMBEDDING_UNAVAILABLE','검색 Embedding 생성에 실패했습니다.') from e
    cond=['v.index_status = \'ready\'', 'e.indexed_revision = v.revision',
          'e.model_name = :model_name']
    params={'keyword_limit':keyword_limit,'pattern':'%'+safe_like(query)+'%',
            'model_name':settings.embedding_model}
    if category_code:
        cond.append('v.category_code=:category');params['category']=category_code
    # Basic은 기존 ID 순을 유지합니다. I-03은 단순하고 설명 가능한 점수를 추가합니다.
    # 제목 3점 + 개요 2점 + 본문 1점. 여러 필드가 맞으면 더하며 동점은 ID 순입니다.
    scored=at_least('intermediate')
    matches={name:f"v.{name} ILIKE :pattern ESCAPE '\\'" for name in ('title','overview','content')}
    rank=' + '.join(f'CASE WHEN {matches[name]} THEN {weight} ELSE 0 END'
                    for name,weight in (('title',3),('overview',2),('content',1)))
    extra=(', ('+rank+') AS keyword_score, '+', '.join(
        f'({condition}) AS {name}_match' for name,condition in matches.items())) if scored else ''
    order='keyword_score DESC, v.report_id' if scored else 'v.report_id'
    sql=('SELECT v.report_id,v.category_code,v.title,v.overview'+extra+' '
         'FROM report_read_view v JOIN report_embeddings e ON e.report_id=v.report_id '
         'WHERE '+' AND '.join(cond)+' AND ('+' OR '.join(matches.values())+') '
         'ORDER BY '+order+' LIMIT :keyword_limit')
    keyword=db.execute(text(sql),params).mappings().all()

    # pgvector SQLAlchemy cosine_distance()가 실제 벡터 연산자 <=>를 사용합니다.
    expr=ReportEmbedding.embedding.cosine_distance(qvec)
    stmt=(select(ReportEmbedding.report_id,expr.label('distance'))
          .join(Report,Report.report_id==ReportEmbedding.report_id)
          .join(ReportCategory,Report.category_id==ReportCategory.category_id)
          .where(Report.index_status=='ready',ReportEmbedding.indexed_revision==Report.revision,
                 ReportEmbedding.model_name==settings.embedding_model)
          .order_by(expr,ReportEmbedding.report_id).limit(semantic_limit))
    if category_code:stmt=stmt.where(ReportCategory.code==category_code)
    sem=db.execute(stmt).all()
    scores={int(row.report_id):max(-1.0,min(1.0,1-float(row.distance))) for row in sem}

    if keyword:
        # Keyword 우선. I/A는 위 점수 순, Basic 및 점수 동점은 낮은 ID 순입니다.
        item=keyword[0]
        rid=int(item['report_id'])
        score=scores.get(rid)
        if score is None:
            # Keyword 상위 후보가 Semantic Top-k 밖이어도 유사도 수치를 얻습니다.
            distance=db.scalar(select(expr).where(ReportEmbedding.report_id==rid))
            score=max(-1.,min(1.,1-float(distance))) if distance is not None else None
        selected=dict(item);keyword_match=True
    elif sem and scores[int(sem[0].report_id)]>=settings.search_min_similarity:
        rid=int(sem[0].report_id)
        selected=db.execute(text('SELECT report_id,category_code,title,overview FROM report_read_view WHERE report_id=:id'),
                            {'id':rid}).mappings().first()
        if selected is None:return {'status':'not_found','query':query,'best_match':None}
        selected=dict(selected);score=scores[rid];keyword_match=False
    else:
        return {'status':'not_found','query':query,'best_match':None}

    result={'report_id':rid,'title':selected['title'],'category_code':selected['category_code'],
            'overview':selected['overview'],'keyword_match':keyword_match,
            'cosine_similarity':round(score,4) if score is not None else None}
    if scored:
        result['keyword_score']=int(selected.get('keyword_score',0))
        result['keyword_matched_fields']=[name for name in matches if selected.get(name+'_match')]
        result['semantic_score']=result['cosine_similarity']
        result['selection_reason']='keyword_score_then_id' if keyword_match else 'semantic_threshold'
        result['threshold']=settings.search_min_similarity
    return {'status':'found','query':query,'best_match':result}
