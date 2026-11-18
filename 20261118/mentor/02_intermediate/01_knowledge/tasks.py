# Day23 / 실습 01 / 응용 / mentor


# BEGIN D23-01-I01
def select_original(rows):
    """
    [강사용 정답] D23-01-I01 · select_original
        기존 수업에서 사용한 101·102·103만 ID 오름차순으로 선택합니다.
        입력: 전체 지식 목록(list[dict]). 출력: 원래 지식 3개를 담은 list.
        원본 딕셔너리의 id/title/content를 수정하지 마세요.
        개념: 원문 ID 고정·검색할 자료의 범위.
    """
    # 해설 D23-01-I01: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    # ① 기존 지식의 ID만 고르고 ② 순서 고정: 앞 차시의 ID/원문과 대응합니다.
    return sorted((dict(r) for r in rows if r['id'] in (101,102,103)),key=lambda r:r['id'])
# END D23-01-I01

# BEGIN D23-01-I02
def make_passage_input(row):
    """
    [강사용 정답] D23-01-I02 · make_passage_input
        E5 문서 입력 텍스트를 "passage: 제목 본문" 형식으로 만드세요.
        입력: 지식 한 행. 출력: 문자열. 제목과 본문을 공백 하나로 구분하세요.
        개념: FAQ 질문과 달리 지식 본문을 검색 대상으로 사용합니다.
    """
    # 해설 D23-01-I02: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    # E5 비대칭 검색은 문서에는 passage: 접두어가 필요합니다.
    return 'passage: ' + row['title'] + ' ' + row['content']
# END D23-01-I02

# BEGIN D23-01-I03
def make_mapping(rows):
    """
    [강사용 정답] D23-01-I03 · make_mapping
        각 지식의 id/title/content/category/source_version 및 passage_input을 기록하세요.
        입력: 선택된 지식 목록. 출력: 딕셔너리 목록.
        개념: 벡터를 생성하기 전에도 원문·ID·버전을 추적해야 합니다.
    """
    # 해설 D23-01-I03: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    # 각 ID의 원문과 Embedding 입력을 함께 보존합니다.
    return [dict(id=r['id'],title=r['title'],content=r['content'],
                 category=r['category'],source_version=r['source_version'],
                 passage_input=make_passage_input(r)) for r in rows]
# END D23-01-I03

# BEGIN D23-01-I04
def reject_duplicate_ids(rows):
    """
    [강사용 정답] D23-01-I04 · reject_duplicate_ids
        모든 9개 지식의 ID 중복 여부를 점검하고 중복이면 ValueError를 내세요.
        단순 len만 비교하지 말고 id의 타입이 int(True 제외)인지도 확인합니다.
        출력: 중복이 없으면 실제 ID 집합(set).
    """
    # 해설 D23-01-I04: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    ids=[r.get('id') for r in rows]
    # bool은 int의 하위 타입이므로 type(...) is int로 엄격하게 검사합니다.
    if any(type(x) is not int or x<=0 for x in ids):raise ValueError('id 타입 오류')
    if len(ids)!=len(set(ids)):raise ValueError('duplicate_id')
    return set(ids)
# END D23-01-I04

# BEGIN D23-01-I05
def reject_missing_fields(rows):
    """
    [강사용 정답] D23-01-I05 · reject_missing_fields
        title/content/category/source_version의 누락 또는 공백 문자열을 거부하세요.
        입력: 전체 지식 목록. 정상 출력: True. 잘못된 항목은 ValueError.
        개념: 잘못된 원문은 정상적인 Embedding 입력이 될 수 없습니다.
    """
    # 해설 D23-01-I05: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    for r in rows:
        for name in ('title','content','category','source_version'):
            if not isinstance(r.get(name),str) or not r[name].strip():
                raise ValueError('missing_or_blank:'+name)
    return True
# END D23-01-I05
