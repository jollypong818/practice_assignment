"""수동 ChatGPT 실험의 준비·원문 보존·집계를 지원합니다.
구현 편의를 위한 제공 코드이며 모델 답변을 만들거나 API를 호출하지 않습니다.
"""
from datetime import datetime, timezone
from pathlib import Path
from .io import read_json, write_json, write_text, write_csv, canonical, sha_text, check_name
from .prompting import render_prompt, check_pair, bundle_hash
from .contracts import inspect_answer, validate_answer
from .retry import repair_prompt

STATES = {"not_run", "completed", "refused", "incomplete", "failed"}
HUMAN_KEYS = ("evidence_ok", "task_ok", "insufficiency_ok")


def prepare_experiment(folder, bundle, cases, repeats=1, source_mode="manual_chat"):
    """동명 실험을 덮어쓰지 않습니다. 생성한 raw 파일은 처음에는 하나도 없습니다."""
    folder = Path(folder)
    if folder.exists():
        raise ValueError("이미 있는 실험입니다. 원문을 보존하고 --run에 새 이름을 사용하세요.")
    if repeats not in (1, 2) or source_mode not in {"manual_chat", "fixture"}:
        raise ValueError("지원하지 않는 반복 수 또는 응답 출처")
    ids = [c["case_id"] for c in cases]
    if len(set(ids)) != len(ids) or not ids:
        raise ValueError("질문 ID가 중복되거나 비어 있습니다")
    # 입력을 전부 검사한 뒤 디렉터리를 만듭니다.
    prepared=[]
    for case in cases:
        check_name(case["case_id"])
        check_pair(bundle,case)
        for repeat in range(1,repeats+1):
            for variant in ("A","B"):
                slot=f'{case["case_id"]}_{variant}_r{repeat}'
                prompt,context=render_prompt(bundle,case,variant)
                prepared.append({"slot_id":slot,"case_id":case["case_id"],"variant":variant,"repeat":repeat,
                    "question":case["question"],"expected_behavior":case["expected_behavior"],
                    "selected_ids":list(dict.fromkeys(case["selected_ids"])),
                    "prompt_version":bundle["variants"][variant]["prompt_version"],
                    "prompt_sha256":sha_text(prompt),"context_sha256":sha_text(context),
                    "context_json":context,"prompt":prompt})
    folder.mkdir(parents=True)
    write_json(folder / "frozen_bundle.json",bundle)
    write_json(folder / "answer_schema.json",bundle["schema"])
    tasks=[]
    for entry in prepared:
        task={k:v for k,v in entry.items() if k!="prompt"}
        tasks.append(task)
        write_text(folder / "prompts" / (entry["slot_id"]+".txt"),entry["prompt"])
        target=folder / "responses" / entry["slot_id"]
        target.mkdir(parents=True)
        write_json(target / "meta.json",{
            "source_mode":source_mode,"execution_state":"not_run","attempt":1,
            "model_label":"미확인","observed_at":None,"recorded_at":None,"tools_and_personalization":"미확인",
            "reason":"미실행","raw_sha256":None,
        })
        write_json(target / "human_review.json",{
            "evidence_ok":None,"task_ok":None,"insufficiency_ok":None,"reviewer":"","note":"미평가"
        })
    manifest={"format":"day21_manual_v1","bundle_sha256":bundle_hash(bundle),
              "source_mode":source_mode,"context_version":bundle["context_version"],
              "schema_version":bundle["schema_version"],"created_at":datetime.now(timezone.utc).isoformat(),
              "tasks":tasks}
    manifest["manifest_sha256"]=sha_text(canonical(manifest))
    write_json(folder / "manifest.json",manifest)
    write_text(folder / "READ_ME_FIRST.md", "# 실제 응답을 채우기 전 상태\n\n"
        "prompts/의 원문 하나를 새 대화에 붙여 넣습니다. A의 대화에서 B를 이어 묻지 않습니다.\n"
        "첫 응답을 고치지 말고 별도 UTF-8 txt에 저장한 뒤 record_manual.py로 등록합니다.\n"
        "raw.txt가 없는 slot은 미실행입니다. 샘플을 가져와 실측처럼 채우지 않습니다.\n"
        "human_review.json의 null은 미평가입니다. 확인한 항목만 true/false로 바꾸고 근거를 적으세요.\n"
        "새 개선안은 새 버전·새 실험 폴더로 구분합니다. 이미 기록한 원문은 덮어쓰지 않습니다.\n")
    return manifest


def load_experiment(folder):
    folder=Path(folder)
    m=read_json(folder/"manifest.json")
    seal=m.get("manifest_sha256")
    body={k:v for k,v in m.items() if k!="manifest_sha256"}
    if seal != sha_text(canonical(body)):
        raise ValueError("실험 manifest가 바뀌었습니다. 새 실험을 만들거나 원본을 복구하세요.")
    bundle=read_json(folder/"frozen_bundle.json")
    if bundle_hash(bundle) != m["bundle_sha256"]:
        raise ValueError("고정한 Prompt·Context·Schema가 변경되었습니다")
    for t in m["tasks"]:
        check_name(t["slot_id"])
        p=(folder/"prompts"/(t["slot_id"]+".txt")).read_text(encoding="utf-8")
        if sha_text(p)!=t["prompt_sha256"] or sha_text(t["context_json"])!=t["context_sha256"]:
            raise ValueError("저장된 Prompt/문맥이 변경되었습니다")
    return m,bundle


def record_manual(folder, slot_id, raw_file=None, model_label="미확인", state="completed", conditions="미확인", reason="", attempt=1, observed_at=None):
    folder=Path(folder)
    m,_=load_experiment(folder)
    if m["source_mode"] != "manual_chat":
        raise ValueError("fixture 실험에 수동 모델 관찰을 섞을 수 없습니다")
    if observed_at is not None:
        try:
            dt=datetime.fromisoformat(observed_at)
        except (TypeError,ValueError):
            raise ValueError("관찰 시각은 시간대가 있는 ISO 형식으로 적으세요") from None
        if dt.tzinfo is None:
            raise ValueError("관찰 시각에 시간대가 필요합니다")
    if state not in STATES or state=="not_run" or attempt not in (1,2):
        raise ValueError("기록 상태 또는 시도 번호를 확인하세요")
    if slot_id not in {t["slot_id"] for t in m["tasks"]}:
        raise ValueError("명세에 없는 slot ID입니다")
    target=folder/"responses"/slot_id
    if attempt==2:
        first_meta,first_raw=_load_attempt(target,"manual_chat",1)
        task=next(t for t in m["tasks"] if t["slot_id"]==slot_id)
        if first_meta["execution_state"]!="completed" or validate_answer(first_raw,task["selected_ids"])[1] not in {"json_error","schema_error"}:
            raise ValueError("첫 응답은 형식 재시도 대상이 아닙니다")
        if not (target/"repair_prompt.txt").exists():
            raise ValueError("review에서 형식 오류를 먼저 확인해야 수정 응답을 등록할 수 있습니다")
        target=target/"attempt_2"
        target.mkdir(exist_ok=True)
    if (target/"raw.txt").exists() or ((target/"meta.json").exists() and read_json(target/"meta.json")["execution_state"]!="not_run"):
        raise ValueError("이미 기록한 응답입니다. 덮어쓰지 말고 새 실험으로 분리하세요")
    raw=None
    if raw_file is not None:
        raw=Path(raw_file).read_text(encoding="utf-8-sig")
        if len(raw.encode("utf-8")) > 20000:
            raise ValueError("수업 응답은 20,000 bytes 이하로 제한합니다")
    if state=="completed" and raw is None:
        raise ValueError("완료 응답 원문 파일이 필요합니다")
    if state!="completed" and not reason.strip():
        raise ValueError("거절·중단·실행 실패의 이유를 짧게 기록하세요")
    if not model_label.strip():
        raise ValueError("모델 표시 또는 미확인을 기록하세요")
    if raw is not None:
        write_text(target/"raw.txt",raw)
    write_json(target/"meta.json",{
        "source_mode":"manual_chat","execution_state":state,"attempt":attempt,
        "model_label":model_label,"observed_at":observed_at,"recorded_at":datetime.now(timezone.utc).isoformat(),
        "tools_and_personalization":conditions,"reason":reason,
        "raw_sha256":None if raw is None else sha_text(raw),
    })


def _load_attempt(target, expected_mode, attempt):
    meta_path=target/"meta.json"
    meta=read_json(meta_path) if meta_path.exists() else {"execution_state":"not_run","source_mode":expected_mode,"attempt":attempt}
    if meta.get("source_mode") != expected_mode or meta.get("attempt")!=attempt or meta.get("execution_state") not in STATES:
        raise ValueError("응답 출처·시도·실행 상태를 확인하세요")
    raw_path=target/"raw.txt"
    raw=raw_path.read_text(encoding="utf-8") if raw_path.exists() else None
    if meta["execution_state"]=="completed" and raw is None:
        raise ValueError("completed로 기록했지만 원문이 없습니다")
    if raw is not None and meta["execution_state"]=="not_run":
        raise ValueError("원문은 있지만 실행 정보가 없습니다. record_manual.py로 등록하세요")
    if raw is not None and meta.get("raw_sha256")!=sha_text(raw):
        raise ValueError("원문 해시가 다릅니다. 이미 등록한 첫 응답을 수정하지 마세요")
    return meta,raw


def review_experiment(folder, validator=validate_answer):
    folder=Path(folder)
    m,bundle=load_experiment(folder)
    all_rows=[]
    for t in m["tasks"]:
        target=folder/"responses"/t["slot_id"]
        human=read_json(target/"human_review.json")
        if any(type(human.get(k)) not in (bool,type(None)) for k in HUMAN_KEYS):
            raise ValueError("사람 평가는 true/false/null만 사용하세요")
        if any(human.get(k) is not None for k in HUMAN_KEYS) and (human.get("note","").strip() in {"","미평가"} or not human.get("reviewer","").strip()):
            raise ValueError("사람 평가를 채웠다면 평가자와 근거 메모도 남기세요")
        first_error=None
        for attempt in (1,2):
            current=target if attempt==1 else target/"attempt_2"
            if attempt==2 and not current.exists():
                continue
            meta,raw=_load_attempt(current,m["source_mode"],attempt)
            if attempt==2 and first_error not in {"json_error","schema_error"}:
                raise ValueError("이 첫 응답은 형식 재시도 대상이 아닙니다")
            state=meta["execution_state"]
            result={"json_ok":None,"schema_ok":None,"reference_ok":None,"evidence_ok":None,"error":None,"answer_object":None,"auto_status":"not_evaluated"}
            if state=="completed":
                result=inspect_answer(raw,t["selected_ids"],validator)
            if attempt==1:
                first_error=result["error"]
                if state=="not_run" and any(human.get(k) is not None for k in HUMAN_KEYS):
                    raise ValueError("미실행 응답에 사람 평가를 채울 수 없습니다")
            row={"slot_id":t["slot_id"],"case_id":t["case_id"],"variant":t["variant"],"repeat":t["repeat"],"attempt":attempt,
                 "source_mode":m["source_mode"],"execution_state":state,
                 "prompt_version":t["prompt_version"],"context_version":m["context_version"],"schema_version":m["schema_version"],
                 "context_sha256":t["context_sha256"],"prompt_sha256":t["prompt_sha256"],
                 "raw_sha256":None if raw is None else sha_text(raw),"model_label":meta.get("model_label","미확인"),
                 "observed_at":meta.get("observed_at"),"recorded_at":meta.get("recorded_at"),"tools_and_personalization":meta.get("tools_and_personalization","미확인"),
                 "reason":meta.get("reason",""),"raw_text":raw,"expected_behavior":t["expected_behavior"],**result}
            if attempt==1:
                row.update({k:human.get(k) for k in HUMAN_KEYS})
                row["human_note"]=human.get("note","")
            else:
                # 첫 응답 평가를 수정 응답의 평가로 복사하지 않습니다.
                row.update({k:None for k in HUMAN_KEYS})
                row["human_note"]="수정 응답은 별도 사람 평가 필요"
            all_rows.append(row)
            if attempt==1 and state=="completed" and result["error"] in {"json_error","schema_error"}:
                original=(folder/"prompts"/(t["slot_id"]+".txt")).read_text(encoding="utf-8")
                # 원문·예외 전문을 붙이지 않고 허용된 오류 이름만 전달합니다.
                write_text(target/"repair_prompt.txt",repair_prompt(original,result["error"]))
    write_json(folder/"all_attempts.json",all_rows)
    fields=["slot_id","case_id","variant","repeat","attempt","source_mode","execution_state","model_label","observed_at","recorded_at",
            "json_ok","schema_ok","reference_ok","evidence_ok","task_ok","insufficiency_ok","error","auto_status","human_note"]
    write_csv(folder/"first_response.csv",[r for r in all_rows if r["attempt"]==1],fields)
    write_csv(folder/"all_attempts.csv",all_rows,fields)
    return all_rows


def summarize(rows):
    """PPT 42장: 최초 응답 전체가 분모. 샘플과 실제/미실행/미평가는 분리합니다."""
    report={"groups":[],"no_automatic_winner":True,"caution":"fixture는 모델 품질 지표가 아닙니다. 소수 관찰은 전체 성능 보장이 아닙니다."}
    for mode in sorted({r["source_mode"] for r in rows}):
        for variant in ("A","B"):
            group=[r for r in rows if r["source_mode"]==mode and r["variant"]==variant and r["attempt"]==1]
            if not group: continue
            n=len(group)
            attempted=sum(r["execution_state"]!="not_run" for r in group)
            completed=sum(r["execution_state"]=="completed" for r in group)
            metrics={}
            for key in ("json_ok","schema_ok","reference_ok"):
                passed=sum(r.get(key) is True for r in group)
                # 부족한 실행을 0% 성능처럼 보이지 않게 합니다. N·실행 수·미실행 수는 항상 공개합니다.
                metrics[key]={"passed":passed,"denominator_planned":n,
                    "rate":passed/n if attempted==n else None,"status":"complete" if attempted==n else "incomplete"}
            human={}
            for key in HUMAN_KEYS:
                rated=[r[key] for r in group if r.get(key) is not None]
                human[key]={"passed":sum(x is True for x in rated),"rated":len(rated),"unrated":n-len(rated),
                            "rate":sum(x is True for x in rated)/len(rated) if rated else None}
            eligible=[r for r in group if r["execution_state"]=="completed" and r["error"] in {"json_error","schema_error"}]
            eligible_ids={r["slot_id"] for r in eligible}
            second=[r for r in rows if r["source_mode"]==mode and r["variant"]==variant and r["attempt"]==2 and r["slot_id"] in eligible_ids and r["execution_state"]!="not_run"]
            recovered=sum(r["execution_state"]=="completed" and r["error"] is None for r in second)
            report["groups"].append({"source_mode":mode,"variant":variant,"N":n,"attempted":attempted,"completed":completed,
                "not_run":n-attempted,"refused":sum(r["execution_state"]=="refused" for r in group),
                "incomplete":sum(r["execution_state"]=="incomplete" for r in group),"failed":sum(r["execution_state"]=="failed" for r in group),
                "automatic":metrics,"human":human,"retry":{"eligible":len(eligible),"attempted":len(second),"recovered":recovered,
                "rate":recovered/len(second) if second else None},
                "claim_scope":"checker_only" if mode=="fixture" else "manual_ui_observation"})
    return report


def write_summary(folder, report):
    folder=Path(folder)
    write_json(folder/"summary.json",report)
    lines=["# A/B 관찰 요약", "", "미실행·미평가를 지우지 않습니다. B의 승리를 미리 정하지 않습니다.", "",
           "| 출처 | 버전 | 계획 N | 실행 | 미실행 | JSON 통과 | Schema 통과 | 참조 통과 | 근거 평가 수 |", "|---|---|---:|---:|---:|---:|---:|---:|---:|"]
    for g in report["groups"]:
        lines.append(f'| {g["source_mode"]} | {g["variant"]} | {g["N"]} | {g["attempted"]} | {g["not_run"]} | {g["automatic"]["json_ok"]["passed"]} | {g["automatic"]["schema_ok"]["passed"]} | {g["automatic"]["reference_ok"]["passed"]} | {g["human"]["evidence_ok"]["rated"]} |')
    lines += ["", "실제 자동 검사 통과는 내용의 사실성 보장이 아닙니다. 질문·주장·인용 본문을 대조하세요.",
              "같은 조건의 반복/수정 응답은 all_attempts에서 확인합니다. 첫 응답 지표는 attempt=1만 사용합니다.",
              "ChatGPT 화면 실험의 제어할 수 없는 모델·도구·개인화 항목은 미확인으로 남깁니다.",
              "근거 메모는 responses/<slot>/human_review.json에 입력합니다. fixture 결과로 Prompt 우열을 주장하지 않습니다."]
    write_text(folder/"summary.md","\n".join(lines)+"\n")
