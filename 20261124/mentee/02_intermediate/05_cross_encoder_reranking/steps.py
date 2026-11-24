"""단계별 역할 분리: steps.py / 독립 실행은 main.py. """

def create_pairs(question, docs):
    """CrossEncoder 입력은 [질문, 문서본문]의 쌍 목록입니다."""
    # BEGIN D27-05-I01
    # TODO D27-05-I01: CrossEncoder 입력은 [질문, 문서본문]의 쌍 목록입니다.
    # 반환값과 예외 조건은 README.md의 수행 기준을 따르세요.
    raise NotImplementedError("D27-05-I01 미완성")
    # END D27-05-I01


def rank_documents(question, docs, scorer):
    """Reranker는 후보를 새로 찾지 않고 동일 후보를 순위 변경합니다."""
    # BEGIN D27-05-I02
    # TODO D27-05-I02: Reranker는 후보를 새로 찾지 않고 동일 후보를 순위 변경합니다.
    # 반환값과 예외 조건은 README.md의 수행 기준을 따르세요.
    raise NotImplementedError("D27-05-I02 미완성")
    # END D27-05-I02
