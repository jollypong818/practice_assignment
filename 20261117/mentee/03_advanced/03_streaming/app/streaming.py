"""Day22 · Streaming과 완료 판정 | PPT 24~31 | 03_advanced
공통 제공 코드는 교시 독립 시작점입니다. 본 파일의 TODO 함수를 실행 경로에 연결합니다.
"""
from coursekit.response import get

def receive_event(state, event, clock, started):
    state.events_seen += 1
    kind = get(event,"type")
    if kind == "response.output_text.delta":
        # TODO D22-03-A01: 비어 있지 않은 첫 텍스트의 시간과 delta를 누적하세요.
        # 입력·완료 기준: clock은 단조 시계입니다. 빈 delta를 첫 표시로 세지 않습니다.
        # BEGIN D22-03-A01
        delta = get(event, "delta", "")
        if delta and state.first_text_ms is None:
            pass  # (clock() - started) * 1000
        # state.parts.append(...)로 누적. delta 개수는 Token 수가 아닙니다.
        raise NotImplementedError("D22-03-A01: TODO를 완성하고 이 raise를 제거하세요")
        # END D22-03-A01
    elif kind in {"response.completed","response.incomplete","response.failed"}:
        # TODO D22-03-A02: 최종 이벤트의 Response를 보관하세요.
        # 입력·완료 기준: 부분 문자열을 합쳤다고 completed를 직접 만들어서는 안 됩니다.
        # BEGIN D22-03-A02
        # 중복 terminal이면 오류, 아니면 state.final에 event.response 저장
        final_response = get(event, "response")
        raise NotImplementedError("D22-03-A02: TODO를 완성하고 이 raise를 제거하세요")
        # END D22-03-A02
    elif kind == "error":
        state.error="stream_error"

def streaming_choice():
    # TODO D22-03-A03: 실제 스트리밍을 요청하도록 선택값을 반환하세요.
    # 입력·완료 기준: 메시지 UI를 새로 만드는 실습이 아닙니다. 최종 상태·부분 파일·first_text_ms를 확인합니다.
    # BEGIN D22-03-A03
    use_stream = None  # True이면 Responses stream=True
    raise NotImplementedError("D22-03-A03: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-03-A03

def compare_runs():
    # TODO D22-03-A04: 동일 입력의 비스트리밍과 스트리밍 순서를 지정하세요.
    # 입력·완료 기준: --action compare에서만 2회 호출합니다. 기본 run은 스트리밍1회입니다.
    # BEGIN D22-03-A04
    modes = []  # 두 경우만 비교하며 출력 문장 일치를 강요하지 않습니다.
    raise NotImplementedError("D22-03-A04: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-03-A04

def timing_view(result):
    # TODO D22-03-A05: 첫 표시 시간과 전체 요청 시간을 분리해 요약하세요.
    # 입력·완료 기준: 미표시인 None과 실제 관측0은 다릅니다. 시뮬레이션 시간을 실제 LLM 속도로 해석하지 않습니다.
    # BEGIN D22-03-A05
    view = {}  # 각 값은 result에서 읽고 None을0으로 바꾸지 않습니다.
    raise NotImplementedError("D22-03-A05: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-03-A05

def check_no_terminal():
    # TODO D22-03-A06: 완료 이벤트가 없으면 최종 Response가 없는지 모의 검사하세요.
    # 입력·완료 기준: raw가 있다는 이유로 성공 처리하지 않는 분기 검사입니다.
    # BEGIN D22-03-A06
    from coursekit.response import StreamState
    from coursekit.fixtures import namespace
    state = StreamState()
    # delta 이벤트만 전달하고 final이 없는지 확인합니다.
    raise NotImplementedError("D22-03-A06: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-03-A06
