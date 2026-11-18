# Day23 / 실습 01 / 심화 knowledge / mentee



# BEGIN D23-01-A01
def select_original(rows):
    """
    TODO D23-01-A01 · select_original
        기존 수업에서 사용한 101·102·103만 ID 오름차순으로 선택합니다.
        입력: 전체 지식 목록(list[dict]). 출력: 원래 지식 3개를 담은 list.
        원본 딕셔너리의 id/title/content를 수정하지 마세요.
        개념: 원문 ID 고정·검색할 자료의 범위.
    """
    # TODO D23-01-A01: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-01-A01: 직접 구현하세요")
# END D23-01-A01

# BEGIN D23-01-A02
def make_passage_input(row):
    """
    TODO D23-01-A02 · make_passage_input
        E5 문서 입력 텍스트를 "passage: 제목 본문" 형식으로 만드세요.
        입력: 지식 한 행. 출력: 문자열. 제목과 본문을 공백 하나로 구분하세요.
        개념: FAQ 질문과 달리 지식 본문을 검색 대상으로 사용합니다.
    """
    # TODO D23-01-A02: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-01-A02: 직접 구현하세요")
# END D23-01-A02

# BEGIN D23-01-A03
def make_mapping(rows):
    """
    TODO D23-01-A03 · make_mapping
        각 지식의 id/title/content/category/source_version 및 passage_input을 기록하세요.
        입력: 선택된 지식 목록. 출력: 딕셔너리 목록.
        개념: 벡터를 생성하기 전에도 원문·ID·버전을 추적해야 합니다.
    """
    # TODO D23-01-A03: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-01-A03: 직접 구현하세요")
# END D23-01-A03
