"""Day22 · Streaming과 완료 판정 | PPT 24~31 | 02_intermediate
공통 제공 코드는 교시 독립 시작점입니다. 본 파일의 TODO 함수를 실행 경로에 연결합니다.
"""
from pathlib import Path
from coursekit.support import parse_args, execute_case, emit
from coursekit.io import write_json
from coursekit.response import get

def receive_event(state, event, clock, started):
    state.events_seen += 1
    kind = get(event,"type")
    if kind == "response.output_text.delta":
        # TODO D22-03-I01: 비어 있지 않은 첫 텍스트의 시간과 delta를 누적하세요.
        # 입력·완료 기준: clock은 단조 시계입니다. 빈 delta를 첫 표시로 세지 않습니다.
        # BEGIN D22-03-I01
        # 해설: clock은 단조 시계입니다. 빈 delta를 첫 표시로 세지 않습니다.
        delta=get(event,"delta","")
        if not isinstance(delta,str):
            state.error="stream_protocol_error"
            return
        if delta and state.first_text_ms is None:
            state.first_text_ms=(clock()-started)*1000
        state.parts.append(delta)
        # END D22-03-I01
    elif kind in {"response.completed","response.incomplete","response.failed"}:
        # TODO D22-03-I02: 최종 이벤트의 Response를 보관하세요.
        # 입력·완료 기준: 부분 문자열을 합쳤다고 completed를 직접 만들어서는 안 됩니다.
        # BEGIN D22-03-I02
        # 해설: 부분 문자열을 합쳤다고 completed를 직접 만들어서는 안 됩니다.
        if state.final is not None:
            state.error="duplicate_terminal_event"
        state.final=get(event,"response")
        # END D22-03-I02
    elif kind == "error":
        state.error="stream_error"

def streaming_choice():
    # TODO D22-03-I03: 실제 스트리밍을 요청하도록 선택값을 반환하세요.
    # 입력·완료 기준: 메시지 UI를 새로 만드는 실습이 아닙니다. 최종 상태·부분 파일·first_text_ms를 확인합니다.
    # BEGIN D22-03-I03
    # 해설: 메시지 UI를 새로 만드는 실습이 아닙니다. 최종 상태·부분 파일·first_text_ms를 확인합니다.
    return True
    # END D22-03-I03

def compare_runs():
    # TODO D22-03-I04: 동일 입력의 비스트리밍과 스트리밍 순서를 지정하세요.
    # 입력·완료 기준: --action compare에서만 2회 호출합니다. 기본 run은 스트리밍1회입니다.
    # BEGIN D22-03-I04
    # 해설: --action compare에서만 2회 호출합니다. 기본 run은 스트리밍1회입니다.
    return [False, True]
    # END D22-03-I04

def timing_view(result):
    # TODO D22-03-I05: 첫 표시 시간과 전체 요청 시간을 분리해 요약하세요.
    # 입력·완료 기준: 미표시인 None과 실제 관측0은 다릅니다. 시뮬레이션 시간을 실제 LLM 속도로 해석하지 않습니다.
    # BEGIN D22-03-I05
    # 해설: 미표시인 None과 실제 관측0은 다릅니다. 시뮬레이션 시간을 실제 LLM 속도로 해석하지 않습니다.
    return {"source_mode":result["source_mode"],"first_text_ms":result.get("first_text_ms"),
            "request_ms":result.get("request_ms"),"e2e_ms":result.get("e2e_ms")}
    # END D22-03-I05

HERE = Path(__file__).resolve().parent

def main():
    args=parse_args(HERE)
    modes=compare_runs() if args.action=="compare" else [streaming_choice()]
    observations=[]
    for use_stream in modes:
        result=execute_case(args,args.case or "H01",stream=use_stream,hooks={"event":receive_event})
        emit(args,result)
        observations.append(timing_view(result))
    write_json(args.output_dir/"timing_comparison.json",observations)
