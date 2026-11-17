"""Day22 · 첫 실제 응답 | PPT 6~13 | 03_advanced
공통 제공 코드는 교시 독립 시작점입니다. 본 파일의 TODO 함수를 실행 경로에 연결합니다.
"""

def make_first_request(model, instructions, question, selected, *, structured=False):
    # TODO D22-01-A01: 첫 요청의 model·instructions·input·출력 상한·store를 완성하세요.
    # 입력·완료 기준: 입력은 전달받은 값입니다. 새 질문·임의 모델을 하드코딩하지 않으며 JSON Schema는 다음 교시입니다.
    # BEGIN D22-01-A01
    # 해설: 입력은 전달받은 값입니다. 새 질문·임의 모델을 하드코딩하지 않으며 JSON Schema는 다음 교시입니다.
    request = {"model":model, "instructions":instructions, "input":question,
               "reasoning":{"effort":"none"}, "max_output_tokens":1200,
               "store":False, "service_tier":"default"}
    return request
    # END D22-01-A01

def create_response(client, request, stream=False):
    # TODO D22-01-A02: Responses API를 한 번 호출하고 반환값을 돌려주세요.
    # 입력·완료 기준: 키를 직접 문자열로 쓰지 않습니다. 한 함수 호출은 create 한 번만 수행합니다.
    # BEGIN D22-01-A02
    # 해설: 키를 직접 문자열로 쓰지 않습니다. 한 함수 호출은 create 한 번만 수행합니다.
    # 실제 SDK 호출 위치입니다. max_retries=0인 클라이언트를 제공받습니다.
    response = client.responses.create(**request, stream=stream)
    return response
    # END D22-01-A02

def make_view(result):
    # TODO D22-01-A03: 키 없이 source·model·종료 상태·응답 ID를 요약하세요.
    # 입력·완료 기준: 미실행이면 response_id는 None입니다. 0이나 가짜 응답 ID를 채우지 않습니다.
    # BEGIN D22-01-A03
    # 해설: 미실행이면 response_id는 None입니다. 0이나 가짜 응답 ID를 채우지 않습니다.
    last = result.get("attempts", [])[-1] if result.get("attempts") else {}
    return {"source_mode":result["source_mode"], "model":result.get("model"),
            "run_status":result["run_status"], "response_id":last.get("response_id")}
    # END D22-01-A03

def setting_cases():
    # TODO D22-01-A04: 키 미설정과 모델 접근 오류의 차이를 모의 비교표에 적으세요.
    # 입력·완료 기준: 반복 실제 호출로 오류를 만들지 않습니다. 모델 접근 거부는 403/404 등 공급자 원인을 봅니다.
    # BEGIN D22-01-A04
    # 해설: 반복 실제 호출로 오류를 만들지 않습니다. 모델 접근 거부는 403/404 등 공급자 원인을 봅니다.
    return [{"case":"missing_key","where":"local_settings","new_api_send_count":0},
            {"case":"model_denied","where":"provider_permission","simulated_send_count":1}]
    # END D22-01-A04

def check_safe_view(view):
    # TODO D22-01-A05: 기록할 필드를 허용 목록으로 제한하는 assertion을 완성하세요.
    # 입력·완료 기준: 설정 객체 전체를 JSON에 넣지 않습니다. 필드 허용 목록은 내용의 전면적 비밀 탐지기가 아닙니다.
    # BEGIN D22-01-A05
    # 해설: 설정 객체 전체를 JSON에 넣지 않습니다. 필드 허용 목록은 내용의 전면적 비밀 탐지기가 아닙니다.
    assert set(view) == {"source_mode","model","run_status","response_id"}
    assert "api_key" not in view and "Authorization" not in view
    return True
    # END D22-01-A05
