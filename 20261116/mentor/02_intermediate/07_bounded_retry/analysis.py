"""Day21 실습 07: 실패 분류·최대 2회. 실행: python main.py"""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))
from coursekit.io import DATA, read_json, write_json, sha_text

# 기준: Day21 PPT 56~63장. 실제 모델 호출/실습 데이터 수정은 하지 않습니다.
# outputs는 실행 시 생성됩니다. 05/08의 모델 응답은 직접 수집한 원문만 등록합니다.
from coursekit.retry import FixtureProvider, run_fixture_scenarios
from coursekit.contracts import validate_answer

def repair_prompt(original, error):
    # 해설 D21-07-I01: 허용한 형식 오류만 안전한 한 문장 요약으로 수정 요청을 만드세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: unknown_source는 자동 형식 수정 요청을 만들지 않습니다.
    # BEGIN D21-07-I01
    safe={"json_error":"JSON 객체 하나를 코드 블록 없이 출력하세요.",
          "schema_error":"필수 필드·자료형·길이를 지키세요. source_ids는 양의 정수 목록입니다."}
    if error not in safe:
        raise ValueError("형식 오류만 수정 요청을 만듭니다")
    repaired=original+"\n[수정 요청] 같은 질문·지식·계약을 유지하세요. "+safe[error]+" 부족한 사실은 만들지 마세요."
    # END D21-07-I01
    return repaired

def run_with_retry(generate, prompt, validate):
    # 해설 D21-07-I02: 최초 1회+수정 1회까지만 반복하고 통과하지 못하면 None을 반환하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 호출 수가 최대 2. 정상 정보 부족도 1회에 종료.
    # 핵심: 성공 반환은 자동 구조·참조 통과일 뿐입니다. 근거를 맞게 읽었는지 사람 검토가 남습니다.
    # BEGIN D21-07-I02
    history=[]
    for attempt in (1,2):
        raw=generate(prompt)
        obj,error=validate(raw)
        history.append({"attempt":attempt,"error":error,"raw_text":raw,"prompt_sha256":sha_text(prompt)})
        if error is None:
            return obj,history
        if error not in {"json_error","schema_error"} or attempt==2:
            break
        prompt=repair_prompt(prompt,error)
    return None,history
    # END D21-07-I02

def main():
    fixtures=read_json(DATA/"validation_fixtures.json")
    # 해설 D21-07-I03: 네 fixture 순서의 호출 수 2·2·1·1을 확인하고 기록하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 복구 성공·연속 실패·규칙 중단·부족 정상 종료 네 경우.
    # BEGIN D21-07-I03
    results=run_fixture_scenarios(fixtures,runner=run_with_retry)
    assert [x["calls"] for x in results]==[2,2,1,1]
    write_json(HERE/"outputs"/"retry_results.json",{"source_mode":"fixture","results":results})
    # END D21-07-I03
    # 해설 D21-07-I04: 첫 응답과 재시도 후 결과를 다른 필드로 집계하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 처음 실패→나중 통과를 첫 응답 통과로 집계하지 않습니다.
    # BEGIN D21-07-I04
    rows=[]
    for item in results:
        history=item["history"]
        rows.append({"scenario":item["scenario"],"first_error":history[0]["error"],
                     "attempts":len(history),"final_auto_ok":item["auto_accepted"],"source_mode":"fixture"})
    write_json(HERE/"outputs"/"first_vs_final.json",rows)
    # END D21-07-I04
    # 해설 D21-07-I05: 마지막 실패 뒤에는 수정 요청이 더 만들어지지 않는지 확인하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: README의 예상 결과와 출력 파일을 대조합니다.
    # 핵심: 이 범위는 완료된 문자열을 받은 뒤입니다. 공급자 거절·통신 재시도는 내일 다룹니다.
    # BEGIN D21-07-I05
    bad=next(x["raw_text"] for x in fixtures if x["fixture_id"]=="broken_json")
    provider=FixtureProvider([bad,bad])
    obj,history=run_with_retry(provider,"original",lambda raw:validate_answer(raw,[101]))
    assert obj is None and provider.calls==2
    assert len(provider.prompts)==2
    assert provider.prompts[1].count("[수정 요청]")==1
    write_json(HERE/"outputs"/"termination.json",{"calls":provider.calls,"success_object":None})
    # END D21-07-I05
    print("[07] 제어 흐름만 검증했습니다. 실제 모델 복구율은 측정하지 않았습니다.")
