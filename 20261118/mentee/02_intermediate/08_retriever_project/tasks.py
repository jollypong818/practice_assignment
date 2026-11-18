# Day23 / 실습 08 / 응용 / mentee
from day23kit.fixtures import fixture_search
from day23kit.embedding import get_encoder, encode_question
from day23kit.db import connect_db, exact_topk, check_data_ready

# BEGIN D23-08-I01
def validate_question(question):
    """
    TODO D23-08-I01 · validate_question
        질문은 1자 이상의 문자열이어야 하며 앞뒤 공백을 제거하세요.
        빈 값/공백만 있는 값이면 ValueError. 반환은 정리된 질문.
        API가 연결되어 있지 않아도 검사 가능한 순수 함수입니다.
    """
    # TODO D23-08-I01: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-08-I01: 직접 구현하세요")
# END D23-08-I01

# BEGIN D23-08-I02
def retrieve_candidates(question,mode,k,category,env_file):
    """
    TODO D23-08-I02 · retrieve_candidates
        fixture면 교육용 fixture_search, live면 E5 query Embedding → pgvector Exact SQL을 사용하세요.
        실제 live는 exercise05에서 9개 자료를 먼저 저장해야 합니다.
        DB 연결 실패를 빈 결과 []로 바꾸지 말고 예외를 전달하세요.
    """
    # TODO D23-08-I02: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-08-I02: 직접 구현하세요")
# END D23-08-I02

# BEGIN D23-08-I03
def format_candidates(hits):
    """
    TODO D23-08-I03 · format_candidates
        후보의 id/title/content/category/source_version/distance를 반환하세요.
        검색된 원문을 요약·변조하지 않고, distance는 숫자 그대로 둡니다.
        답변 상태(answered)를 자동으로 부여하지 마세요.
    """
    # TODO D23-08-I03: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-08-I03: 직접 구현하세요")
# END D23-08-I03

# BEGIN D23-08-I04
def validate_options(k,category):
    """
    TODO D23-08-I04 · validate_options
        k는 bool 제외 정수 1~9, category는 None 또는 course/development/support.
        위반하면 ValueError. 정상 출력은 {'k': k,'category': category}.
        입력 검사를 끝내기 전 모델·DB를 호출하지 마세요.
    """
    # TODO D23-08-I04: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-08-I04: 직접 구현하세요")
# END D23-08-I04

# BEGIN D23-08-I05
def make_run_report(question,hits,mode,elapsed_ms):
    """
    TODO D23-08-I05 · make_run_report
        run_status=candidates 또는 empty를 구분하세요.
        source_mode=(fixture:simulated, live:pgvector_exact), elapsed_ms,
        retrieved_ids, human_evidence_ok=None을 기록합니다.
        검색된 것만으로 답변 정확도·근거 승인 True를 만들지 마세요.
    """
    # TODO D23-08-I05: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-08-I05: 직접 구현하세요")
# END D23-08-I05
