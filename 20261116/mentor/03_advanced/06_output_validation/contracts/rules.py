"""PPT 52, 78: 이번 문맥의 출처와 상태 조합 검사."""
from coursekit.contracts import INSUFFICIENT

def check_rules(obj, provided_ids):
    # 해설 D21-06-A03: 중복 출처와 이번에 제공하지 않은 출처를 서로 구분하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: README의 예상 결과와 출력 파일을 대조합니다.
    # BEGIN D21-06-A03
    ids=obj.source_ids
    if len(ids)!=len(set(ids)):
        return "duplicate_source"
    if not set(ids)<=set(provided_ids):
        return "unknown_source"
    # END D21-06-A03
    # 해설 D21-06-A04: 상태별 필드 조합과 공백·부족 고정문을 검사하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 정상 부족 응답은 오류가 아닙니다. 과도한 포기는 사람이 평가합니다.
    # BEGIN D21-06-A04
    if obj.status=="answered":
        if not ids or obj.missing_information!="":
            return "status_rule"
    else:
        if ids or not obj.missing_information.strip():
            return "status_rule"
    if not obj.answer.strip():
        return "blank_answer"
    if obj.status=="insufficient_context" and obj.answer!=INSUFFICIENT:
        return "status_rule"
    # END D21-06-A04
    return None
