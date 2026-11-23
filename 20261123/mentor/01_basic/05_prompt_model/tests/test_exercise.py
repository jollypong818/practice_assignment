"""로컬 입력·출력 계약만 검사합니다. 실제 모델/DB/네트워크를 호출하지 않습니다."""
from pathlib import Path
import importlib.util
import sys
import pytest

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE.parents[1]))


@pytest.fixture
def exercise():
    spec = importlib.util.spec_from_file_location("day26_05_B", HERE / "main.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableLambda
from coursekit.checkpoints import make_prompt


def test_prompt_then_model(exercise):
    calls = []
    def respond(value):
        calls.append(value)
        return AIMessage(content="로컬 검사 응답")
    inputs = exercise.make_inputs("질문 A", "[201] 원문 위치\n근거 A")
    assert inputs == {"question": "질문 A", "context": "[201] 원문 위치\n근거 A"}
    value, message = exercise.invoke_pair(make_prompt(), RunnableLambda(respond), inputs)
    assert type(value).__name__ == "ChatPromptValue"
    assert len(calls) == 1 and calls[0] is value
    messages = value.to_messages()
    assert [m.type for m in messages] == ["system", "human"]
    assert "질문 A" in messages[1].content and "근거 A" in messages[1].content
    assert isinstance(message, AIMessage) and message.text == "로컬 검사 응답"


def test_missing_key_stops_before_model(exercise):
    calls = []
    model = RunnableLambda(lambda value: calls.append(value))
    with pytest.raises(KeyError):
        exercise.invoke_pair(make_prompt(), model, {"question": "질문"})
    assert calls == []


def test_model_failure_is_not_an_answer(exercise):
    def fail(_):
        raise TimeoutError("로컬 테스트용")
    with pytest.raises(TimeoutError):
        exercise.invoke_pair(make_prompt(), RunnableLambda(fail),
                             exercise.make_inputs("질문", "근거"))
