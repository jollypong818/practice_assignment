# Day23 / 실습 08 / 심화 validation / mentee
from day23kit.data import load_knowledge, E5_MODEL_ID


# BEGIN D23-08-A01
def validate_question(question):
    """
    TODO D23-08-A01 · validate_question
        질문은 1자 이상의 문자열이어야 하며 앞뒤 공백을 제거하세요.
        빈 값/공백만 있는 값이면 ValueError. 반환은 정리된 질문.
        API가 연결되어 있지 않아도 검사 가능한 순수 함수입니다.
    """
    # TODO D23-08-A01: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-08-A01: 직접 구현하세요")
# END D23-08-A01

# BEGIN D23-08-A04
def validate_options(k,category):
    """
    TODO D23-08-A04 · validate_options
        k는 bool 제외 정수 1~9, category는 None 또는 course/development/support.
        위반하면 ValueError. 정상 출력은 {'k': k,'category': category}.
        입력 검사를 끝내기 전 모델·DB를 호출하지 마세요.
    """
    # TODO D23-08-A04: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-08-A04: 직접 구현하세요")
# END D23-08-A04

# BEGIN D23-08-A06
def check_model_and_versions(hits,mode):
    """
    TODO D23-08-A06 · check_model_and_versions
        live 결과의 embedding_model이 intfloat/multilingual-e5-small인지 확인하세요.
        모든 ID의 source_version이 오늘 고정 스냅샷과 일치하는지 검증하세요.
        fixture는 실제 DB/모델 검증이 아니므로 'simulated_only'로 기록하세요.
    """
    # TODO D23-08-A06: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-08-A06: 직접 구현하세요")
# END D23-08-A06
