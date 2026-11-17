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
    # 해설 D21-02-I01: 예제 ID 901을 사용해 정상 답과 정보 부족 답을 완성하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 정상·부족 예제 2개. 평가 질문 D/H를 Few-shot에 사용하지 않습니다.
    # 핵심: 입력 예제를 늘려도 모델 가중치가 바뀌는 것은 아닙니다.
    # BEGIN D21-02-I01
    example_context = [{"id":901,"content":"대여 장소는 안내 데스크입니다."}]
    examples = [
        {"question":"어디서 대여하나요?","context":example_context,
         "answer":{"status":"answered","answer":"안내 데스크에서 대여합니다.","source_ids":[901],"missing_information":""}},
        {"question":"대여료는 얼마인가요?","context":example_context,
         "answer":{"status":"insufficient_context","answer":"제공된 지식으로는 답할 수 없습니다.","source_ids":[],"missing_information":"대여료"}},
    ]
    # END D21-02-I01
    return examples

def main():
    examples=build_examples()
    # 해설 D21-02-I02: 같은 질문에 Zero-shot과 Few-shot Prompt를 각각 만드세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 두 Prompt가 생성됩니다. 이는 05의 근거 규칙 A/B와 별도 설계 실험입니다.
    # BEGIN D21-02-I02
    case=read_json(DATA/"dev_v1.json")[0]
    zero_bundle=make_bundle(examples=[])
    few_bundle=make_bundle(examples=examples)
    zero_prompt,_=render_prompt(zero_bundle,case,"A")
    few_prompt,_=render_prompt(few_bundle,case,"A")
    assert "901" not in zero_prompt and "901" in few_prompt
    # END D21-02-I02
    # 해설 D21-02-I03: 변경점·가설·고정 조건과 두 Prompt를 저장하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 가설을 실제 성능 결과처럼 기록하지 않습니다.
    # BEGIN D21-02-I03
    experiment={"experiment":"examples_design_only","base_version":"examples_zero_v1","new_version":"examples_few_v1",
                "changed":"예제 유무","hypothesis":"정상과 정보 부족의 출력 조합을 잘 따를지 관찰한다.",
                "fixed":["질문","knowledge_v1","answer_schema_v1","근거 규칙"],"source_mode":"design_only"}
    write_json(HERE/"outputs"/"examples.json",examples)
    write_json(HERE/"outputs"/"experiment.json",experiment)
    write_text(HERE/"outputs"/"zero_prompt.txt",zero_prompt)
    write_text(HERE/"outputs"/"few_prompt.txt",few_prompt)
    # END D21-02-I03
    # 해설 D21-02-I04: 예제 하나의 질문 표현만 바꾸고 새 버전으로 기록하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 기존 examples를 변경하지 않고 새 파일로 저장합니다.
    # BEGIN D21-02-I04
    replaced=json.loads(json.dumps(examples,ensure_ascii=False))
    replaced[0]["question"]="대여 장소를 알려 주세요."
    record={"version":"examples_few_v2","changed":"정상 예제 질문 표현 1개","hypothesis":"의미가 같은 표현에도 출력 계약을 유지하는지 관찰",
            "examples":replaced,"fixed_context":"knowledge_v1","fixed_schema":"answer_schema_v1"}
    save_version(HERE/"outputs"/"examples_few_v2.json",record)
    # END D21-02-I04
    print("[02] 예제·버전 설계 완료. 05는 예제 고정, 근거 규칙만 비교합니다.")
