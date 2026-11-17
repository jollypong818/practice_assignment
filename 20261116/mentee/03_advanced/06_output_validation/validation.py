"""Day21 실습 06: JSON·Schema·참조 검증. 실행: python main.py"""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))
from coursekit.io import DATA, read_json, write_json

# 기준: Day21 PPT 46~55장. 실제 모델 호출/실습 데이터 수정은 하지 않습니다.
# outputs는 실행 시 생성됩니다. 05/08의 모델 응답은 직접 수집한 원문만 등록합니다.
from pydantic import ValidationError

from contracts.schema import make_model
from contracts.parser import parse_answer
from contracts.rules import check_rules

def validate_answer(raw, provided_ids):
    obj,error=parse_answer(raw)
    if error:
        return None,error
    error=check_rules(obj,provided_ids)
    return (None,error) if error else (obj,None)

def main():
    fixtures=read_json(DATA/"validation_fixtures.json")
    # TODO D21-06-A05: 제공 fixture를 분류하고 모델 정의에서 Schema를 내보내세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 26개 fixture가 기대 오류와 일치. semantic_counterexample은 자동 통과하지만 사람 검토 필요.
    # BEGIN D21-06-A05
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
    raise NotImplementedError("D21-06-A05: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-06-A05
    # TODO D21-06-A06: ID 101을 붙인 서버 답변이 자동 검사만 통과하는 반례를 확인하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: README의 예상 결과와 출력 파일을 대조합니다.
    # 핵심: 이 사람 예상 판단은 작성된 반례의 해설입니다. 실제 모델 평가 점수를 대신 채우지 않습니다.
    # BEGIN D21-06-A06
    counter = next(x for x in fixtures if x["fixture_id"] == "semantic_counterexample")
    obj, error = validate_answer(counter["raw_text"], counter["provided_ids"])
    review = {"source_mode":"fixture","auto_ok":False,"human_expected":"","reason":"","model_performance_claim":False}
    # TODO: 자동 통과와 사람의 예상 근거 부적합을 별도로 저장
    raise NotImplementedError("D21-06-A06: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-06-A06
    # TODO D21-06-A07: 중복 키·NaN·과도한 크기·Schema 경계를 실제 반례로 검사하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 예외를 숨겨 통과하지 말고 기대 오류 단계까지 대조합니다.
    # BEGIN D21-06-A07
    raw_cases = ['{"x":1,"x":2}', '{"x":NaN}', 'x'*20001]
    # TODO: 모두 json_error로 분류되는지 검사
    # TODO: 최대 500자는 허용, bool ID는 거부
    bool_rejected = False
    raise NotImplementedError("D21-06-A07: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-06-A07
    print("[06] 로컬 검증 완료. 구조·참조 검사와 실제 근거 평가는 다릅니다.")
