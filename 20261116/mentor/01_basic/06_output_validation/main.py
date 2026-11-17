"""Day21 실습 06: JSON·Schema·참조 검증. 실행: python main.py"""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))
from coursekit.io import DATA, read_json, write_json, run

# 기준: Day21 PPT 46~55장. 실제 모델 호출/실습 데이터 수정은 하지 않습니다.
# outputs는 실행 시 생성됩니다. 05/08의 모델 응답은 직접 수집한 원문만 등록합니다.
from typing import Annotated, Literal
from pydantic import BaseModel, ConfigDict, Field, ValidationError
from coursekit.contracts import strict_json, INSUFFICIENT

def make_model():
    # 해설 D21-06-B01: PPT 50장의 엄격한 네 필드 계약을 선언하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 문자열 ID "101", bool true, 추가 필드, 501자 답을 거부합니다.
    # 핵심: 모델 정의는 로컬 검증입니다. 실제 LLM의 생성 형식을 자동 제약하는 API 설정은 아닙니다.
    # BEGIN D21-06-B01
    SourceID=Annotated[int,Field(strict=True,gt=0)]
    class KnowledgeAnswer(BaseModel):
        model_config=ConfigDict(extra="forbid",strict=True)
        status: Literal["answered","insufficient_context"]
        answer: str = Field(min_length=1,max_length=500)
        source_ids: list[SourceID] = Field(max_length=3)
        missing_information: str = Field(max_length=200)
    # END D21-06-B01
    return KnowledgeAnswer

def parse_answer(raw):
    Model=make_model()
    # 해설 D21-06-B02: JSON 문법 실패와 Pydantic Schema 실패를 분리하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 깨진 JSON→json_error, {} 또는 문자열 출처→schema_error.
    # 핵심: 형변환을 허용해 잘못된 출처를 억지로 정수로 만들지 않습니다.
    # BEGIN D21-06-B02
    try:
        data=strict_json(raw)
    except (ValueError,RecursionError):
        return None,"json_error"
    try:
        obj=Model.model_validate(data)
    except ValidationError:
        return None,"schema_error"
    # END D21-06-B02
    return obj,None

def check_rules(obj, provided_ids):
    # 해설 D21-06-B03: 이번 문맥의 출처 범위와 상태별 조합을 확인하세요.
    # 입력·대상: obj 및 실제 전달된 provided_ids
    # 완료 기준: [999]→unknown_source; 부족 응답은 고정문·빈 출처·부족 정보명 조합.
    # 핵심: ID 포함 검사는 근거 문장의 의미적 뒷받침을 증명하지 않습니다.
    # BEGIN D21-06-B03
    ids=obj.source_ids
    if len(ids)!=len(set(ids)):
        return "duplicate_source"
    if not set(ids)<=set(provided_ids):
        return "unknown_source"
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
    # END D21-06-B03
    return None

def validate_answer(raw, provided_ids):
    obj,error=parse_answer(raw)
    if error:
        return None,error
    error=check_rules(obj,provided_ids)
    return (None,error) if error else (obj,None)

def main():
    fixtures=read_json(DATA/"validation_fixtures.json")
    # 해설 D21-06-B04: 제공 fixture를 분류하고 모델 정의에서 Schema를 내보내세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 26개 fixture가 기대 오류와 일치. semantic_counterexample은 자동 통과하지만 사람 검토 필요.
    # BEGIN D21-06-B04
    results=[]
    for item in fixtures:
        obj,error=validate_answer(item["raw_text"],item["provided_ids"])
        results.append({"fixture_id":item["fixture_id"],"source_mode":"fixture","error":error,
                        "expected_error":item["expected_error"],"matches_expected":error==item["expected_error"],"evidence_ok":None})
    assert all(r["matches_expected"] for r in results)
    write_json(HERE/"outputs"/"fixture_results.json",results)
    write_json(HERE/"outputs"/"answer_schema.json",make_model().model_json_schema())
    # END D21-06-B04
    print("[06] 로컬 검증 완료. 구조·참조 검사와 실제 근거 평가는 다릅니다.")

if __name__ == "__main__":
    run(main)
