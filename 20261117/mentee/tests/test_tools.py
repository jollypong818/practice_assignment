"""Prompt 가져오기 도구의 실패·원문 보존 검사. 외부 API를 호출하지 않습니다."""
import importlib.util
from pathlib import Path
import sys
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from coursekit.contracts import KnowledgeAnswer

spec=importlib.util.spec_from_file_location('import_day21_prompt',Path(__file__).resolve().parents[1]/'tools/import_day21_prompt.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

@pytest.fixture
def bundle():
    return {'bundle_version':'prompt_bundle_v1','schema':KnowledgeAnswer.model_json_schema(),
            'template':'[역할] 도우미\n'+mod.DYNAMIC_SECTION+'[예제]\n$examples_json\n[규칙]\n$evidence_rule\n[출력]\n$contract',
            'variants':{'A':{'prompt_version':'custom_a','evidence_rule':'규칙 A'},'B':{'prompt_version':'custom_b','evidence_rule':'규칙 B'}},
            'contract_text':'계약 원문','examples':[{'example':'가상의 참고 예제'}]}

@pytest.mark.parametrize('variant',['A','B'])
def test_convert_preserves_selected_rule(bundle,variant):
    out,origin=mod.convert(bundle,variant)
    assert bundle['variants'][variant]['evidence_rule'] in out
    assert bundle['contract_text'] in out and '가상의 참고 예제' in out
    assert '$question' not in out and '$context_json' not in out
    assert 'user 입력 JSON' in out and origin['variant']==variant
    assert origin['prompt_version']==bundle['variants'][variant]['prompt_version']

@pytest.mark.parametrize('kind',['version','schema','section','unknown_variable','missing_variant'])
def test_convert_refuses_unrecognized_bundle(bundle,kind):
    if kind=='version':bundle['bundle_version']='other'
    elif kind=='schema':bundle['schema']={}
    elif kind=='section':bundle['template']='임의의 변경 템플릿'
    elif kind=='unknown_variable':bundle['template']+='\n$extra'
    else:bundle['variants'].pop('B')
    with pytest.raises(ValueError):mod.convert(bundle,'B')
