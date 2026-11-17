"""Day22 · 메시지와 출력 계약 | PPT 14~23 | 03_advanced
공통 제공 코드는 교시 독립 시작점입니다. 본 파일의 TODO 함수를 실행 경로에 연결합니다.
"""
import json
from coursekit.request import WireAnswer, OUTPUT_FORMAT, build_request as checkpoint_request
from coursekit.response import get, output_text

def make_request(model, instructions, question, selected, *, structured=True):
    # TODO D22-02-A01: 질문과 선택 지식만 user input으로 직렬화하세요.
    # 입력·완료 기준: selected_ids가 아닌 선택된 지식의 id·title·content·category를 보냅니다. expected_behavior는 넣지 않습니다.
    # BEGIN D22-02-A01
    payload = {"question": question, "knowledge": []}  # 이번 selected를 넣습니다.
    serialized = ""  # json.dumps(..., ensure_ascii=False)
    raise NotImplementedError("D22-02-A01: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-02-A01
    # TODO D22-02-A02: 공급자용 Schema를 요청의 text.format으로 연결하세요.
    # 입력·완료 기준: response_format이 아니라 Responses의 text.format입니다. Wire와 로컬 KnowledgeAnswer는 다릅니다.
    # BEGIN D22-02-A02
    request = checkpoint_request(model, instructions, question, selected, structured=False)
    request["input"] = []  # role="user", content=serialized
    request["text"] = {}   # {"format": OUTPUT_FORMAT}
    raise NotImplementedError("D22-02-A02: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-02-A02

def response_gate(response):
    # TODO D22-02-A03: 거절 콘텐츠와 미완료 상태를 먼저 구분하세요.
    # 입력·완료 기준: API status와 answer JSON의 status는 다릅니다. 거절을 형식 오류로 바꾸지 않습니다.
    # BEGIN D22-02-A03
    for item in get(response, "output", []) or []:
        if get(item, "type") == "message":
            for part in get(item, "content", []) or []:
                pass  # refusal이면 None, "refused" 반환
    status = get(response, "status")  # completed가 아니면 오류 반환
    raise NotImplementedError("D22-02-A03: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-02-A03
    # TODO D22-02-A04: 완료 응답에서도 빈 본문을 검사한 뒤 원문을 반환하세요.
    # 입력·완료 기준: 원문을 수정해 유효한 JSON처럼 만들지 않습니다. 로컬 검증기는 다음 단계에서 실행됩니다.
    # BEGIN D22-02-A04
    raw = output_text(response)
    # 힌트: 공백을 제거한 결과가 비어 있으면 (None, "empty_output")
    raise NotImplementedError("D22-02-A04: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-02-A04

def choose_cases():
    # TODO D22-02-A05: 정상 질문 D02와 정보 부족 질문 D03의 순서를 지정하세요.
    # 입력·완료 기준: 실제 호출 2개입니다. 부족 응답은 유효한 업무 결과일 수 있습니다.
    # BEGIN D22-02-A05
    cases = []  # D02는102, D03은101을 제공합니다.
    raise NotImplementedError("D22-02-A05: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-02-A05

def check_wire_schema():
    # TODO D22-02-A06: Wire Schema의 네 필드 필수·추가 필드 금지를 검사하세요.
    # 입력·완료 기준: 이 검사로 로컬 길이·출처·사실성 규칙까지 통과했다고 말하지 않습니다.
    # BEGIN D22-02-A06
    schema = WireAnswer.model_json_schema()
    raise NotImplementedError("D22-02-A06: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-02-A06
