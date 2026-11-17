"""Day22 · 첫 실제 응답 | PPT 6~13 | 02_intermediate
공통 제공 코드는 교시 독립 시작점입니다. 본 파일의 TODO 함수를 실행 경로에 연결합니다.
"""
from pathlib import Path
from coursekit.support import parse_args, execute_case, emit
from coursekit.io import write_json

def make_first_request(model, instructions, question, selected, *, structured=False):
    # TODO D22-01-I01: 첫 요청의 model·instructions·input·출력 상한·store를 완성하세요.
    # 입력·완료 기준: 입력은 전달받은 값입니다. 새 질문·임의 모델을 하드코딩하지 않으며 JSON Schema는 다음 교시입니다.
    # BEGIN D22-01-I01
    # 해설: 입력은 전달받은 값입니다. 새 질문·임의 모델을 하드코딩하지 않으며 JSON Schema는 다음 교시입니다.
    request = {"model":model, "instructions":instructions, "input":question,
               "reasoning":{"effort":"none"}, "max_output_tokens":1200,
               "store":False, "service_tier":"default"}
    return request
    # END D22-01-I01

def create_response(client, request, stream=False):
    # TODO D22-01-I02: Responses API를 한 번 호출하고 반환값을 돌려주세요.
    # 입력·완료 기준: 키를 직접 문자열로 쓰지 않습니다. 한 함수 호출은 create 한 번만 수행합니다.
    # BEGIN D22-01-I02
    # 해설: 키를 직접 문자열로 쓰지 않습니다. 한 함수 호출은 create 한 번만 수행합니다.
    # 실제 SDK 호출 위치입니다. max_retries=0인 클라이언트를 제공받습니다.
    response = client.responses.create(**request, stream=stream)
    return response
    # END D22-01-I02

def make_view(result):
    # TODO D22-01-I03: 키 없이 source·model·종료 상태·응답 ID를 요약하세요.
    # 입력·완료 기준: 미실행이면 response_id는 None입니다. 0이나 가짜 응답 ID를 채우지 않습니다.
    # BEGIN D22-01-I03
    # 해설: 미실행이면 response_id는 None입니다. 0이나 가짜 응답 ID를 채우지 않습니다.
    last = result.get("attempts", [])[-1] if result.get("attempts") else {}
    return {"source_mode":result["source_mode"], "model":result.get("model"),
            "run_status":result["run_status"], "response_id":last.get("response_id")}
    # END D22-01-I03

def setting_cases():
    # TODO D22-01-I04: 키 미설정과 모델 접근 오류의 차이를 모의 비교표에 적으세요.
    # 입력·완료 기준: 반복 실제 호출로 오류를 만들지 않습니다. 모델 접근 거부는 403/404 등 공급자 원인을 봅니다.
    # BEGIN D22-01-I04
    # 해설: 반복 실제 호출로 오류를 만들지 않습니다. 모델 접근 거부는 403/404 등 공급자 원인을 봅니다.
    return [{"case":"missing_key","where":"local_settings","new_api_send_count":0},
            {"case":"model_denied","where":"provider_permission","simulated_send_count":1}]
    # END D22-01-I04

HERE = Path(__file__).resolve().parent

def main():
    args=parse_args(HERE)
    result=execute_case(args,"FIRST",request_builder=make_first_request,hooks={"create":create_response})
    emit(args,result)
    view=make_view(result)
    write_json(args.output_dir/"connection_view.json",view)
    write_json(args.output_dir/"settings_cases.json",setting_cases())
