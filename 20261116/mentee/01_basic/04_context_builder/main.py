"""Day21 실습 04: Context 선택·예산. 실행: python main.py"""
from pathlib import Path
import sys
import json

HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))
from coursekit.io import DATA, read_json, write_json, write_text, run

# 기준: Day21 PPT 28~36장. 실제 모델 호출/실습 데이터 수정은 하지 않습니다.
# outputs는 실행 시 생성됩니다. 05/08의 모델 응답은 직접 수집한 원문만 등록합니다.

def select_context(rows, selected_ids):
    # TODO D21-04-B01: 선택 ID의 순서를 보존해 지식을 골라 JSON으로 직렬화하세요.
    # 입력·대상: knowledge_v1 목록, selected_ids=[102]
    # 완료 기준: 102만 포함한 JSON. 없는 ID는 ValueError. 순서가 바뀌면 문맥도 달라집니다.
    # 핵심: ID 선택과 직렬화일 뿐 의미 검색·RAG를 구현한 것이 아닙니다.
    # BEGIN D21-04-B01
    by_id = {row["id"]:row for row in rows}
    if len(by_id) != len(rows):
        raise ValueError("중복 ID를 확인하세요")
    ids = list(dict.fromkeys(selected_ids))  # 중복 선택은 첫 순서만 남김
    if any(i not in by_id for i in ids):
        raise ValueError("선택한 ID가 없습니다")
    chosen = []
    for knowledge_id in ids:
        chosen.append(None)  # TODO: by_id[knowledge_id]
    context_json = json.dumps([], ensure_ascii=False)  # TODO: chosen
    raise NotImplementedError("D21-04-B01: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-04-B01
    return chosen, context_json

def calculate_budget():
    # TODO D21-04-B02: PPT의 가상 token 예산에서 근거 문맥에 남는 공간을 구하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: available_for_context=4936
    # 핵심: 실제 모델 최대 길이나 측정 결과가 아닙니다. 입력 형식을 포함한 실제 token 측정은 별도입니다.
    # BEGIN D21-04-B02
    parts = {"window":8192,"instructions_question":800,"examples":600,"output_reserve":1600,"margin":256}
    available = 0  # TODO: window에서 지시·질문, 예제, 출력 예약, 여유를 뺍니다.
    result = {"source":"hypothetical_budget_not_model_measurement", "parts":parts, "available_for_context":available}
    # TODO: 결과 4936과 비교. len(text)를 token 수라고 부르지 마세요.
    raise NotImplementedError("D21-04-B02: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-04-B02
    return result

def main():
    rows=read_json(DATA/"knowledge_v1.json")
    chosen, context_json=select_context(rows,[102])
    budget=calculate_budget()
    # TODO D21-04-B03: 포함·제외 ID와 원문·예산을 저장하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 포함 [102], 제외 101·103. 실제 입력 원문을 보존합니다.
    # BEGIN D21-04-B03
    included_ids = []  # TODO: chosen의 id 목록
    excluded = []
    for row in rows:
        if row["id"] not in included_ids:
            excluded.append({"id":row["id"], "reason":""})  # TODO: 제외 이유
    manifest = {"context_version":"knowledge_v1", "included_ids":included_ids, "excluded":excluded, "budget":budget}
    write_text(HERE/"outputs"/"context.json", "")  # TODO: context_json
    write_json(HERE/"outputs"/"context_manifest.json", manifest)
    raise NotImplementedError("D21-04-B03: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-04-B03
    print("[04] Context와 가상 예산 저장 완료. token 실측·검색 결과가 아닙니다.")

if __name__ == "__main__":
    run(main)
