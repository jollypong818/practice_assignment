# Day23 / 실습 08 / 응용 / mentor
from day23kit.fixtures import fixture_search
from day23kit.embedding import get_encoder, encode_question
from day23kit.db import connect_db, exact_topk, check_data_ready

# BEGIN D23-08-I01
def validate_question(question):
    """
    [강사용 정답] D23-08-I01 · validate_question
        질문은 1자 이상의 문자열이어야 하며 앞뒤 공백을 제거하세요.
        빈 값/공백만 있는 값이면 ValueError. 반환은 정리된 질문.
        API가 연결되어 있지 않아도 검사 가능한 순수 함수입니다.
    """
    # 해설 D23-08-I01: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    if not isinstance(question,str) or not question.strip():raise ValueError('empty_question')
    return question.strip()
# END D23-08-I01

# BEGIN D23-08-I02
def retrieve_candidates(question,mode,k,category,env_file):
    """
    [강사용 정답] D23-08-I02 · retrieve_candidates
        fixture면 교육용 fixture_search, live면 E5 query Embedding → pgvector Exact SQL을 사용하세요.
        실제 live는 exercise05에서 9개 자료를 먼저 저장해야 합니다.
        DB 연결 실패를 빈 결과 []로 바꾸지 말고 예외를 전달하세요.
    """
    # 해설 D23-08-I02: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    if mode=='fixture':return fixture_search(question,k,category)
    encoder=get_encoder('live')
    qvec=encode_question(encoder,question)
    # 실제 연결은 명시적으로 --mode live를 지정한 경우에만 만듭니다.
    with connect_db(env_file) as conn:
        check_data_ready(conn)
        return exact_topk(conn,qvec,k,category)
# END D23-08-I02

# BEGIN D23-08-I03
def format_candidates(hits):
    """
    [강사용 정답] D23-08-I03 · format_candidates
        후보의 id/title/content/category/source_version/distance를 반환하세요.
        검색된 원문을 요약·변조하지 않고, distance는 숫자 그대로 둡니다.
        답변 상태(answered)를 자동으로 부여하지 마세요.
    """
    # 해설 D23-08-I03: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    return [{'id':h['id'],'title':h['title'],'content':h['content'],
             'category':h['category'],'source_version':h['source_version'],
             'distance':round(float(h['distance']),6)} for h in hits]
# END D23-08-I03

# BEGIN D23-08-I04
def validate_options(k,category):
    """
    [강사용 정답] D23-08-I04 · validate_options
        k는 bool 제외 정수 1~9, category는 None 또는 course/development/support.
        위반하면 ValueError. 정상 출력은 {'k': k,'category': category}.
        입력 검사를 끝내기 전 모델·DB를 호출하지 마세요.
    """
    # 해설 D23-08-I04: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    if type(k) is not int or not 1<=k<=9:raise ValueError('invalid_k')
    if category not in (None,'course','development','support'):raise ValueError('invalid_category')
    return {'k':k,'category':category}
# END D23-08-I04

# BEGIN D23-08-I05
def make_run_report(question,hits,mode,elapsed_ms):
    """
    [강사용 정답] D23-08-I05 · make_run_report
        run_status=candidates 또는 empty를 구분하세요.
        source_mode=(fixture:simulated, live:pgvector_exact), elapsed_ms,
        retrieved_ids, human_evidence_ok=None을 기록합니다.
        검색된 것만으로 답변 정확도·근거 승인 True를 만들지 마세요.
    """
    # 해설 D23-08-I05: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    return {'run_status':'candidates' if hits else 'empty',
            'source_mode':'simulated' if mode=='fixture' else 'pgvector_exact',
            'retrieved_ids':[h['id'] for h in hits],
            'elapsed_ms':round(elapsed_ms,3),
            'human_evidence_ok':None}
# END D23-08-I05
