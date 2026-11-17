"""Day21 실습 01: Prompt 구조와 요구사항. 실행: python main.py"""
from pathlib import Path
import sys
import json
from string import Template

HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))
from coursekit.io import DATA, read_json, write_json, write_text, run
from coursekit.prompting import CONTRACT_TEXT

# 기준: Day21 PPT 7~13장. 실제 모델 호출/실습 데이터 수정은 하지 않습니다.
# outputs는 실행 시 생성됩니다. 05/08의 모델 응답은 직접 수집한 원문만 등록합니다.

def build_requirements():
    # TODO D21-01-B01: 역할·작업·입력·제약·실패·출력 여섯 칸을 완성하세요.
    # 입력·대상: PPT 8장의 여섯 요소
    # 완료 기준: 6개 키가 모두 있고 각 문장이 비어 있지 않습니다.
    # 핵심: 역할을 전문가로 꾸미는 것과 정확한 근거를 제공하는 것은 다릅니다.
    # BEGIN D21-01-B01
    requirements = {
        "role": "",         # TODO: 누구를 돕는 작성자인가?
        "task": "",         # TODO: 어떤 질문에, 어떤 언어·길이로 답할까?
        "input": "",        # TODO: 질문과 선택 지식
        "constraints": "",  # TODO: 근거 범위와 예제 ID 사용 금지
        "failure": "",      # TODO: 없는 사실을 추측하지 않는 처리
        "output": "",       # TODO: 출력할 네 필드 이름
    }
    raise NotImplementedError("D21-01-B01: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-01-B01
    return requirements

def build_prompt(question, rows, requirements):
    # TODO D21-01-B02: Template에 질문·직렬화한 지식·출력 계약을 대입하세요.
    # 입력·대상: question, rows, requirements; CONTRACT_TEXT는 제공 코드
    # 완료 기준: 질문·지식 원문·네 필드 약속이 prompt에 있으며 $question이 남지 않습니다.
    # 핵심: 지식 본문은 데이터입니다. Template 대입은 코드 실행 또는 보안 권한 부여가 아닙니다.
    # BEGIN D21-01-B02
    context_json = json.dumps([], ensure_ascii=False)  # TODO: rows
    # JSON 중괄호와 충돌하지 않도록 $변수 형식인 Template을 사용합니다.
    template = Template("[역할] $role\n[작업] $task\n[입력] $input\n[질문] $question\n[지식 데이터] $context_json\n[제약] $constraints\n[실패] $failure\n[출력] $contract")
    prompt = template.substitute(
        **requirements,
        question="",           # TODO: question
        context_json="",       # TODO: 위 context_json
        contract=CONTRACT_TEXT,
    )
    raise NotImplementedError("D21-01-B02: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-01-B02
    return prompt

def main():
    requirements=build_requirements()
    rows=read_json(DATA / "knowledge_v1.json")[:1]
    prompt=build_prompt("파일을 어디에 보관하나요?",rows,requirements)
    # TODO D21-01-B03: 요구사항과 Prompt 원문을 저장하고 기준 질문을 확인하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: outputs/requirements.json 및 prompt.txt 생성. 아직 실제 모델 품질 결과는 없습니다.
    # BEGIN D21-01-B03
    assert len(requirements) == 6
    # TODO: prompt에 질문과 '개인 폴더'가 있는지 확인하세요.
    write_json(HERE / "outputs" / "requirements.json", {})  # TODO: requirements
    write_text(HERE / "outputs" / "prompt.txt", "")        # TODO: prompt
    raise NotImplementedError("D21-01-B03: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-01-B03
    print("[01] Prompt 요구사항과 원문 저장 완료. 모델 결과가 아닙니다.")

if __name__ == "__main__":
    run(main)
