"""PPT 51, 77: 문법과 구조 검사. 사실성 판정은 하지 않습니다."""
from pydantic import ValidationError
from coursekit.contracts import strict_json
from .schema import make_model

def parse_answer(raw):
    Model=make_model()
    # 해설 D21-06-A02: JSON 문법 실패와 Pydantic Schema 실패를 분리하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 깨진 JSON→json_error, {} 또는 문자열 출처→schema_error.
    # 핵심: 형변환을 허용해 잘못된 출처를 억지로 정수로 만들지 않습니다.
    # BEGIN D21-06-A02
    try:
        data=strict_json(raw)
    except (ValueError,RecursionError):
        return None,"json_error"
    try:
        obj=Model.model_validate(data)
    except ValidationError:
        return None,"schema_error"
    # END D21-06-A02
    return obj,None
