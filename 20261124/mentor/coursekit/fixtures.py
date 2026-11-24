"""오프라인 데이터(모델·DB 실측이 아님). 비공개/옛 버전/미공개 데이터는 제외합니다."""
from coursekit.io import load_json
from coursekit.documents import hit_to_document


def allowed(row, category, role='learner'):
    return (row['category']==category and row['is_current'] and row['ready']
            and (row['access_level']=='public' or role=='staff'))


def fixture_hits(category='시설', role='learner'):
    return [dict(row, citation_id=row['fixture_citation_id'])
            for row in load_json('corpus.json') if allowed(row,category,role)]


def fixture_search(query,category='시설',k=5,role='learner',*,question_id=None):
    """제공 순위 또는 단순 토큰 포함 기준. 실제 E5 검색 결과로 표시하지 않습니다."""
    if type(k) is not int or not 1<=k<=20:raise ValueError('k: 1~20')
    pool=fixture_hits(category,role)
    forced=load_json('fixture_rankings.json').get(question_id,[]) if question_id else []
    def score(row):
        if row['chunk_id'] in forced:return (1000-forced.index(row['chunk_id']),row['chunk_id'])
        # 재현 가능한 문자 수준 단순 휴리스틱. RAG 품질 평가에 사용 금지.
        qset=set(query.replace(' ','').lower())
        content=row['body']+row['title']
        return (sum(ch in qset for ch in content),row['chunk_id'])
    return [hit_to_document(row) for row in sorted(pool,key=score,reverse=True)[:k]]


def get_question(qid='Q01'):
    matches=[q for q in load_json('questions.json') if q['id']==qid]
    if not matches:raise KeyError(qid)
    return matches[0]


def rewrite_fixture(question,history):
    """LLM 미호출 규칙: 제공된 대화 1개만 처리하는 학습 예시."""
    text=question.strip()
    if text in {'그럼 취소는 어떻게 해?','그거 취소 어떻게 해?'}:
        if any('회의실' in turn.get('content','') for turn in history):
            return '회의실 예약을 취소하는 방법은?'
        return None
    if text=='예약 시간을 바꾸고 싶은데?' and any('회의실' in turn.get('content','') for turn in history):
        return '회의실 예약 시간을 변경하는 방법은?'
    if any(word in text for word in ('그거','그것')) and not history:return None
    return text


def fixed_rank_scores(question,docs):
    """CrossEncoder 실측값이 아닌 교육용 고정 점수."""
    boosts={'FAC-102-C1':3.2,'FAC-103-C1':2.6,'FAC-104-C1':2.1,'ACA-101-C1':3.5,
            'FAC-101-C1':0.5,'FAC-107-C1':0.3,'ACA-102-C1':0.4,'FAC-105-C1':1.1}
    return [float(boosts.get(d.metadata['chunk_id'],0.1)) for d in docs]
