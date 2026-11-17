"""교시 공통 실행 도우미. 별도 정상 시작점이며 이전 교시 TODO 완료를 요구하지 않습니다."""
from dataclasses import replace
from copy import deepcopy
from types import SimpleNamespace
from pathlib import Path
from .io import write_json,read_json,input_parts
from .config import load_settings,choose_model
from .request import build_request
from .runner import run_request,RetryPolicy,not_run
from .fixtures import SimClient,response_for
from .errors import ProviderError
from .support import execute_case,emit
from .metrics import estimate_cost,summarize_runs


def failure_scenarios(args, *, classifier, delay, policy):
    # 어떠한 --source 값에도 실제 401/429를 유발하지 않습니다.
    settings=load_settings("simulated")
    case,selected,instructions=input_parts("H01")
    request=build_request(settings.models["fast"],instructions,case["question"],selected)
    normal=response_for("H01")
    bad=response_for("H01",raw='{"status":')
    definitions=[
        ("auth",[ProviderError(401)],1,"auth_error"),
        ("quota",[ProviderError(429,"insufficient_quota")],1,"quota_error"),
        ("unknown_429",[ProviderError(429,"other")],1,"unknown_429"),
        ("rate_then_ok",[ProviderError(429,"rate_limit_exceeded",headers={"retry-after":"2"}),normal],2,"validated"),
        ("server_twice",[ProviderError(500),ProviderError(500)],2,"server_error"),
        ("timeout",[ProviderError(kind="timeout")],1,"timeout"),
        ("retry_after_long",[ProviderError(429,"rate_limit_exceeded",headers={"retry-after":"120"})],1,"deferred"),
        ("format_once",[bad,normal],2,"validated"),
        ("shared_four",[ProviderError(429,"rate_limit_exceeded"),bad,ProviderError(503),normal],4,"validated"),
        ("refused",[response_for("H01",refusal=True)],1,"refused"),
        ("incomplete",[response_for("H01",status="incomplete")],1,"incomplete"),
    ]
    results=[]
    for name,steps,expected_sends,expected_status in definitions:
        client=SimClient("H01",steps=steps)
        try:
            result=run_request(request,{103},source="simulated",settings=settings,case_id=name,client=client,
                               policy=policy,hooks={"classify":classifier,"delay":delay})
        finally:
            client.close()
        result["expected"]={"simulated_send_count":expected_sends,"run_status":expected_status}
        result["check_passed"]=len(client.calls)==expected_sends and result["run_status"]==expected_status
        emit(args,result)
        results.append(result)
    write_json(args.output_dir/"scenario_checks.json",[
        {"case":r["case_id"],"actual":r["run_status"],"expected":r["expected"],"passed":r["check_passed"]} for r in results])
    if not all(r["check_passed"] for r in results):
        raise ValueError("실패 정책의 예상 결과와 다릅니다. scenario_checks.json을 확인하세요")
    return results


def usage_lab(args, *, usage_reader, calculator, row_builder, summarizer=None):
    if args.run_file:
        result=read_json(args.run_file)
        rows=[]
        for attempt in result.get("attempts",[]):
            # 실제 기록의 usage는 이미 추출된 값입니다. 과거 실행의 미수신 값을 임의 채우지 않습니다.
            cost=calculator(attempt.get("usage"),attempt.get("actual_model") or result["model"],
                            service_tier=attempt.get("response_service_tier") or "default")
            if result["source_mode"]=="simulated":
                cost={**cost,"example_estimated_usd":cost["estimated_usd"],"estimated_usd":None,"cost_status":"fixture_not_billed"}
            rows.append(row_builder(result,attempt,cost))
        write_json(args.output_dir/"usage_analysis.json",{"origin_run_id":result["run_id"],"source_mode":result["source_mode"],"rows":rows,
                     "cost_totals": summarizer(result.get("attempts",[])) if summarizer else None})
        print("API 재호출 없이 원래 기록을 분석했습니다.")
        return rows
    if args.source!="simulated":
        result=not_run("USAGE","추가 호출을 하지 않습니다. --run-file에 앞 교시의 run.json을 지정하세요")
        emit(args,result)
        return []
    usage=usage_reader(response_for("H01"))
    model=load_settings("simulated").models["fast"]
    example=calculator(usage,model)
    records=[{"case":"formula_example","source_mode":"simulated","usage":usage,
              "example_estimated_usd":example["estimated_usd"],"estimated_usd":None},
             {"case":"missing_usage","source_mode":"simulated",**calculator(None,model)},
             {"case":"unknown_model","source_mode":"simulated",**calculator(usage,"unknown-model")}]
    write_json(args.output_dir/"cost_examples.json",records)
    if example["estimated_usd"]!="0.00138":
        raise ValueError("계산 예시가 다릅니다: 입력1000·cached400·출력200")
    print("모의 계산 예시 0.00138 USD. 실제 API 청구가 아닙니다.")
    return records


def routing_lab(args, *, router, record_view, compare_modes):
    modes=compare_modes() if args.action=="compare" else [args.mode]
    results=[]
    # 자동 fallback이 아니라 사용자가 명시적으로 선택한 비교 실행입니다.
    for mode in modes:
        changed=deepcopy(args)
        changed.mode=mode
        result=execute_case(changed,args.case or "H01",route=router)
        emit(args,result)
        results.append(record_view(result))
        if result["run_status"] in {"quota_error","auth_error","permission_error","budget_exhausted"}:
            break
    write_json(args.output_dir/"model_comparison.json",results)
    return results
