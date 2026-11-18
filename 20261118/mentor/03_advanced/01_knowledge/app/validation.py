# Day23 / 실습 01 / 심화 validation / mentor



# BEGIN D23-01-A04
def reject_duplicate_ids(rows):
    """
    [강사용 정답] D23-01-A04 · reject_duplicate_ids
        모든 9개 지식의 ID 중복 여부를 점검하고 중복이면 ValueError를 내세요.
        단순 len만 비교하지 말고 id의 타입이 int(True 제외)인지도 확인합니다.
        출력: 중복이 없으면 실제 ID 집합(set).
    """
    # 해설 D23-01-A04: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    ids=[r.get('id') for r in rows]
    # bool은 int의 하위 타입이므로 type(...) is int로 엄격하게 검사합니다.
    if any(type(x) is not int or x<=0 for x in ids):raise ValueError('id 타입 오류')
    if len(ids)!=len(set(ids)):raise ValueError('duplicate_id')
    return set(ids)
# END D23-01-A04

# BEGIN D23-01-A05
def reject_missing_fields(rows):
    """
    [강사용 정답] D23-01-A05 · reject_missing_fields
        title/content/category/source_version의 누락 또는 공백 문자열을 거부하세요.
        입력: 전체 지식 목록. 정상 출력: True. 잘못된 항목은 ValueError.
        개념: 잘못된 원문은 정상적인 Embedding 입력이 될 수 없습니다.
    """
    # 해설 D23-01-A05: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    for r in rows:
        for name in ('title','content','category','source_version'):
            if not isinstance(r.get(name),str) or not r[name].strip():
                raise ValueError('missing_or_blank:'+name)
    return True
# END D23-01-A05

# BEGIN D23-01-A06
def audit_versions(rows):
    """
    [강사용 정답] D23-01-A06 · audit_versions
        101~103은 knowledge_v1, 104~109는 knowledge_search_v2인지 검사하세요.
        기존 원문을 덮어쓰지 말고, 오류이면 ValueError를 발생시킵니다.
        반환: {버전: ID 목록} 딕셔너리. 개념: 데이터 갱신 계약·버전 추적.
    """
    # 해설 D23-01-A06: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    out={'knowledge_v1':[],'knowledge_search_v2':[]}
    for r in rows:
        expected='knowledge_v1' if r['id'] in (101,102,103) else 'knowledge_search_v2'
        if r['source_version']!=expected:raise ValueError('version_mismatch:'+str(r['id']))
        out[expected].append(r['id'])
    return out
# END D23-01-A06
