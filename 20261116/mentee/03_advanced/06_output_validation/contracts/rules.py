"""PPT 52, 78: 이번 문맥의 출처와 상태 조합 검사."""
from coursekit.contracts import INSUFFICIENT

def check_rules(obj, provided_ids):
    # TODO D21-06-A03: 중복 출처와 이번에 제공하지 않은 출처를 서로 구분하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: README의 예상 결과와 출력 파일을 대조합니다.
    # BEGIN D21-06-A03
    ids = obj.source_ids
    # TODO: len/set을 비교해 duplicate_source, 문맥 밖 ID는 unknown_source
    # 전체 knowledge의 모든 ID가 아닌 provided_ids만 사용합니다.
    raise NotImplementedError("D21-06-A03: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-06-A03
    # TODO D21-06-A04: 상태별 필드 조합과 공백·부족 고정문을 검사하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 정상 부족 응답은 오류가 아닙니다. 과도한 포기는 사람이 평가합니다.
    # BEGIN D21-06-A04
    # TODO: answered는 출처 필요·missing 빈 문자열
    # TODO: 부족은 출처 []·missing.strip() 필요·answer 고정문
    # TODO: 공백만 있는 answer는 blank_answer
    state_error = None
    raise NotImplementedError("D21-06-A04: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-06-A04
    return None
