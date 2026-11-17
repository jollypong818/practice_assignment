"""Day22 · 첫 실제 응답 | PPT 6~13 | 01_basic
공통 제공 코드는 교시 독립 시작점입니다. 본 파일의 TODO 함수를 실행 경로에 연결합니다.
"""
from pathlib import Path
import sys
HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))

from coursekit.support import parse_args, guarded, execute_case, emit
from coursekit.io import write_json

def make_first_request(model, instructions, question, selected, *, structured=False):
    # TODO D22-01-B01: 첫 요청의 model·instructions·input·출력 상한·store를 완성하세요.
    # 입력·완료 기준: 입력은 전달받은 값입니다. 새 질문·임의 모델을 하드코딩하지 않으며 JSON Schema는 다음 교시입니다.
    # BEGIN D22-01-B01
    # 해설: 입력은 전달받은 값입니다. 새 질문·임의 모델을 하드코딩하지 않으며 JSON Schema는 다음 교시입니다.
    request = {"model":model, "instructions":instructions, "input":question,
               "reasoning":{"effort":"none"}, "max_output_tokens":1200,
               "store":False, "service_tier":"default"}
    return request
    # END D22-01-B01

def create_response(client, request, stream=False):
    # TODO D22-01-B02: Responses API를 한 번 호출하고 반환값을 돌려주세요.
    # 입력·완료 기준: 키를 직접 문자열로 쓰지 않습니다. 한 함수 호출은 create 한 번만 수행합니다.
    # BEGIN D22-01-B02
    # 해설: 키를 직접 문자열로 쓰지 않습니다. 한 함수 호출은 create 한 번만 수행합니다.
    # 실제 SDK 호출 위치입니다. max_retries=0인 클라이언트를 제공받습니다.
    response = client.responses.create(**request, stream=stream)
    return response
    # END D22-01-B02

def make_view(result):
    # TODO D22-01-B03: 키 없이 source·model·종료 상태·응답 ID를 요약하세요.
    # 입력·완료 기준: 미실행이면 response_id는 None입니다. 0이나 가짜 응답 ID를 채우지 않습니다.
    # BEGIN D22-01-B03
    # 해설: 미실행이면 response_id는 None입니다. 0이나 가짜 응답 ID를 채우지 않습니다.
    last = result.get("attempts", [])[-1] if result.get("attempts") else {}
    return {"source_mode":result["source_mode"], "model":result.get("model"),
            "run_status":result["run_status"], "response_id":last.get("response_id")}
    # END D22-01-B03

# 강사용 핵심 해설
# model은 문서의 후보 식별자이며 계정 접근권까지 보장하지 않습니다.
# create 한 번은 전송 한 번입니다. 재시도는 공통 실행기 한 곳에서만 관리합니다.
# 첫 성공은 연결 확인이고, 사실에 맞는 답인지와 출력 계약은 별도 검사입니다.

def main():
    args=parse_args(HERE)
    result=execute_case(args,"FIRST",request_builder=make_first_request,hooks={"create":create_response})
    emit(args,result)
    view=make_view(result)
    write_json(args.output_dir/"connection_view.json",view)

if __name__=="__main__":
    guarded(main)
