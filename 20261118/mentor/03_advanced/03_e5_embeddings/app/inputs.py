# Day23 / 실습 03 / 심화 inputs / mentor
from day23kit.data import passage_text


# BEGIN D23-03-A01
def make_passages(rows):
    """
    [강사용 정답] D23-03-A01 · make_passages
        지식 목록을 E5 문서 입력 문자열 목록으로 변환하세요.
        문서에는 'passage: ' + 제목 + ' ' + 본문을 사용합니다.
        한 행마다 정확히 한 문자열을 만들어 순서를 유지하세요.
    """
    # 해설 D23-03-A01: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    # 문서마다 고정된 순서로 passage를 구성하여 ID와 행 인덱스를 보존합니다.
    return [passage_text(row) for row in rows]
# END D23-03-A01

# BEGIN D23-03-A02
def make_queries(questions):
    """
    [강사용 정답] D23-03-A02 · make_queries
        질문 목록 각 요소 앞에 query: 공백을 붙이세요.
        출력: 입력과 동일한 순서의 문자열 리스트.
        빈 질문을 추가해 그럴듯한 벡터를 만들지 마세요.
    """
    # 해설 D23-03-A02: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    return ['query: '+q for q in questions]
# END D23-03-A02
