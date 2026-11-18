# Day23 / 실습 01 / 심화 validation / mentee



# BEGIN D23-01-A04
def reject_duplicate_ids(rows):
    """
    TODO D23-01-A04 · reject_duplicate_ids
        모든 9개 지식의 ID 중복 여부를 점검하고 중복이면 ValueError를 내세요.
        단순 len만 비교하지 말고 id의 타입이 int(True 제외)인지도 확인합니다.
        출력: 중복이 없으면 실제 ID 집합(set).
    """
    # TODO D23-01-A04: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-01-A04: 직접 구현하세요")
# END D23-01-A04

# BEGIN D23-01-A05
def reject_missing_fields(rows):
    """
    TODO D23-01-A05 · reject_missing_fields
        title/content/category/source_version의 누락 또는 공백 문자열을 거부하세요.
        입력: 전체 지식 목록. 정상 출력: True. 잘못된 항목은 ValueError.
        개념: 잘못된 원문은 정상적인 Embedding 입력이 될 수 없습니다.
    """
    # TODO D23-01-A05: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-01-A05: 직접 구현하세요")
# END D23-01-A05

# BEGIN D23-01-A06
def audit_versions(rows):
    """
    TODO D23-01-A06 · audit_versions
        101~103은 knowledge_v1, 104~109는 knowledge_search_v2인지 검사하세요.
        기존 원문을 덮어쓰지 말고, 오류이면 ValueError를 발생시킵니다.
        반환: {버전: ID 목록} 딕셔너리. 개념: 데이터 갱신 계약·버전 추적.
    """
    # TODO D23-01-A06: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-01-A06: 직접 구현하세요")
# END D23-01-A06
