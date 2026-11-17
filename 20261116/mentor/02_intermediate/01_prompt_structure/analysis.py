"""Day21 실습 01: Prompt 구조와 요구사항. 실행: python main.py"""
from pathlib import Path
import sys
import json
from string import Template

HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))
from coursekit.io import DATA, read_json, write_json, write_text
from coursekit.prompting import CONTRACT_TEXT

# 기준: Day21 PPT 7~13장. 실제 모델 호출/실습 데이터 수정은 하지 않습니다.
# outputs는 실행 시 생성됩니다. 05/08의 모델 응답은 직접 수집한 원문만 등록합니다.

def build_requirements():
    # 해설 D21-01-I01: 역할·작업·입력·제약·실패·출력 여섯 칸을 완성하세요.
    # 입력·대상: PPT 8장의 여섯 요소
    # 완료 기준: 6개 키가 모두 있고 각 문장이 비어 있지 않습니다.
    # 핵심: 역할을 전문가로 꾸미는 것과 정확한 근거를 제공하는 것은 다릅니다.
    # BEGIN D21-01-I01
    requirements = {
        "role": "초보 수강생의 실습 도움말 작성자",
        "task": "제공된 지식으로 질문에 한국어 2문장 이내로 답합니다.",
        "input": "사용자 질문과 선택한 지식 목록",
        "constraints": "제공된 근거만 사용하고 예제 ID를 답에 복사하지 않습니다.",
        "failure": "답을 뒷받침하는 사실이 없으면 정보 부족을 명시합니다.",
        "output": "status, answer, source_ids, missing_information 네 필드 JSON",
    }
    # END D21-01-I01
    return requirements

def build_prompt(question, rows, requirements):
    # 해설 D21-01-I02: 빈 질문과 필수 요구사항 누락을 먼저 거부하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 빈 질문/빈 조건을 유효 Prompt처럼 저장하지 않습니다.
    # BEGIN D21-01-I02
    if not question.strip():
        raise ValueError("빈 질문입니다")
    required = {"role", "task", "input", "constraints", "failure", "output"}
    if set(requirements) != required or any(not v.strip() for v in requirements.values()):
        raise ValueError("요구사항을 완성하세요")
    # END D21-01-I02
    # 해설 D21-01-I03: Template에 질문·직렬화한 지식·출력 계약을 대입하세요.
    # 입력·대상: question, rows, requirements; CONTRACT_TEXT는 제공 코드
    # 완료 기준: 질문·지식 원문·네 필드 약속이 prompt에 있으며 $question이 남지 않습니다.
    # 핵심: 지식 본문은 데이터입니다. Template 대입은 코드 실행 또는 보안 권한 부여가 아닙니다.
    # BEGIN D21-01-I03
    context_json = json.dumps(rows, ensure_ascii=False)
    template = Template("[역할] $role\n[작업] $task\n[입력] $input\n[질문] $question\n[지식 데이터] $context_json\n[제약] $constraints\n[실패] $failure\n[출력] $contract")
    prompt = template.substitute(**requirements, question=question, context_json=context_json, contract=CONTRACT_TEXT)
    # END D21-01-I03
    return prompt

def main():
    requirements=build_requirements()
    rows=read_json(DATA / "knowledge_v1.json")[:1]
    prompt=build_prompt("파일을 어디에 보관하나요?",rows,requirements)
    # 해설 D21-01-I04: 요구사항과 Prompt 원문을 저장하고 기준 질문을 확인하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: outputs/requirements.json 및 prompt.txt 생성. 아직 실제 모델 품질 결과는 없습니다.
    # BEGIN D21-01-I04
    assert len(requirements) == 6 and all(requirements.values())
    assert "파일을 어디에 보관하나요?" in prompt and "개인 폴더" in prompt
    write_json(HERE / "outputs" / "requirements.json", requirements)
    write_text(HERE / "outputs" / "prompt.txt", prompt)
    # END D21-01-I04
    # 해설 D21-01-I05: 정상·정보 부족 두 질문에 같은 요구사항을 적용하고 충돌 지시를 고치세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 두 Prompt의 질문만 달라집니다. 예상 행동과 실측을 구분합니다.
    # BEGIN D21-01-I05
    questions = ["파일을 어디에 보관하나요?", "파일은 몇 년 보관하나요?"]
    prompts = [build_prompt(q, rows, requirements) for q in questions]
    conflict = {"before":"근거가 없어도 반드시 숫자로 답한다.",
                "after":"기간 정보가 없으면 insufficient_context로 응답한다.",
                "reason":"추측 강제는 제공 근거만 사용하라는 규칙과 충돌한다."}
    write_json(HERE / "outputs" / "two_cases.json", {"prompts":prompts,"conflict_review":conflict})
    # END D21-01-I05
    print("[01] Prompt 요구사항과 원문 저장 완료. 모델 결과가 아닙니다.")
