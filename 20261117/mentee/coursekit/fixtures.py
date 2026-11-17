"""직접 작성한 모의 응답. 실제 모델 출력·속도·사용량 측정치가 아닙니다."""
from types import SimpleNamespace
import copy
import json
from .errors import ProviderError
from .contracts import INSUFFICIENT


def namespace(obj):
    if isinstance(obj, dict):
        return SimpleNamespace(**{k: namespace(v) for k, v in obj.items()})
    if isinstance(obj, list):
        return [namespace(v) for v in obj]
    return obj


def response_for(case_id="H01", *, status="completed", raw=None, refusal=False, usage=True):
    answers = {
        "D02": {"status":"answered", "answer":"프로젝트 폴더에서 서버를 실행합니다.", "source_ids":[102], "missing_information":""},
        "D03": {"status":"insufficient_context", "answer":INSUFFICIENT, "source_ids":[], "missing_information":"보관 기간"},
        "H01": {"status":"answered", "answer":"오류 메시지와 시도한 작업을 함께 적습니다.", "source_ids":[103], "missing_information":""},
        "H02": {"status":"insufficient_context", "answer":INSUFFICIENT, "source_ids":[], "missing_information":"서버 접속 비밀번호"},
        "H03": {"status":"answered", "answer":"실습 파일은 개인 폴더에 보관하고 서버는 프로젝트 폴더에서 실행합니다. 질문에는 오류 메시지와 시도한 작업을 함께 적습니다.", "source_ids":[101,102,103], "missing_information":""},
    }
    text = ("API는 프로그램 사이에 요청과 결과를 전달하는 약속입니다." if case_id=="FIRST" else
            json.dumps(answers[case_id], ensure_ascii=False)) if raw is None else raw
    part = {"type":"refusal", "refusal":"모의 거절 응답"} if refusal else {"type":"output_text", "text":text, "annotations":[]}
    return namespace({"id": "simulated-response", "_request_id":"simulated-request",
        "status":status, "model":"fixture-model", "service_tier":"default",
        "output":[{"type":"message", "content":[part]}], "output_text":"" if refusal else text,
        "incomplete_details":{"reason":"max_output_tokens"} if status=="incomplete" else None,
        "usage": {"input_tokens":1000,"output_tokens":200,"total_tokens":1200,
                  "input_tokens_details":{"cached_tokens":400},"output_tokens_details":{"reasoning_tokens":0}} if usage else None})


def make_events(response, scenario="normal"):
    text = response.output_text
    result = [namespace({"type":"response.created"}), namespace({"type":"response.output_text.delta","delta":""})]
    if scenario == "error_event":
        return result + [namespace({"type":"error","code":"server_error"})]
    chunks = [text[:len(text)//2], text[len(text)//2:]]
    result.extend(namespace({"type":"response.output_text.delta","delta":c}) for c in chunks)
    if scenario in {"no_terminal", "interrupted"}:
        if scenario == "interrupted":
            result.append(ProviderError(kind="connection"))
        return result
    result.append(namespace({"type":"response.output_text.done","text":text}))
    kind = "response." + response.status
    result.append(namespace({"type":kind,"response":response}))
    return result


class FakeStream:
    def __init__(self, events, client):
        self.events, self.client = events, client
    def __enter__(self):
        return self
    def __exit__(self, *_):
        self.client.stream_closed = True
    def __iter__(self):
        for event in self.events:
            if isinstance(event, Exception):
                raise event
            yield event


class SimClient:
    """Responses.create와 같은 호출 면만 모사합니다. OpenAI SDK 자체 검증이 아닙니다."""
    def __init__(self, case_id="H01", steps=None, stream_scenario="normal"):
        self.case_id = case_id
        self.steps = list(steps) if steps is not None else [response_for(case_id)]
        self.stream_scenario = stream_scenario
        self.calls = []
        self.closed = False
        self.stream_closed = False
        self.responses = self
    def create(self, **kwargs):
        self.calls.append(copy.deepcopy(kwargs))
        if not self.steps:
            raise AssertionError("모의 응답을 초과하여 호출했습니다")
        step = self.steps.pop(0)
        if isinstance(step, Exception):
            raise step
        if kwargs.get("stream"):
            return FakeStream(make_events(step, self.stream_scenario), self)
        return step
    def close(self):
        self.closed = True


class VirtualClock:
    def __init__(self):
        self.value = 0.0
        self.sleeps = []
    def now(self):
        self.value += 0.001
        return self.value
    def sleep(self, seconds):
        self.sleeps.append(seconds)
        self.value += seconds
