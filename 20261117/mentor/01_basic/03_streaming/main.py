"""Day22 · Streaming과 완료 판정 | PPT 24~31 | 01_basic
공통 제공 코드는 교시 독립 시작점입니다. 본 파일의 TODO 함수를 실행 경로에 연결합니다.
"""
from pathlib import Path
import sys
HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))

from coursekit.support import parse_args, guarded, execute_case, emit
from coursekit.response import get

def receive_event(state, event, clock, started):
    state.events_seen += 1
    kind = get(event,"type")
    if kind == "response.output_text.delta":
        # TODO D22-03-B01: 비어 있지 않은 첫 텍스트의 시간과 delta를 누적하세요.
        # 입력·완료 기준: clock은 단조 시계입니다. 빈 delta를 첫 표시로 세지 않습니다.
        # BEGIN D22-03-B01
        # 해설: clock은 단조 시계입니다. 빈 delta를 첫 표시로 세지 않습니다.
        delta=get(event,"delta","")
        if not isinstance(delta,str):
            state.error="stream_protocol_error"
            return
        if delta and state.first_text_ms is None:
            state.first_text_ms=(clock()-started)*1000
        state.parts.append(delta)
        # END D22-03-B01
    elif kind in {"response.completed","response.incomplete","response.failed"}:
        # TODO D22-03-B02: 최종 이벤트의 Response를 보관하세요.
        # 입력·완료 기준: 부분 문자열을 합쳤다고 completed를 직접 만들어서는 안 됩니다.
        # BEGIN D22-03-B02
        # 해설: 부분 문자열을 합쳤다고 completed를 직접 만들어서는 안 됩니다.
        if state.final is not None:
            state.error="duplicate_terminal_event"
        state.final=get(event,"response")
        # END D22-03-B02
    elif kind == "error":
        state.error="stream_error"

def streaming_choice():
    # TODO D22-03-B03: 실제 스트리밍을 요청하도록 선택값을 반환하세요.
    # 입력·완료 기준: 메시지 UI를 새로 만드는 실습이 아닙니다. 최종 상태·부분 파일·first_text_ms를 확인합니다.
    # BEGIN D22-03-B03
    # 해설: 메시지 UI를 새로 만드는 실습이 아닙니다. 최종 상태·부분 파일·first_text_ms를 확인합니다.
    return True
    # END D22-03-B03

# 강사용 핵심 해설
# delta는 텍스트 조각이며 Token 1개와 대응하지 않습니다. 조각 수로 비용을 계산하지 않습니다.
# first_text_ms는 첫 비어 있지 않은 delta를 관측한 시간입니다. 소켓 연결 완료 시간과 다릅니다.
# output_text.done은 문자열 한 부분의 종료일 수 있습니다. 최종 Response의 상태도 확인해야 합니다.
# 중간 출력은 콘솔에 미검증으로 표시하며 DB·캐시에 저장 승인하지 않습니다.

def main():
    args=parse_args(HERE)
    modes=[streaming_choice()]
    observations=[]
    for use_stream in modes:
        result=execute_case(args,args.case or "H01",stream=use_stream,hooks={"event":receive_event})
        emit(args,result)

if __name__=="__main__":
    guarded(main)
