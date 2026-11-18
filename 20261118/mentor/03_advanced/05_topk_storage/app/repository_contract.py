# Day23 / 실습 05 / 심화 repository_contract / mentor
from day23kit.data import passage_text
from day23kit.db import TABLE_SQL, SQL_TOPK, SQL_CATEGORY


# BEGIN D23-05-A01
def schema_sql():
    """
    [강사용 정답] D23-05-A01 · schema_sql
        기존 knowledge 테이블을 건드리지 않는 day23_search_docs의 CREATE TABLE SQL을 작성하세요.
        필드: id(PK),title,content,category,source_version,embedding_model,embedding vector(384).
        DROP/TRUNCATE를 사용하지 않습니다.
    """
    # 해설 D23-05-A01: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    # 강의의 실제 테이블 정의와 동일한 SQL입니다.
    return TABLE_SQL
# END D23-05-A01

# BEGIN D23-05-A02
def prepare_document_rows(rows):
    """
    [강사용 정답] D23-05-A02 · prepare_document_rows
        지식 101~109의 ID/제목/본문/분류/버전 및 passage 입력을 순서대로 묶으세요.
        반환: [{'id', 'passage_input', ...}, ...]. 같은 ID를 새로 만들지 않습니다.
    """
    # 해설 D23-05-A02: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    return [{**dict(r),'passage_input':passage_text(r)} for r in rows]
# END D23-05-A02

# BEGIN D23-05-A03
def topk_sql():
    """
    [강사용 정답] D23-05-A03 · topk_sql
        Cosine distance(<=>) 오름차순, k개 제한 SQL을 작성하세요.
        SELECT에 id,title,content,category,source_version,embedding_model,distance 포함.
        E5 외 다른 공간 혼합을 막도록 embedding_model을 필터합니다.
    """
    # 해설 D23-05-A03: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    return SQL_TOPK
# END D23-05-A03

# BEGIN D23-05-A04
def filtered_sql():
    """
    [강사용 정답] D23-05-A04 · filtered_sql
        category 필터가 포함된 Top-k SQL을 작성하세요.
        쿼리 벡터와 category, 모델, k는 문자열 합치기가 아닌 %s 바인딩입니다.
    """
    # 해설 D23-05-A04: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    return SQL_CATEGORY
# END D23-05-A04
