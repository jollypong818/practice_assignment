"""Day21 실습 02: Zero/Few-shot·버전. 실행: python main.py"""
from pathlib import Path
import sys
import json

HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))
from coursekit.io import DATA, read_json, write_json, write_text, save_version
from coursekit.prompting import make_bundle

# 기준: Day21 PPT 14~20장. 실제 모델 호출/실습 데이터 수정은 하지 않습니다.
# outputs는 실행 시 생성됩니다. 05/08의 모델 응답은 직접 수집한 원문만 등록합니다.
from coursekit.prompting import render_prompt

def build_examples():
    # TODO D21-02-A01: 예제 ID 901을 사용해 정상 답과 정보 부족 답을 완성하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 정상·부족 예제 2개. 평가 질문 D/H를 Few-shot에 사용하지 않습니다.
    # 핵심: 입력 예제를 늘려도 모델 가중치가 바뀌는 것은 아닙니다.
    # BEGIN D21-02-A01
    example_context = [{"id":901,"content":"대여 장소는 안내 데스크입니다."}]
    examples = [
        {"question":"어디서 대여하나요?","context":example_context,
         "answer":{"status":"", "answer":"", "source_ids":[], "missing_information":""}},
        {"question":"대여료는 얼마인가요?","context":example_context,
         "answer":{"status":"", "answer":"", "source_ids":[], "missing_information":""}},
    ]
    # TODO: 정상 답에는 [901], 정보 부족에는 []와 부족한 사실 이름을 사용합니다.
    raise NotImplementedError("D21-02-A01: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-02-A01
    return examples

def main():
    examples=build_examples()
    # TODO D21-02-A02: 같은 질문에 Zero-shot과 Few-shot Prompt를 각각 만드세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 두 Prompt가 생성됩니다. 이는 05의 근거 규칙 A/B와 별도 설계 실험입니다.
    # BEGIN D21-02-A02
    case = read_json(DATA/"dev_v1.json")[0]
    zero_bundle = make_bundle(examples=[])     # 예제 없는 입력
    few_bundle = make_bundle(examples=[])      # TODO: examples 사용
    zero_prompt, _ = render_prompt(zero_bundle, case, "A")
    few_prompt, _ = render_prompt(few_bundle, case, "A")
    # TODO: 예제 ID 901의 포함 여부를 확인
    raise NotImplementedError("D21-02-A02: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-02-A02
    # TODO D21-02-A03: 변경점·가설·고정 조건과 두 Prompt를 저장하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 가설을 실제 성능 결과처럼 기록하지 않습니다.
    # BEGIN D21-02-A03
    experiment = {
        "experiment":"examples_design_only", "base_version":"examples_zero_v1", "new_version":"examples_few_v1",
        "changed":"", "hypothesis":"", "fixed":[], "source_mode":"design_only"
    }
    # TODO: 예제 유무를 바꿨다는 기록과 고정 조건을 작성
    write_json(HERE/"outputs"/"examples.json", [])  # TODO: examples
    write_json(HERE/"outputs"/"experiment.json", experiment)
    write_text(HERE/"outputs"/"zero_prompt.txt", "")  # TODO: zero_prompt
    write_text(HERE/"outputs"/"few_prompt.txt", "")   # TODO: few_prompt
    raise NotImplementedError("D21-02-A03: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-02-A03
    # TODO D21-02-A04: 예제 하나의 질문 표현만 바꾸고 새 버전으로 기록하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 기존 examples를 변경하지 않고 새 파일로 저장합니다.
    # BEGIN D21-02-A04
    replaced = json.loads(json.dumps(examples,ensure_ascii=False))
    # TODO: replaced[0]["question"]만 바꾸고 새 버전·이유 기록
    record = {"version":"examples_few_v2","changed":"","hypothesis":"","examples":replaced}
    # TODO: save_version 사용. 05 A/B에 이 변경을 함께 섞지 마세요.
    raise NotImplementedError("D21-02-A04: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-02-A04
    # TODO D21-02-A05: Few-shot 예제에 D/H 질문과 답이 누출되지 않았는지 검사하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: README의 예상 결과와 출력 파일을 대조합니다.
    # 핵심: 문자열 일치 검사는 최소 보호입니다. 같은 의미로 바꾼 답 누출은 사람이 추가 검토합니다.
    # BEGIN D21-02-A05
    eval_cases = read_json(DATA/"dev_v1.json") + read_json(DATA/"holdout_v1.json")
    eval_questions = set()  # TODO: 질문 문자열 집합
    # TODO: 모든 예제의 질문이 평가 질문 집합 밖인지, 예제 출처가 901 범위인지 검사
    raise NotImplementedError("D21-02-A05: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-02-A05
    # TODO D21-02-A06: 동일 버전 덮어쓰기 방지가 실제로 동작하는지 임시 폴더에서 검사하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: README의 예상 결과와 출력 파일을 대조합니다.
    # BEGIN D21-02-A06
    from tempfile import TemporaryDirectory
    with TemporaryDirectory() as temp:
        path = Path(temp)/"version.json"
        # TODO: 같은 경로에 다른 내용을 저장할 때 ValueError인지 검사
        blocked = False
    # TODO: 실제 결과를 version_guard.json에 저장
    raise NotImplementedError("D21-02-A06: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-02-A06
    print("[02] 예제·버전 설계 완료. 05는 예제 고정, 근거 규칙만 비교합니다.")
