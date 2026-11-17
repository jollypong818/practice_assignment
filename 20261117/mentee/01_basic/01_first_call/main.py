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
    request = {"model": None, "instructions": instructions, "input": None,
               "reasoning": {"effort": "none"}, "max_output_tokens": None,
               "store": None, "service_tier": "default"}
    # model은 전달값, input은 question, 출력 상한1200, store=False
    raise NotImplementedError("D22-01-B01: TODO를 완성하고 이 raise를 제거하세요")
    return request  # 위 TODO와 raise 제거를 마친 뒤 반환합니다.
    # END D22-01-B01

def create_response(client, request, stream=False):
    # TODO D22-01-B02: Responses API를 한 번 호출하고 반환값을 돌려주세요.
    # 입력·완료 기준: 키를 직접 문자열로 쓰지 않습니다. 한 함수 호출은 create 한 번만 수행합니다.
    # BEGIN D22-01-B02
    options = dict(request)  # 힌트: 이미 만든 요청 딕셔너리
    response = None  # 힌트: client.responses.create(**options, stream=stream)
    raise NotImplementedError("D22-01-B02: TODO를 완성하고 이 raise를 제거하세요")
    return response  # 위 TODO와 raise 제거를 마친 뒤 반환합니다.
    # END D22-01-B02

def make_view(result):
    # TODO D22-01-B03: 키 없이 source·model·종료 상태·응답 ID를 요약하세요.
    # 입력·완료 기준: 미실행이면 response_id는 None입니다. 0이나 가짜 응답 ID를 채우지 않습니다.
    # BEGIN D22-01-B03
    last = result.get("attempts", [])[-1] if result.get("attempts") else {}
    summary = {"source_mode": None, "model": None, "run_status": None, "response_id": None}
    # 힌트: result와 last에서 같은 필드명을 읽습니다.
    raise NotImplementedError("D22-01-B03: TODO를 완성하고 이 raise를 제거하세요")
    return summary  # 위 TODO와 raise 제거를 마친 뒤 반환합니다.
    # END D22-01-B03

def main():
    args=parse_args(HERE)
    result=execute_case(args,"FIRST",request_builder=make_first_request,hooks={"create":create_response})
    emit(args,result)
    view=make_view(result)
    write_json(args.output_dir/"connection_view.json",view)

if __name__=="__main__":
    guarded(main)
