"""가상 입력으로 검사기·기록기의 동작을 검사합니다. 실제 모델 품질 테스트가 아닙니다."""
from pathlib import Path
import sys
import json
import copy
import pytest

ROLE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROLE))
from coursekit.io import DATA, read_json, write_json, write_text, sha_text, canonical, save_version
from coursekit.prompting import build_context, make_bundle, render_prompt, check_pair, bundle_hash
from coursekit.contracts import KnowledgeAnswer, validate_answer, inspect_answer, strict_json, INSUFFICIENT
from coursekit.retry import run_with_retry, FixtureProvider, repair_prompt, run_fixture_scenarios
from coursekit.experiments import prepare_experiment, load_experiment, record_manual, review_experiment, summarize
from pydantic import ValidationError

FIXTURES=read_json(DATA/'validation_fixtures.json')
BY_ID={x['fixture_id']:x for x in FIXTURES}
ROWS=read_json(DATA/'knowledge_v1.json')
CASES=read_json(DATA/'dev_v1.json')

@pytest.mark.parametrize('item',FIXTURES,ids=[x['fixture_id'] for x in FIXTURES])
def test_validation_fixture(item):
    obj,error=validate_answer(item['raw_text'],item['provided_ids'])
    assert error==item['expected_error']
    assert (obj is not None)==(error is None)

@pytest.mark.parametrize('value',['', ' ', 'bad', '{}', '[]', 'null', '"string"'])
def test_parse_result_stages(value):
    _,error=validate_answer(value,[101])
    assert error in {'json_error','schema_error','blank_answer'}

@pytest.mark.parametrize('field,value',[('source_ids',[True]),('source_ids',['101']),('source_ids',[101.0]),('source_ids',[-1]),('source_ids',[0]),('source_ids',[101,102,103,104]),('answer','a'*501),('answer',''),('missing_information','a'*201),('status','unknown')])
def test_schema_negative_boundary(field,value):
    data=json.loads(BY_ID['valid_answer']['raw_text'])
    data[field]=value
    with pytest.raises(ValidationError):KnowledgeAnswer.model_validate(data)

def test_schema_positive_boundary():
    data={'status':'answered','answer':'가'*500,'source_ids':[101,102,103],'missing_information':''}
    obj=KnowledgeAnswer.model_validate(data)
    assert obj.source_ids==[101,102,103]
    schema=KnowledgeAnswer.model_json_schema()
    assert set(schema['required'])=={'status','answer','source_ids','missing_information'}
    assert schema['additionalProperties'] is False
    assert schema['properties']['answer']['maxLength']==500
    assert schema['properties']['source_ids']['maxItems']==3

def test_semantic_not_automatically_passed():
    f=BY_ID['semantic_counterexample']
    result=inspect_answer(f['raw_text'],f['provided_ids'])
    assert result['error'] is None and result['reference_ok'] is True
    assert result['evidence_ok'] is None

def test_context_relevant_ids_order_and_duplicate():
    output=json.loads(build_context(ROWS,[102,102,101]))
    assert [r['id'] for r in output]==[102,101]
    assert output[0]==ROWS[1]

@pytest.mark.parametrize('selected',[[999],[True],['101'],[-1]])
def test_invalid_selected_ids(selected):
    with pytest.raises(ValueError):build_context(ROWS,selected)

def test_duplicate_snapshot_rejected():
    with pytest.raises(ValueError):build_context(ROWS+[ROWS[0]],[101])

def test_template_exact_input_and_no_eval_labels():
    bundle=make_bundle()
    for case in CASES:
        assert check_pair(bundle,case)
        p,c=render_prompt(bundle,case,'A')
        assert case['question'] in p
        assert 'expected_behavior' not in p
        assert json.loads(c)==[r for r in ROWS if r['id'] in case['selected_ids']]
    trick=copy.deepcopy(CASES[0]);trick['question']='$context_json {"x":1}'
    assert trick['question'] in render_prompt(bundle,trick,'A')[0]

def test_hash_order_change_and_key_order_invariance():
    assert canonical({'a':1,'b':2})==canonical({'b':2,'a':1})
    assert sha_text(canonical(ROWS))!=sha_text(canonical(list(reversed(ROWS))))
    assert bundle_hash(make_bundle())==bundle_hash(make_bundle())

def test_fixture_retry_scenarios():
    rows=run_fixture_scenarios(FIXTURES)
    assert [r['calls'] for r in rows]==[2,2,1,1]
    assert [r['auto_accepted'] for r in rows]==[True,False,False,True]
    assert all(r['source_mode']=='fixture' and r['actual_model_recovery_rate'] is None for r in rows)

def test_never_repair_after_last_failure(monkeypatch):
    import coursekit.retry as r
    calls=[]
    original=r.repair_prompt
    def tracked(prompt,error):
        calls.append(error)
        return original(prompt,error)
    monkeypatch.setattr(r,'repair_prompt',tracked)
    provider=FixtureProvider([BY_ID['broken_json']['raw_text']]*2)
    obj,h=r.run_with_retry(provider,'original',lambda raw:validate_answer(raw,[101]))
    assert obj is None and provider.calls==2 and len(h)==2 and calls==['json_error']

def test_generation_error_not_silently_success_or_retried():
    calls=[]
    def fail(prompt):
        calls.append(prompt)
        raise RuntimeError('provider envelope must be handled separately')
    with pytest.raises(RuntimeError):run_with_retry(fail,'p',lambda x:validate_answer(x,[101]))
    assert len(calls)==1

def test_repair_safety_and_rule_stop():
    with pytest.raises(ValueError):repair_prompt('p','/private/example SECRET_TEST')
    assert 'SECRET_TEST' not in repair_prompt('p','schema_error')
    provider=FixtureProvider([BY_ID['unknown_source']['raw_text']])
    obj,h=run_with_retry(provider,'p',lambda x:validate_answer(x,[101]))
    assert obj is None and provider.calls==1 and h[0]['error']=='unknown_source'

def new_experiment(tmp_path,mode='manual_chat',repeats=1):
    folder=tmp_path/'experiment'
    prepare_experiment(folder,make_bundle(),CASES,repeats=repeats,source_mode=mode)
    return folder

def register_synthetic(folder,tmp_path,slot,fixture_id='valid_answer',attempt=1,state='completed'):
    # 이 테스트에서 manual 경로를 통과시키는 입력도 작성된 가상 샘플입니다. 결과를 사용자 관찰로 배포하지 않습니다.
    f=tmp_path/(slot+str(attempt)+'.txt');f.write_text(BY_ID[fixture_id]['raw_text'],encoding='utf-8')
    record_manual(folder,slot,f,'TEST_ONLY_NOT_A_REAL_MODEL',state,'TEST_FIXTURE','test',attempt, '2026-11-16T14:35:00+09:00')

def test_all_not_run_does_not_look_like_zero_quality(tmp_path):
    folder=new_experiment(tmp_path)
    assert not list(folder.rglob('raw.txt'))
    rows=review_experiment(folder)
    groups=summarize(rows)['groups']
    assert len(rows)==6
    assert all(g['N']==3 and g['not_run']==3 and g['attempted']==0 for g in groups)
    assert all(g['automatic']['json_ok']['rate'] is None for g in groups)
    assert all(g['human']['evidence_ok']['rate'] is None for g in groups)

def test_experiment_no_overwrite(tmp_path):
    folder=new_experiment(tmp_path)
    with pytest.raises(ValueError):prepare_experiment(folder,make_bundle(),CASES)

def test_raw_preserved_including_fences(tmp_path):
    folder=new_experiment(tmp_path)
    register_synthetic(folder,tmp_path,'D01_A_r1','code_fence')
    raw=(folder/'responses/D01_A_r1/raw.txt').read_text(encoding='utf-8')
    assert raw==BY_ID['code_fence']['raw_text']
    rows=review_experiment(folder)
    r=next(r for r in rows if r['slot_id']=='D01_A_r1')
    assert r['error']=='json_error'
    assert (folder/'responses/D01_A_r1/repair_prompt.txt').exists()

def test_actual_registration_metadata_time_and_no_overwrite(tmp_path):
    folder=new_experiment(tmp_path)
    register_synthetic(folder,tmp_path,'D01_A_r1')
    meta=read_json(folder/'responses/D01_A_r1/meta.json')
    assert meta['observed_at']=='2026-11-16T14:35:00+09:00' and meta['recorded_at']
    with pytest.raises(ValueError):register_synthetic(folder,tmp_path,'D01_A_r1')

def test_registration_missing_time_is_not_fabricated(tmp_path):
    folder=new_experiment(tmp_path)
    f=tmp_path/'sample.txt';f.write_text(BY_ID['valid_answer']['raw_text'],encoding='utf-8')
    record_manual(folder,'D01_A_r1',f,model_label='TEST_ONLY')
    m=read_json(folder/'responses/D01_A_r1/meta.json')
    assert m['observed_at'] is None and m['recorded_at'] is not None

@pytest.mark.parametrize('kind',['bundle','prompt','raw','manifest'])
def test_tampering_detected(tmp_path,kind):
    folder=new_experiment(tmp_path)
    if kind=='bundle':
        p=folder/'frozen_bundle.json';d=read_json(p);d['changed']='modified';write_json(p,d)
    elif kind=='prompt':
        p=folder/'prompts/D01_A_r1.txt';p.write_text('modified',encoding='utf-8')
    elif kind=='manifest':
        p=folder/'manifest.json';d=read_json(p);d['source_mode']='fixture';write_json(p,d)
    else:
        register_synthetic(folder,tmp_path,'D01_A_r1');(folder/'responses/D01_A_r1/raw.txt').write_text('modified',encoding='utf-8')
    with pytest.raises(ValueError):review_experiment(folder)

def test_review_requires_rater_and_reason(tmp_path):
    folder=new_experiment(tmp_path)
    register_synthetic(folder,tmp_path,'D01_A_r1')
    p=folder/'responses/D01_A_r1/human_review.json'
    r=read_json(p);r['evidence_ok']=True;write_json(p,r)
    with pytest.raises(ValueError):review_experiment(folder)
    r.update(reviewer='TEST_RATER',note='가상 지식101의 보관 위치와 일치');write_json(p,r)
    out=review_experiment(folder)
    assert next(x for x in out if x['slot_id']=='D01_A_r1')['evidence_ok'] is True

def test_not_run_cannot_be_human_scored(tmp_path):
    folder=new_experiment(tmp_path)
    p=folder/'responses/D01_A_r1/human_review.json'
    d=read_json(p);d.update(evidence_ok=True,reviewer='TEST_RATER',note='not real');write_json(p,d)
    with pytest.raises(ValueError):review_experiment(folder)

def test_retry_record_does_not_change_first_metrics(tmp_path):
    folder=new_experiment(tmp_path)
    register_synthetic(folder,tmp_path,'D01_A_r1','broken_json')
    review_experiment(folder)
    register_synthetic(folder,tmp_path,'D01_A_r1','valid_answer',attempt=2)
    rows=review_experiment(folder)
    assert len(rows)==7
    group=next(g for g in summarize(rows)['groups'] if g['variant']=='A')
    assert group['automatic']['json_ok']['passed']==0
    assert group['retry']=={'eligible':1,'attempted':1,'recovered':1,'rate':1.0}
    assert [r['error'] for r in rows if r['slot_id']=='D01_A_r1']==['json_error',None]

def test_rule_failure_not_retried(tmp_path):
    folder=new_experiment(tmp_path)
    register_synthetic(folder,tmp_path,'D01_A_r1','unknown_source')
    review_experiment(folder)
    assert not (folder/'responses/D01_A_r1/repair_prompt.txt').exists()
    with pytest.raises(ValueError):register_synthetic(folder,tmp_path,'D01_A_r1','valid_answer',attempt=2)

def test_refusal_is_not_json_error_or_business_insufficient(tmp_path):
    folder=new_experiment(tmp_path)
    f=tmp_path/'refusal.txt';f.write_text('TEST_ONLY refusal',encoding='utf-8')
    record_manual(folder,'D01_A_r1',f,model_label='TEST_ONLY',state='refused',reason='simulated')
    rows=review_experiment(folder)
    r=next(x for x in rows if x['slot_id']=='D01_A_r1')
    assert r['execution_state']=='refused' and r['error'] is None and r['json_ok'] is None
    assert not (folder/'responses/D01_A_r1/repair_prompt.txt').exists()

def test_fixture_cannot_register_as_manual(tmp_path):
    folder=new_experiment(tmp_path,'fixture')
    with pytest.raises(ValueError):register_synthetic(folder,tmp_path,'D01_A_r1')

def test_repeat_plan_no_overwrite(tmp_path):
    folder=new_experiment(tmp_path,repeats=2)
    manifest,_=load_experiment(folder)
    assert len(manifest['tasks'])==12 and len(set(t['slot_id'] for t in manifest['tasks']))==12

def test_version_guard(tmp_path):
    p=tmp_path/'version.json'
    save_version(p,{'v':1});save_version(p,{'v':1})
    with pytest.raises(ValueError):save_version(p,{'v':2})

@pytest.mark.parametrize('time',['2026-11-16T14:35:00','invalid'])
def test_observation_time_is_validated(tmp_path,time):
    folder=new_experiment(tmp_path)
    with pytest.raises(ValueError):record_manual(folder,'D01_A_r1',None,state='failed',reason='test',observed_at=time)
