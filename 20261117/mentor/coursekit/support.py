"""교시별 독립 실행과 공통 안전 장치. TODO 함수가 실제 처리 경로에 전달됩니다."""
from pathlib import Path
from copy import deepcopy
from datetime import datetime, timezone
import argparse
import ast
import time
import uuid
import sys
from .io import ROOT, read_json, write_json, input_parts, load_case, selected_knowledge, digest
from .config import load_settings, choose_model, SetupError
from .request import build_request
from .runner import run_request, not_run, RetryPolicy
from .records import save_run, save_table, table_rows
from .cache import cache_key, make_entry, read_cache
from .metrics import summarize_runs


class TodoIncomplete(Exception):
    pass


def ensure_completed(here):
    pending = []
    for path in sorted(Path(here).rglob("*.py")):
        if "tests" in path.parts:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node,ast.Raise) and isinstance(node.exc,ast.Call):
                func=node.exc.func
                if isinstance(func,ast.Name) and func.id=="NotImplementedError":
                    value=node.exc.args[0].value if node.exc.args and isinstance(node.exc.args[0],ast.Constant) else "TODO"
                    pending.append(str(value))
    if pending:
        raise TodoIncomplete("미완성 TODO가 있어 API를 보내지 않습니다: " + ", ".join(pending))


def parse_args(here):
    parser=argparse.ArgumentParser(description="Day22: 실제 호출은 --source live --allow-paid, 모의는 --source simulated")
    parser.add_argument("--source",choices=["live","simulated"],default="live")
    parser.add_argument("--allow-paid",action="store_true",help="실제 호출·과금 가능성을 확인했습니다")
    parser.add_argument("--mode",default="fast")
    parser.add_argument("--prompt-file",type=Path,help="16일에 고정한 instructions txt; 지정하지 않으면 제공 기준본")
    parser.add_argument("--case",default=None)
    parser.add_argument("--action",choices=["run","reuse","changed","compare"],default="run")
    parser.add_argument("--run-file",type=Path,help="이미 생성한 run.json; 비용 읽기·사람 승인 캐시에 사용")
    parser.add_argument("--output-dir",type=Path,default=Path(here)/"outputs")
    parser.add_argument("--no-repair",action="store_true",help="최초 출력만 확인하고 형식 수정 호출을 끕니다")
    args=parser.parse_args()
    ensure_completed(here)
    return args


def guarded(main):
    try:
        main()
    except TodoIncomplete as exc:
        print(str(exc))
        raise SystemExit(2) from None
    except (SetupError,ValueError,FileNotFoundError) as exc:
        # 설정 검사 메시지는 직접 작성한 안전한 설명입니다. 공급자 예외는 runner에서 분류합니다.
        print("실행 전 확인:",str(exc))
        raise SystemExit(2) from None


def execute_case(args, case_id, *, stream=False, hooks=None, request_builder=build_request,
                 route=choose_model, policy=None, changed=False):
    prepared_at=time.perf_counter()
    if args.source=="live" and not args.allow_paid:
        return not_run(case_id,"실제 호출은 --allow-paid 확인 뒤 실행합니다")
    try:
        settings=load_settings(args.source)
        model, reason=route(args.mode, settings.models)
        if case_id=="FIRST":
            question="API의 역할을 쉽게 설명해 주세요."
            selected=[]
            instructions="한국어 한 문장으로 답하세요."
        else:
            case, selected, instructions=input_parts(case_id)
            question=case["question"]
        if args.prompt_file and case_id!="FIRST":
            instructions=args.prompt_file.read_text(encoding="utf-8-sig")
        if changed:
            selected=deepcopy(selected)
            selected[0]["content"] += " 실행 환경도 함께 적습니다."
        request=request_builder(model,instructions,question,selected,structured=case_id!="FIRST")
        provided_ids={row["id"] for row in selected}
        prepared_ms=(time.perf_counter()-prepared_at)*1000
        active_policy=policy or (RetryPolicy(max_generations=1) if args.no_repair or case_id=="FIRST" else RetryPolicy())
        result=run_request(request,provided_ids,source=args.source,settings=settings,case_id=case_id,
                           stream=stream,policy=active_policy,hooks=hooks)
        result.update(scope=settings.scope,route_reason=reason,selected_knowledge=selected)
        result["preparation_ms"]=round(prepared_ms,3)
        if args.source=="live" and result.get("e2e_ms") is not None:
            result["e2e_ms"]=round(result["e2e_ms"]+prepared_ms,3)
        return result
    except (SetupError,ValueError) as exc:
        return not_run(case_id,str(exc))


def emit(args, result):
    path=save_run(args.output_dir,result)
    if result.get("raw"):
        print("응답 원문(자동 검증/사람 검토와 구분):",result["raw"])
    return path


def cache_action(args, *, key_builder=cache_key, cache_reader=read_cache):
    if args.run_file is None:
        raise ValueError("--run-file에 검토한 run.json을 지정하세요. 먼저 --action run으로 생성합니다")
    original=read_json(args.run_file)
    review_path=args.run_file.with_name("review.json")
    if not review_path.is_file():
        return not_run(original["case_id"],"review.json이 없습니다. tools/review.py로 사람이 검토하세요")
    review=read_json(review_path)
    entry=make_entry(original,review)
    if entry is None:
        return not_run(original["case_id"],"검증·승인·원문 해시가 맞지 않아 캐시에 넣지 않았습니다")
    settings=load_settings(args.source,require_key=False)
    model,reason=choose_model(args.mode,settings.models)
    case,selected,instructions=input_parts(original["case_id"])
    if args.prompt_file:
        instructions=args.prompt_file.read_text(encoding="utf-8-sig")
    if args.action=="changed":
        selected[0]["content"] += " 실행 환경도 함께 적습니다."
    request=build_request(model,instructions,case["question"],selected)
    key=key_builder(request,settings.scope)
    cache={entry["key"]:entry}
    answer=cache_reader(cache,key,time.time(),{row["id"] for row in selected},
                        expected_source="api_live" if args.source=="live" else "simulated",scope=settings.scope)
    if answer is None:
        return {**not_run(case["case_id"],"cache_miss: 만료·본문·모델·scope·버전·현재 출처를 확인하세요",model),
                "run_status":"cache_miss","old_key":entry["key"],"current_key":key,
                "route_reason":reason,"scope":settings.scope,
                "next_action":"변경 입력을 실제로 호출하려면 --action changed --allow-paid를 별도로 선택하세요"}
    answer.update(case_id=case["case_id"],scope=settings.scope,route_reason=reason,cache_key=key,
                  request=request,provided_ids=case["selected_ids"])
    return answer


def cache_lab(args, *, hooks=None, key_builder=cache_key, cache_reader=read_cache):
    if args.action=="reuse":
        result=cache_action(args,key_builder=key_builder,cache_reader=cache_reader)
    elif args.action=="changed":
        if args.run_file is None:
            raise ValueError("변경 전 승인한 --run-file이 필요합니다")
        miss=cache_action(args,key_builder=key_builder,cache_reader=cache_reader)
        emit(args,miss)
        if miss["run_status"] != "cache_miss":
            return miss
        # 미스 관찰과 재호출은 분리된 실행 기록입니다. live에는 allow-paid가 계속 필요합니다.
        result=execute_case(args,read_json(args.run_file)["case_id"],hooks=hooks,changed=True)
    else:
        result=execute_case(args,args.case or "H01",hooks=hooks)
    path=emit(args,result)
    if result["run_status"]=="validated" and result["source_mode"]!="app_cache":
        print("근거를 직접 검토한 뒤: python tools/review.py --run-file",path,"--decision approve --note '<검토 이유>'")
    return result


def daily_project(args, *, prepare_cases=None, hooks=None, make_table=table_rows, finish_summary=summarize_runs, policy=None):
    if args.action in {"reuse","changed"}:
        return cache_lab(args,hooks=hooks)
    case_ids=prepare_cases() if prepare_cases else ["H01","H02","H03"]
    if args.case:
        if args.case not in case_ids:
            raise ValueError("최종 질문은 H01~H03입니다")
        case_ids=[args.case]
    runs=[]
    stopped=None
    for case_id in case_ids:
        if stopped:
            result=not_run(case_id,"앞 호출을 중단했습니다: "+stopped)
        else:
            result=execute_case(args,case_id,stream=(case_id=="H01"),hooks=hooks,policy=policy)
        emit(args,result)
        runs.append(result)
        if result["run_status"] in {"auth_error","permission_error","quota_error","model_or_resource_error","budget_exhausted","not_run"}:
            stopped=result["run_status"]
    batch_id=str(uuid.uuid4())
    batch=args.output_dir/"batches"/batch_id
    save_table(batch/"observations.csv",make_table(runs))
    write_json(batch/"summary.json",finish_summary(runs))
    print("프로젝트 표:",batch/"observations.csv")
    print("남은 확인: 사람 근거 검토 → 승인 답 cache reuse/changed → 04의 모의 오류 한 건")
    return runs
