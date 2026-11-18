# Day23 / 실습 01 / 심화 knowledge / mentor



# BEGIN D23-01-A01
def select_original(rows):
    """
    [강사용 정답] D23-01-A01 · select_original
        기존 수업에서 사용한 101·102·103만 ID 오름차순으로 선택합니다.
        입력: 전체 지식 목록(list[dict]). 출력: 원래 지식 3개를 담은 list.
        원본 딕셔너리의 id/title/content를 수정하지 마세요.
        개념: 원문 ID 고정·검색할 자료의 범위.
    """
    # 해설 D23-01-A01: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    # ① 기존 지식의 ID만 고르고 ② 순서 고정: 앞 차시의 ID/원문과 대응합니다.
    return sorted((dict(r) for r in rows if r['id'] in (101,102,103)),key=lambda r:r['id'])
# END D23-01-A01

# BEGIN D23-01-A02
def make_passage_input(row):
    """
    [강사용 정답] D23-01-A02 · make_passage_input
        E5 문서 입력 텍스트를 "passage: 제목 본문" 형식으로 만드세요.
        입력: 지식 한 행. 출력: 문자열. 제목과 본문을 공백 하나로 구분하세요.
        개념: FAQ 질문과 달리 지식 본문을 검색 대상으로 사용합니다.
    """
    # 해설 D23-01-A02: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    # E5 비대칭 검색은 문서에는 passage: 접두어가 필요합니다.
    return 'passage: ' + row['title'] + ' ' + row['content']
# END D23-01-A02

# BEGIN D23-01-A03
def make_mapping(rows):
    """
    [강사용 정답] D23-01-A03 · make_mapping
        각 지식의 id/title/content/category/source_version 및 passage_input을 기록하세요.
        입력: 선택된 지식 목록. 출력: 딕셔너리 목록.
        개념: 벡터를 생성하기 전에도 원문·ID·버전을 추적해야 합니다.
    """
    # 해설 D23-01-A03: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    # 각 ID의 원문과 Embedding 입력을 함께 보존합니다.
    return [dict(id=r['id'],title=r['title'],content=r['content'],
                 category=r['category'],source_version=r['source_version'],
                 passage_input=make_passage_input(r)) for r in rows]
# END D23-01-A03
