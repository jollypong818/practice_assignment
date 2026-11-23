"""현재 폴더의 구현만 검사합니다. API·DB·다운로드는 실행하지 않습니다."""
import importlib.util
from pathlib import Path
import sys
from copy import deepcopy
import pytest

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE.parents[1]))
from coursekit.data import example_hit, load_hits

MODULE_PATH = HERE / "tasks.py"
SPEC = importlib.util.spec_from_file_location("d26_mentee_3_A", MODULE_PATH)
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

def test_document_read_is_not_a_model_call():
    fix = m.repair_document_call()
    assert fix["correct_read"] == "doc.page_content"
    assert fix["generation_role"] == "Chat Model의 invoke"

def test_prompt_receives_two_named_strings():
    value = m.make_prompt_input("질문 A", "선택한 본문 B")
    assert value == {"question": "질문 A", "context": "선택한 본문 B"}
