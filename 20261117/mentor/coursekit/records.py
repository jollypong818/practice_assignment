"""작업별 고유 파일. 원문/첫 실패는 덮어쓰지 않고 사람 평가를 별도 파일로 남깁니다."""
from pathlib import Path
import json
import csv
from .io import write_json, canonical, digest


def save_run(folder, result):
    folder = Path(folder)
    run_dir = folder / "runs" / result["run_id"]
    if run_dir.exists():
        raise ValueError("동일 run_id 덮어쓰기 금지")
    run_dir.mkdir(parents=True)
    write_json(run_dir/"run.json", result)
    # 요청·응답은 가상의 수업 데이터만 기록합니다. API 키·환경변수 전체는 수집하지 않습니다.
    if result.get("request"):
        write_json(run_dir/"request.json", result["request"])
    for index, attempt in enumerate(result.get("attempts",[]),1):
        if attempt.get("raw") is not None:
            (run_dir/f"raw_attempt_{index:02d}.txt").write_text(attempt["raw"],encoding="utf-8")
        if attempt.get("partial_text"):
            (run_dir/f"partial_attempt_{index:02d}.txt").write_text(attempt["partial_text"],encoding="utf-8")
    write_json(run_dir/"review_template.json", {"run_id":result["run_id"],"run_hash":digest(result),
        "decision":None,"note":"질문·answer·인용 본문을 대조한 뒤 tools/review.py로 기록합니다.","evidence_ok":None})
    print("result:", run_dir/"run.json")
    print("status:",result["run_status"],"source:",result["source_mode"],"new_api_sends:",result.get("new_api_send_count",0))
    return run_dir/"run.json"


def table_rows(runs):
    return [{"run_id":r["run_id"],"case_id":r["case_id"],"source_mode":r["source_mode"],
             "run_status":r["run_status"],"model":r.get("model"),"route_reason":r.get("route_reason"),
             "evidence_ok":r.get("evidence_ok"),"new_api_send_count":r.get("new_api_send_count",0),
             "first_text_ms":r.get("first_text_ms"),"request_ms":r.get("request_ms"),"e2e_ms":r.get("e2e_ms"),
             "usage_json":json.dumps(r.get("usage"),ensure_ascii=False),"estimated_usd":r.get("estimated_usd"),
             "origin_run_id":r.get("origin_run_id")} for r in runs]


def save_table(path, rows):
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    if not rows:
        raise ValueError("표 행이 없습니다")
    with Path(path).open("w",encoding="utf-8-sig",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]))
        writer.writeheader()
        # None은 빈칸 대신 unknown으로 명시합니다. 실제 0은 0으로 유지합니다.
        writer.writerows({k:"unknown" if v is None else v for k,v in row.items()} for row in rows)
