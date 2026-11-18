# Day23 / 실습 08 / 심화 validation / mentor
from day23kit.data import load_knowledge, E5_MODEL_ID


# BEGIN D23-08-A01
def validate_question(question):
    """
    [강사용 정답] D23-08-A01 · validate_question
        질문은 1자 이상의 문자열이어야 하며 앞뒤 공백을 제거하세요.
        빈 값/공백만 있는 값이면 ValueError. 반환은 정리된 질문.
        API가 연결되어 있지 않아도 검사 가능한 순수 함수입니다.
    """
    # 해설 D23-08-A01: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    if not isinstance(question,str) or not question.strip():raise ValueError('empty_question')
    return question.strip()
# END D23-08-A01

# BEGIN D23-08-A04
def validate_options(k,category):
    """
    [강사용 정답] D23-08-A04 · validate_options
        k는 bool 제외 정수 1~9, category는 None 또는 course/development/support.
        위반하면 ValueError. 정상 출력은 {'k': k,'category': category}.
        입력 검사를 끝내기 전 모델·DB를 호출하지 마세요.
    """
    # 해설 D23-08-A04: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    if type(k) is not int or not 1<=k<=9:raise ValueError('invalid_k')
    if category not in (None,'course','development','support'):raise ValueError('invalid_category')
    return {'k':k,'category':category}
# END D23-08-A04

# BEGIN D23-08-A06
def check_model_and_versions(hits,mode):
    """
    [강사용 정답] D23-08-A06 · check_model_and_versions
        live 결과의 embedding_model이 intfloat/multilingual-e5-small인지 확인하세요.
        모든 ID의 source_version이 오늘 고정 스냅샷과 일치하는지 검증하세요.
        fixture는 실제 DB/모델 검증이 아니므로 'simulated_only'로 기록하세요.
    """
    # 해설 D23-08-A06: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    if mode=='fixture':return 'simulated_only'
    snapshot={r['id']:r for r in load_knowledge()}
    for hit in hits:
        if hit.get('embedding_model')!=E5_MODEL_ID:raise ValueError('embedding_model_mismatch')
        if hit['id'] not in snapshot:raise ValueError('unexpected_knowledge_id')
        if hit['source_version']!=snapshot[hit['id']]['source_version']:
            raise ValueError('source_version_mismatch')
    return 'live_contract_verified'
# END D23-08-A06
