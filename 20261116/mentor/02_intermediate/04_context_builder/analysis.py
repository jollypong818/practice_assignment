"""Day21 실습 04: Context 선택·예산. 실행: python main.py"""
from pathlib import Path
import sys
import json

HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))
from coursekit.io import DATA, read_json, write_json, write_text

# 기준: Day21 PPT 28~36장. 실제 모델 호출/실습 데이터 수정은 하지 않습니다.
# outputs는 실행 시 생성됩니다. 05/08의 모델 응답은 직접 수집한 원문만 등록합니다.

def select_context(rows, selected_ids):
    # 해설 D21-04-I01: 선택 ID의 순서를 보존해 지식을 골라 JSON으로 직렬화하세요.
    # 입력·대상: knowledge_v1 목록, selected_ids=[102]
    # 완료 기준: 102만 포함한 JSON. 없는 ID는 ValueError. 순서가 바뀌면 문맥도 달라집니다.
    # 핵심: ID 선택과 직렬화일 뿐 의미 검색·RAG를 구현한 것이 아닙니다.
    # BEGIN D21-04-I01
    by_id={row["id"]:row for row in rows}
    if len(by_id)!=len(rows):
        raise ValueError("중복 ID를 확인하세요")
    ids=list(dict.fromkeys(selected_ids))
    if any(i not in by_id for i in ids):
        raise ValueError("선택한 ID가 없습니다")
    chosen=[by_id[i] for i in ids]
    context_json=json.dumps(chosen,ensure_ascii=False)
    # END D21-04-I01
    return chosen, context_json

def calculate_budget():
    # 해설 D21-04-I02: PPT의 가상 token 예산에서 근거 문맥에 남는 공간을 구하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: available_for_context=4936
    # 핵심: 실제 모델 최대 길이나 측정 결과가 아닙니다. 입력 형식을 포함한 실제 token 측정은 별도입니다.
    # BEGIN D21-04-I02
    parts={"window":8192,"instructions_question":800,"examples":600,"output_reserve":1600,"margin":256}
    available=parts["window"]-parts["instructions_question"]-parts["examples"]-parts["output_reserve"]-parts["margin"]
    result={"source":"hypothetical_budget_not_model_measurement","parts":parts,"available_for_context":available}
    assert available==4936
    # END D21-04-I02
    return result

def main():
    rows=read_json(DATA/"knowledge_v1.json")
    chosen, context_json=select_context(rows,[102])
    budget=calculate_budget()
    # 해설 D21-04-I03: 포함·제외 ID와 원문·예산을 저장하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 포함 [102], 제외 101·103. 실제 입력 원문을 보존합니다.
    # BEGIN D21-04-I03
    included_ids=[r["id"] for r in chosen]
    excluded=[{"id":r["id"],"reason":"이번 서버 실행 질문에서 선택하지 않음"} for r in rows if r["id"] not in included_ids]
    manifest={"context_version":"knowledge_v1","included_ids":included_ids,"excluded":excluded,"budget":budget}
    write_text(HERE/"outputs"/"context.json",context_json)
    write_json(HERE/"outputs"/"context_manifest.json",manifest)
    # END D21-04-I03
    # 해설 D21-04-I04: 중복 선택은 제거하고, 스냅샷 중복 ID와 없는 ID는 오류인지 확인하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 중복 선택과 잘못된 원본 ID를 구분합니다.
    # BEGIN D21-04-I04
    dedup,_=select_context(rows,[102,102,101])
    assert [r["id"] for r in dedup]==[102,101]
    errors=[]
    for records,ids in [(rows,[999]),(rows+[rows[0]],[101])]:
        try:
            select_context(records,ids)
        except ValueError:
            errors.append(True)
        else:
            errors.append(False)
    assert all(errors)
    write_json(HERE/"outputs"/"selection_checks.json",{"dedup_ids":[r["id"] for r in dedup],"errors_detected":errors})
    # END D21-04-I04
    # 해설 D21-04-I05: 허용·유효성·관련성 검토를 선택 이유와 함께 적으세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: README의 예상 결과와 출력 파일을 대조합니다.
    # 핵심: 이 기록만으로 권한 통제가 구현된 것은 아닙니다. 자료 선정 정책을 설명하는 활동입니다.
    # BEGIN D21-04-I05
    policy={"permissions":"수업용 가상 지식만 사용","validity":"knowledge_v1 고정","relevance":"서버 실행 위치는 102",
            "order":"요청한 selected_ids의 첫 순서","excluded_when_over_budget":"중복·무관 정보부터 검토, 실제 tokenizer로 재측정 필요"}
    write_json(HERE/"outputs"/"context_policy.json",policy)
    # END D21-04-I05
    print("[04] Context와 가상 예산 저장 완료. token 실측·검색 결과가 아닙니다.")
