"""현재 폴더의 구현만 검사합니다. API·DB·다운로드는 실행하지 않습니다."""
import importlib.util
from pathlib import Path
import sys
from copy import deepcopy
import pytest

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE.parents[1]))
from coursekit.data import example_hit, load_hits

MODULE_PATH = HERE / "main.py"
SPEC = importlib.util.spec_from_file_location("d26_mentor_3_B", MODULE_PATH)
m = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = m
SPEC.loader.exec_module(m)

def test_data_and_execution_roles_are_distinct():
    access = m.access_kinds()
    assert access == {"Document": "data", "Retriever": "invoke", "Prompt": "invoke", "Chat Model": "invoke"}

def test_prompt_output_is_not_model_output():
    outputs = m.component_outputs()
    assert set(outputs) == {"Document", "Retriever", "Prompt", "Chat Model"}
    assert outputs["Retriever"] == "list[Document]"
    assert outputs["Prompt"] == "ChatPromptValue"
    assert outputs["Chat Model"] == "AIMessage"
