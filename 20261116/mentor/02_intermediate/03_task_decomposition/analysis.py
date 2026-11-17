"""Day21 실습 03: 작업 분해와 정보 부족. 실행: python main.py"""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))
from coursekit.io import DATA, read_json, write_json, write_text

# 기준: Day21 PPT 21~27장. 실제 모델 호출/실습 데이터 수정은 하지 않습니다.
# outputs는 실행 시 생성됩니다. 05/08의 모델 응답은 직접 수집한 원문만 등록합니다.

def analyze_card(card):
    # 해설 D21-03-I01: 질문이 요구하는 사실과, 제공 자료가 지원하는 사실을 구분하세요.
    # 입력·대상: 교사가 작성한 required/supported/conflicts 카드
    # 완료 기준: C01 missing=[], C02 missing=[보관 기간]
    # 핵심: 이 코드는 자유로운 질문의 의미를 자동 이해하지 않습니다. 명시된 판단 카드를 처리합니다.
    # BEGIN D21-03-I01
    required=list(card["required"])
    supported=card["supported"]
    missing=[fact for fact in required if fact not in supported]
    conflicts=list(card["conflicts"])
    # END D21-03-I01
    # 해설 D21-03-I02: 하나라도 근거가 부족하면 수업의 정보 부족 상태를 선택하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: README의 예상 결과와 출력 파일을 대조합니다.
    # 핵심: 오늘 계약은 부분 답변을 새 상태로 추가하지 않습니다. 충분한 근거가 없으면 명시적으로 멈춥니다.
    # BEGIN D21-03-I02
    status="insufficient_context" if missing or conflicts else "answered"
    source_ids=[]
    if status=="answered":
        for fact in required:
            source_ids.extend(supported[fact])
    source_ids=list(dict.fromkeys(source_ids))
    result={"case_id":card["case_id"],"required":required,"supported_facts":list(supported),
            "missing":missing,"conflicts":conflicts,"status":status,"source_ids":source_ids,
            "basis":"teacher_authored_fact_card"}
    # END D21-03-I02
    return result

def main():
    cards=read_json(DATA/"decomposition_cards.json")
    # 해설 D21-03-I03: 정상·정보 부족의 판단과 최종 출력 지시를 저장하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 2개 결과와 작업 지시를 저장합니다. 모델 추론 관찰 기록이 아닙니다.
    # BEGIN D21-03-I03
    results=[analyze_card(c) for c in cards[:2]]
    instruction="질문이 요구하는 사실과 근거를 대조하세요. 부족하면 추측하지 말고 필요한 정보를 적으세요. 내부 사고 기록 대신 최종 JSON만 반환하세요."
    assert results[0]["status"]=="answered" and results[1]["status"]=="insufficient_context"
    write_json(HERE/"outputs"/"task_cards.json",results)
    write_text(HERE/"outputs"/"task_instruction.txt",instruction)
    # END D21-03-I03
    # 해설 D21-03-I04: 위치와 기간을 함께 묻는 질문에서 빠진 사실을 확인하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 없는 보관 기간을 위치 정보로 추측하지 않습니다.
    # BEGIN D21-03-I04
    compound=analyze_card(cards[2])
    assert compound["missing"]==["보관 기간"]
    assert compound["status"]=="insufficient_context" and compound["source_ids"]==[]
    write_json(HERE/"outputs"/"compound_case.json",compound)
    # END D21-03-I04
    print("[03] 판단 카드 완료. 근거 대조는 사람의 판단이 포함됩니다.")
