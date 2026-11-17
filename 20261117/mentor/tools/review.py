"""모델의 실제 근거 검토는 사람이 합니다. 자동 승인·가짜 평가값을 넣지 않습니다."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import argparse
import time
from coursekit.io import read_json,write_json,digest


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--run-file",type=Path,required=True)
    parser.add_argument("--decision",choices=["approve","reject"],required=True)
    parser.add_argument("--note",required=True)
    args=parser.parse_args()
    run=read_json(args.run_file)
    if not args.note.strip() or len(args.note)>500:
        raise SystemExit("실제 주장·근거를 대조한 이유를 1~500자로 기록하세요")
    if run.get("run_status")!="validated" or run.get("source_mode") not in {"api_live","simulated"}:
        raise SystemExit("자동 검사 미통과/미실행/캐시 행은 새로 승인하지 않습니다")
    review_file=args.run_file.with_name("review.json")
    if review_file.exists():
        raise SystemExit("기존 사람 검토를 덮어쓰지 않습니다. 변경 이유와 함께 별도 새 실험을 만드세요")
    review={"run_id":run["run_id"],"run_hash":digest(run),"decision":args.decision,
            "evidence_ok":args.decision=="approve","note":args.note.strip(),"reviewed_at_epoch":time.time(),
            "origin_source_mode":run["source_mode"]}
    write_json(review_file,review)
    print("사람 검토 저장:",review_file)
    if run["answer_object"]["status"]!="answered":
        print("정보 부족 응답의 검토는 기록하지만 성공 답변 캐시에는 넣지 않습니다.")

if __name__=="__main__":
    main()
