"""Day21 실습 06: JSON·Schema·참조 검증. 실행: python main.py"""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))
from coursekit.io import DATA, read_json, write_json

# 기준: Day21 PPT 46~55장. 실제 모델 호출/실습 데이터 수정은 하지 않습니다.
# outputs는 실행 시 생성됩니다. 05/08의 모델 응답은 직접 수집한 원문만 등록합니다.
from typing import Annotated, Literal
from pydantic import BaseModel, ConfigDict, Field, ValidationError
from coursekit.contracts import strict_json, INSUFFICIENT

def make_model():
    # TODO D21-06-I01: PPT 50장의 엄격한 네 필드 계약을 선언하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 문자열 ID "101", bool true, 추가 필드, 501자 답을 거부합니다.
    # 핵심: 모델 정의는 로컬 검증입니다. 실제 LLM의 생성 형식을 자동 제약하는 API 설정은 아닙니다.
    # BEGIN D21-06-I01
    SourceID = Annotated[int, Field(strict=True, gt=0)]
    class KnowledgeAnswer(BaseModel):
        model_config = ConfigDict(extra="forbid", strict=True)
        status: Literal["answered", "insufficient_context"]
        answer: str = Field(min_length=1, max_length=1)  # TODO: 최대 500
        source_ids: list[SourceID] = Field(max_length=1) # TODO: 최대 3
        missing_information: str = Field(max_length=1) # TODO: 최대 200
    # 기본값을 추가하지 마세요. 네 필드 모두 필수입니다.
    raise NotImplementedError("D21-06-I01: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-06-I01
    return KnowledgeAnswer

def parse_answer(raw):
    Model=make_model()
    # TODO D21-06-I02: JSON 문법 실패와 Pydantic Schema 실패를 분리하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 깨진 JSON→json_error, {} 또는 문자열 출처→schema_error.
    # 핵심: 형변환을 허용해 잘못된 출처를 억지로 정수로 만들지 않습니다.
    # BEGIN D21-06-I02
    try:
        data = strict_json(raw)  # 크기·중복 키 보호는 제공 함수
    except (ValueError, RecursionError):
        return None, ""         # TODO: json_error
    try:
        obj = None              # TODO: Model.model_validate(data)
    except ValidationError:
        return None, ""         # TODO: schema_error
    raise NotImplementedError("D21-06-I02: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-06-I02
    return obj,None

def check_rules(obj, provided_ids):
    # TODO D21-06-I03: 중복 출처와 이번에 제공하지 않은 출처를 서로 구분하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: README의 예상 결과와 출력 파일을 대조합니다.
    # BEGIN D21-06-I03
    ids = obj.source_ids
    # TODO: len/set을 비교해 duplicate_source, 문맥 밖 ID는 unknown_source
    # 전체 knowledge의 모든 ID가 아닌 provided_ids만 사용합니다.
    raise NotImplementedError("D21-06-I03: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-06-I03
    # TODO D21-06-I04: 상태별 필드 조합과 공백·부족 고정문을 검사하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 정상 부족 응답은 오류가 아닙니다. 과도한 포기는 사람이 평가합니다.
    # BEGIN D21-06-I04
    # TODO: answered는 출처 필요·missing 빈 문자열
    # TODO: 부족은 출처 []·missing.strip() 필요·answer 고정문
    # TODO: 공백만 있는 answer는 blank_answer
    state_error = None
    raise NotImplementedError("D21-06-I04: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-06-I04
    return None

def validate_answer(raw, provided_ids):
    obj,error=parse_answer(raw)
    if error:
        return None,error
    error=check_rules(obj,provided_ids)
    return (None,error) if error else (obj,None)

def main():
    fixtures=read_json(DATA/"validation_fixtures.json")
    # TODO D21-06-I05: 제공 fixture를 분류하고 모델 정의에서 Schema를 내보내세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 26개 fixture가 기대 오류와 일치. semantic_counterexample은 자동 통과하지만 사람 검토 필요.
    # BEGIN D21-06-I05
    results = []
    for item in fixtures:
        obj, error = validate_answer(item["raw_text"], item["provided_ids"])
        results.append({"fixture_id":item["fixture_id"],"source_mode":"fixture",
                        "error":error,"expected_error":item["expected_error"],
                        "matches_expected":False,  # TODO: error와 expected_error 비교
                        "evidence_ok":None})
    # TODO: 각 행의 matches_expected가 True인지 확인
    write_json(HERE/"outputs"/"fixture_results.json", results)
    write_json(HERE/"outputs"/"answer_schema.json", {})  # TODO: model_json_schema()
    raise NotImplementedError("D21-06-I05: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-06-I05
    # TODO D21-06-I06: ID 101을 붙인 서버 답변이 자동 검사만 통과하는 반례를 확인하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: README의 예상 결과와 출력 파일을 대조합니다.
    # 핵심: 이 사람 예상 판단은 작성된 반례의 해설입니다. 실제 모델 평가 점수를 대신 채우지 않습니다.
    # BEGIN D21-06-I06
    counter = next(x for x in fixtures if x["fixture_id"] == "semantic_counterexample")
    obj, error = validate_answer(counter["raw_text"], counter["provided_ids"])
    review = {"source_mode":"fixture","auto_ok":False,"human_expected":"","reason":"","model_performance_claim":False}
    # TODO: 자동 통과와 사람의 예상 근거 부적합을 별도로 저장
    raise NotImplementedError("D21-06-I06: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-06-I06
    print("[06] 로컬 검증 완료. 구조·참조 검사와 실제 근거 평가는 다릅니다.")
