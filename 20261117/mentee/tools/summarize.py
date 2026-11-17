"""실측·모의·캐시·미실행을 분리하고 review.json을 실제 표에 반영합니다."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from coursekit.io import read_json,write_json,digest
from coursekit.records import save_table,table_rows
from coursekit.metrics import summarize_runs
from copy import deepcopy
import argparse
import uuid

p=argparse.ArgumentParser()
p.add_argument("--outputs",type=Path,required=True)
args=p.parse_args()
runs=[]
for path in sorted(args.outputs.glob("runs/*/run.json")):
    run=read_json(path)
    review_path=path.with_name("review.json")
    if review_path.exists():
        review=read_json(review_path)
        if review["run_hash"]!=digest(run):
            raise SystemExit("검토 이후 원문이 변경되어 집계를 중단합니다: "+str(path))
        run=deepcopy(run)
        run["evidence_ok"]=review["evidence_ok"]
    runs.append(run)
if not runs:
    raise SystemExit("실행 기록이 없습니다")
folder=args.outputs/"tables"/str(uuid.uuid4())
save_table(folder/"observations.csv",table_rows(runs))
write_json(folder/"summary.json",summarize_runs(runs))
print(folder)
