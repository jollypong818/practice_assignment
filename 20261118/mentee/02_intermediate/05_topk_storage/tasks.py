# Day23 / 실습 05 / 응용 / mentee
from day23kit.data import passage_text
from day23kit.db import TABLE_SQL, SQL_TOPK, SQL_CATEGORY

# BEGIN D23-05-I01
def schema_sql():
    """
    TODO D23-05-I01 · schema_sql
        기존 knowledge 테이블을 건드리지 않는 day23_search_docs의 CREATE TABLE SQL을 작성하세요.
        필드: id(PK),title,content,category,source_version,embedding_model,embedding vector(384).
        DROP/TRUNCATE를 사용하지 않습니다.
    """
    # TODO D23-05-I01: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-05-I01: 직접 구현하세요")
# END D23-05-I01

# BEGIN D23-05-I02
def prepare_document_rows(rows):
    """
    TODO D23-05-I02 · prepare_document_rows
        지식 101~109의 ID/제목/본문/분류/버전 및 passage 입력을 순서대로 묶으세요.
        반환: [{'id', 'passage_input', ...}, ...]. 같은 ID를 새로 만들지 않습니다.
    """
    # TODO D23-05-I02: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-05-I02: 직접 구현하세요")
# END D23-05-I02

# BEGIN D23-05-I03
def topk_sql():
    """
    TODO D23-05-I03 · topk_sql
        Cosine distance(<=>) 오름차순, k개 제한 SQL을 작성하세요.
        SELECT에 id,title,content,category,source_version,embedding_model,distance 포함.
        E5 외 다른 공간 혼합을 막도록 embedding_model을 필터합니다.
    """
    # TODO D23-05-I03: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-05-I03: 직접 구현하세요")
# END D23-05-I03

# BEGIN D23-05-I04
def filtered_sql():
    """
    TODO D23-05-I04 · filtered_sql
        category 필터가 포함된 Top-k SQL을 작성하세요.
        쿼리 벡터와 category, 모델, k는 문자열 합치기가 아닌 %s 바인딩입니다.
    """
    # TODO D23-05-I04: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-05-I04: 직접 구현하세요")
# END D23-05-I04

# BEGIN D23-05-I05
def check_search_options(k,category):
    """
    TODO D23-05-I05 · check_search_options
        k는 bool을 제외한 정수 1~9, category는 None 또는 course/development/support인지 검사하세요.
        잘못된 값은 ValueError. 정상 시 {'k':k,'category':category} 반환.
    """
    # TODO D23-05-I05: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-05-I05: 직접 구현하세요")
# END D23-05-I05
