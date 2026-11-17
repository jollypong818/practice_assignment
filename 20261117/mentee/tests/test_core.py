"""외부 API를 호출하지 않는 분기·계약 검사. 실제 인증·요금 검증과 구분합니다."""
import json
import math
from copy import deepcopy
from datetime import datetime,timezone,timedelta
from types import SimpleNamespace
from decimal import Decimal
from pathlib import Path
import sys
import socket
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from coursekit import contracts
from coursekit.config import load_settings,choose_model,SetupError,Settings
from coursekit.io import input_parts,digest,read_json,ROOT
from coursekit.request import build_request,OUTPUT_FORMAT,check_request_for_send
from coursekit.response import completed_text, get, accept_event, StreamState
from coursekit.fixtures import response_for,SimClient,VirtualClock,namespace
from coursekit.errors import ProviderError,classify_error,parse_retry_after,retry_delay,normalize_error
from coursekit.runner import run_request,RetryPolicy
from coursekit.metrics import read_usage,estimate_cost,sum_cost,summarize_runs
from coursekit.cache import cache_key,make_entry,read_cache
from coursekit.budget import SendLedger,BudgetStopped

@pytest.fixture(autouse=True)
def forbid_network(monkeypatch):
    def blocked(*args,**kwargs):
        raise AssertionError("오프라인 검사에서 네트워크 사용 금지")
    monkeypatch.setattr(socket.socket,"connect",blocked)
    monkeypatch.setattr(socket,"create_connection",blocked)

@pytest.fixture
def settings():return load_settings("simulated")
@pytest.fixture
def request_data(settings):
    case,rows,prompt=input_parts("H01")
    return build_request(settings.models["fast"],prompt,case["question"],rows)

def run(steps,settings,request_data,**kw):
    client=SimClient("H01",steps=steps,stream_scenario=kw.pop("scenario","normal"))
    result=run_request(request_data,{103},source="simulated",settings=settings,case_id="H01",client=client,**kw)
    return result,client

@pytest.mark.parametrize("change,error",[
    ({"source_ids":["103"]},"schema_error"),({"source_ids":[True]},"schema_error"),
    ({"source_ids":[0]},"schema_error"),({"source_ids":[999]},"unknown_source"),
    ({"source_ids":[103,103]},"duplicate_source"),({"source_ids":[]},"status_rule"),
    ({"answer":""},"schema_error"),({"answer":" "},"blank_answer"),
    ({"answer":"a"*501},"schema_error"),({"missing_information":"x"},"status_rule"),
    ({"status":"invented"},"schema_error"),({"extra":"x"},"schema_error"),
])
def test_day21_contract(change,error):
    answer=json.loads(response_for().output_text);answer.update(change)
    assert contracts.inspect_answer(json.dumps(answer),{103})["error"]==error

@pytest.mark.parametrize("raw",['{','{"a":1,"a":2}','{"a":NaN}','{"a":Infinity}', 'x'*20001])
def test_json_strict(raw):assert contracts.inspect_answer(raw,{103})["error"]=="json_error"

def test_insufficient():
    result=contracts.inspect_answer(response_for("H02").output_text,{102})
    assert result["error"] is None and result["evidence_ok"] is None

def test_only_delivered_ids():
    assert contracts.inspect_answer(response_for("H01").output_text,{101})["error"]=="unknown_source"

def test_semantics_not_auto():
    obj=json.loads(response_for("H01").output_text);obj["answer"]="보관 기간은 100년입니다."
    report=contracts.inspect_answer(json.dumps(obj),{103})
    assert report["error"] is None and report["evidence_ok"] is None

@pytest.mark.parametrize("status,refusal,raw,expected",[
    ("completed",False,None,None),("completed",True,None,"refused"),
    ("incomplete",False,None,"incomplete"),("failed",False,None,"failed"),
    ("completed",False," ","empty_output"),("in_progress",False,None,"in_progress"),
    ("incomplete",True,None,"refused"),
])
def test_gate(status,refusal,raw,expected):
    assert completed_text(response_for(status=status,refusal=refusal,raw=raw))[1]==expected

@pytest.mark.parametrize("scenario,status",[("normal","validated"),("no_terminal","stream_interrupted"),
    ("interrupted","stream_interrupted"),("error_event","stream_interrupted")])
def test_stream_paths(settings,request_data,scenario,status):
    result,client=run([response_for()],settings,request_data,stream=True,scenario=scenario)
    assert result["run_status"]==status
    assert len(client.calls)==1 and client.stream_closed
    if status!="validated":assert result["answer_object"] is None

@pytest.mark.parametrize("kind,expected",[("incomplete","incomplete"),("failed","failed")])
def test_stream_terminal(settings,request_data,kind,expected):
    result,client=run([response_for(status=kind)],settings,request_data,stream=True)
    assert result["run_status"]==expected and result["usage"] is not None


def test_stream_refusal(settings,request_data):
    result,_=run([response_for(refusal=True)],settings,request_data,stream=True)
    assert result["run_status"]=="refused" and result["first_text_ms"] is None


def test_empty_delta_first_time():
    state=StreamState();clock=lambda:2.0
    accept_event(state,namespace({"type":"response.output_text.delta","delta":""}),clock,1.0)
    assert state.first_text_ms is None
    accept_event(state,namespace({"type":"response.output_text.delta","delta":"hello"}),clock,1.0)
    assert state.first_text_ms==1000
    accept_event(state,namespace({"type":"response.output_text.done"}),clock,1.0)
    assert state.final is None

@pytest.mark.parametrize("error,kind,retry",[
    (ProviderError(401),"auth_error",False),(ProviderError(403),"permission_error",False),
    (ProviderError(404),"model_or_resource_error",False),(ProviderError(400),"request_error",False),
    (ProviderError(429,"rate_limit_exceeded"),"rate_limit",True),
    (ProviderError(429,error_type="tokens"),"rate_limit",True),
    (ProviderError(429,"insufficient_quota"),"quota_error",False),
    (ProviderError(429,error_type="billing_not_active"),"quota_error",False),
    (ProviderError(429,"unknown"),"unknown_429",False),
    (ProviderError(500),"server_error",True),(ProviderError(503),"server_error",True),
    (ProviderError(501),"unknown_error",False),(ProviderError(kind="timeout"),"timeout",False),
    (ProviderError(kind="connection"),"connection",False),
])
def test_classification(error,kind,retry):assert classify_error(error)=={"kind":kind,"retryable":retry}

@pytest.mark.parametrize("header,expected",[(None,None),("2",2.0),("0",0.0),("-1",None),("nan",None),
    ("inf",None),("garbage",None),("1.25",1.25)])
def test_retry_after(header,expected):assert parse_retry_after(header)==expected

def test_retry_after_date():
    now=datetime(2026,11,17,tzinfo=timezone.utc)
    assert parse_retry_after("Tue, 17 Nov 2026 00:00:05 GMT",now)==5
    assert parse_retry_after("Mon, 16 Nov 2026 00:00:05 GMT",now)==0

@pytest.mark.parametrize("hint,remaining,expected",[(10,5,None),(2,10,2),(None,10,1),(0,10,1),(1,1,None)])
def test_delay(hint,remaining,expected):assert retry_delay(1,hint,remaining,0)==expected


def test_bounded_retry_four(settings,request_data):
    steps=[ProviderError(429,"rate_limit_exceeded",headers={"retry-after":"2"}),
           response_for(raw='{'),ProviderError(503),response_for()]
    clock=VirtualClock()
    result,client=run(steps,settings,request_data,clock=clock.now,sleeper=clock.sleep)
    assert result["run_status"]=="validated" and len(client.calls)==4
    assert [a["generation_no"] for a in result["attempts"]]==[1,1,2,2]
    assert clock.sleeps[0]>=2
    assert result["new_api_send_count"]==0 and result["simulated_send_count"]==4
    assert result["attempts"][1]["raw"]=='{'
    assert '{' not in client.calls[2]["input"][-1]["content"]  # raw를 재전송하지 않음

@pytest.mark.parametrize("steps,count,status",[
    ([ProviderError(500),ProviderError(500)],2,"server_error"),
    ([ProviderError(401)],1,"auth_error"),
    ([ProviderError(429,"insufficient_quota")],1,"quota_error"),
    ([ProviderError(kind="timeout")],1,"timeout"),
    ([ProviderError(429,"what")],1,"unknown_429"),
    ([response_for(refusal=True)],1,"refused"),
    ([response_for("H02")],1,"validated"),
    ([response_for(raw=json.dumps({"status":"answered","answer":"a","source_ids":[999],"missing_information":""}))],1,"unknown_source"),
    ([response_for(raw='{'),response_for(raw='{')],2,"json_error"),
])
def test_stops(settings,request_data,steps,count,status):
    result,client=run(steps,settings,request_data)
    assert len(client.calls)==count and result["run_status"]==status


def test_long_retry_after(settings,request_data):
    clock=VirtualClock()
    result,client=run([ProviderError(429,"rate_limit_exceeded",headers={"retry-after":"90"})],settings,request_data,
                      clock=clock.now,sleeper=clock.sleep)
    assert result["run_status"]=="deferred" and not clock.sleeps and len(client.calls)==1


def test_no_format_repair(settings,request_data):
    result,client=run([response_for(raw='{')],settings,request_data,policy=RetryPolicy(max_generations=1))
    assert len(client.calls)==1 and result["run_status"]=="json_error"

@pytest.mark.parametrize("limit",[0,5,100])
def test_bad_budget(limit):
    with pytest.raises(ValueError):RetryPolicy(max_sends_total=limit)


def test_cost_exact(settings):
    u=read_usage(response_for())
    assert estimate_cost(u,settings.models["fast"])["estimated_usd"]=="0.00138"
    u["reasoning_tokens"]=100
    assert estimate_cost(u,settings.models["fast"])["estimated_usd"]=="0.00138"

@pytest.mark.parametrize("usage",[None,{}, {"input_tokens":1,"output_tokens":1,"cached_tokens":None},
    {"input_tokens":True,"cached_tokens":0,"output_tokens":1},
    {"input_tokens":1,"cached_tokens":2,"output_tokens":1},
    {"input_tokens":1,"cached_tokens":0,"output_tokens":1,"reasoning_tokens":2},
    {"input_tokens":-1,"cached_tokens":0,"output_tokens":1}])
def test_cost_unknown(settings,usage):assert estimate_cost(usage,settings.models["fast"])["estimated_usd"] is None


def test_cost_known_zero(settings):
    u={"input_tokens":0,"output_tokens":0,"cached_tokens":0}
    assert Decimal(estimate_cost(u,settings.models["fast"])["estimated_usd"])==0


def test_cost_unknown_model(settings):assert estimate_cost(read_usage(response_for()),"other")["estimated_usd"] is None

def test_cost_service_tier(settings):assert estimate_cost(read_usage(response_for()),settings.models["fast"],service_tier="priority")["estimated_usd"] is None

def test_cost_sum_unknown():
    summary=sum_cost([{"source_mode":"api_live","estimated_usd":None},{"source_mode":"api_live","estimated_usd":"0.00138"},
                      {"source_mode":"app_cache","estimated_usd":"900"},{"source_mode":"simulated","estimated_usd":"900"}])
    assert summary=={"known_estimated_usd":"0.00138","unknown_cost_attempts":1,"total_estimated_usd":None}


def test_usage_missing_is_not_zero():
    assert read_usage(response_for(usage=False)) is None
    u=read_usage(SimpleNamespace(usage=SimpleNamespace(input_tokens=0,output_tokens=0)))
    assert u["input_tokens"]==0 and u["cached_tokens"] is None


def approved_result(settings,request_data):
    result,_=run([response_for()],settings,request_data)
    result["scope"]="classroom-demo"
    review={"decision":"approve","note":"직접 작성한 검사 fixture의 승인 분기",
            "run_id":result["run_id"],"run_hash":digest(result),"reviewed_at_epoch":100.0}
    return result,review


def test_cache_hit(settings,request_data):
    result,review=approved_result(settings,request_data);entry=make_entry(result,review)
    hit=read_cache({entry["key"]:entry},entry["key"],101.0,{103},expected_source="simulated",scope="classroom-demo")
    assert hit["new_api_send_count"]==0 and hit["usage"]["input_tokens"]==0 and hit["estimated_usd"]=="0"
    assert hit["origin_run_id"]==result["run_id"] and hit["origin_source_mode"]=="simulated"

@pytest.mark.parametrize("change",["ttl","permission","origin","unapproved","version","source"])
def test_cache_misses(settings,request_data,change):
    result,review=approved_result(settings,request_data);entry=make_entry(result,review)
    kw={"expected_source":"simulated","scope":"classroom-demo"}; now=101.0;ids={103}
    if change=="ttl":now=entry["expires_at"]
    if change=="permission":kw["scope"]="different"
    if change=="origin":kw["expected_source"]="api_live"
    if change=="unapproved":entry["human_approved"]=False
    if change=="version":entry["validator_version"]="v999"
    if change=="source":ids={101}
    assert read_cache({entry["key"]:entry},entry["key"],now,ids,**kw) is None

@pytest.mark.parametrize("mutation",["text","model","prompt","schema","scope","validator"])
def test_key_changes(request_data,mutation):
    first=cache_key(request_data,"classroom-demo");other=deepcopy(request_data)
    scope="classroom-demo";version="day21-v1"
    if mutation=="text":other["input"][0]["content"]+=" changed"
    if mutation=="model":other["model"]="other"
    if mutation=="prompt":other["instructions"]+=" changed"
    if mutation=="schema":other["text"]={"format":{}}
    if mutation=="scope":scope="other"
    if mutation=="validator":version="v2"
    assert first!=cache_key(other,scope,version)

@pytest.mark.parametrize("change",["hash","decision","empty_note","failed","insufficient"])
def test_no_unauthorized_cache_write(settings,request_data,change):
    result,review=approved_result(settings,request_data)
    if change=="hash":review["run_hash"]="bad"
    if change=="decision":review["decision"]="reject"
    if change=="empty_note":review["note"]=""
    if change=="failed":result["run_status"]="failed"
    if change=="insufficient":result["answer_object"]["status"]="insufficient_context"
    assert make_entry(result,review) is None


def test_ledger_persists(tmp_path):
    path=tmp_path/"ledger.json";first=SendLedger(path,2)
    assert first.reserve("a",1)==1
    assert SendLedger(path,2).reserve("b",1)==2
    with pytest.raises(BudgetStopped):first.reserve("c",1)


def test_corrupt_ledger_not_reset(tmp_path):
    path=tmp_path/"ledger.json";path.write_text("broken")
    with pytest.raises(BudgetStopped):SendLedger(path,20).reserve("x",1)
    assert path.read_text()=="broken"


def test_ledger_lock(tmp_path):
    path=tmp_path/"ledger.json";path.with_suffix(".lock").touch()
    with pytest.raises(BudgetStopped):SendLedger(path,20).reserve("x",1)


def test_invalid_route_no_send(settings):
    with pytest.raises(SetupError):choose_model("wrong",settings.models)
    with pytest.raises(SetupError):choose_model("quality",{"fast":"x","quality":None})


def test_sim_does_not_read_key(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY","secret-never-use")
    monkeypatch.setenv("OPENAI_MODEL","nonsense")
    assert load_settings("simulated").api_key==""


def test_request_contract(request_data):
    assert check_request_for_send(request_data) is None
    payload=json.loads(request_data["input"][0]["content"])
    assert set(payload)=={"question","knowledge"} and [x["id"] for x in payload["knowledge"]]==[103]
    assert "expected_behavior" not in payload and request_data["store"] is False
    assert request_data["text"]["format"]["strict"] is True

@pytest.mark.parametrize("key,value",[("store",True),("max_output_tokens",1201),("service_tier","priority"),("tools",[])])
def test_request_guard(request_data,key,value):
    request_data[key]=value
    with pytest.raises(ValueError):check_request_for_send(request_data)


def test_live_adapter_settings_without_network(monkeypatch,settings):
    from coursekit.runner import make_client
    calls={}
    class FakeSDK:
        def __init__(self,**kwargs):calls.update(kwargs)
    monkeypatch.setitem(sys.modules,"openai",SimpleNamespace(OpenAI=FakeSDK))
    make_client(Settings("never-record",settings.models),"live","H01")
    assert calls["max_retries"]==0 and calls["timeout"]==30.0
    assert calls["base_url"]=="https://api.openai.com/v1"
    # 이 검사는 실제SDK가아닌생성자계약의모의검사입니다.


def test_partial_end_usage_not_zero(settings,request_data):
    result,_=run([response_for()],settings,request_data,stream=True,scenario="interrupted")
    assert result["usage"] is None and result["estimated_usd"] is None


def test_actual_known_model_cost_branch(tmp_path,request_data,settings):
    # 라이브 분기 테스트에만 주입한 가짜 클라이언트. 외부 전송은 네트워크 guard로 금지되어 있습니다.
    response=response_for();response.model=settings.models["fast"]
    result=run_request(request_data,{103},source="live",settings=settings,case_id="unit-live-branch",
                       client=SimClient(steps=[response]),ledger_path=tmp_path/"test_ledger.json")
    assert result["estimated_usd"]=="0.00138" and result["new_api_send_count"]==1
    # 실제 결과 폴더로 내보내지 않습니다. 단위 테스트 안에서만 값 비교합니다.


def test_failed_live_cost_unknown(tmp_path,request_data,settings):
    response=response_for();response.model=settings.models["fast"]
    fake=SimClient(steps=[ProviderError(500),response]);clock=VirtualClock()
    result=run_request(request_data,{103},source="live",settings=settings,case_id="unit-live-branch",
                       client=fake,ledger_path=tmp_path/"test_ledger.json",clock=clock.now,sleeper=clock.sleep)
    assert result["known_estimated_usd"]=="0.00138" and result["estimated_usd"] is None
    assert result["unknown_cost_attempts"]==1


def test_record_modes_not_mixed(settings,request_data):
    result,_=run([response_for()],settings,request_data)
    report=summarize_runs([result])
    assert report["api_live"]["runs"]==0 and report["simulated"]["runs"]==1
