"""Day22 · AI 지식 답변 생성기 v2 | PPT 60~68 | 02_intermediate
공통 제공 코드는 교시 독립 시작점입니다. 본 파일의 TODO 함수를 실행 경로에 연결합니다.
"""
from pathlib import Path
from coursekit.support import parse_args, daily_project
from coursekit.io import write_json
from coursekit.metrics import summarize_runs
from coursekit.records import table_rows

def project_cases():
    # TODO D22-08-I01: 최종연동확인질문H01·H02·H03을같은순서로지정하세요.
    # 입력·완료 기준: 이미본질문이므로새holdout의일반화성능이라고부르지않습니다.
    # BEGIN D22-08-I01
    # 해설: 이미본질문이므로새holdout의일반화성능이라고부르지않습니다.
    return ["H01","H02","H03"]
    # END D22-08-I01

def project_rows(runs):
    # TODO D22-08-I02: 각실행의상태·사용량·시간을표행으로연결하세요.
    # 입력·완료 기준: 실패한행도버리지않습니다. 모든질문의예상답을실측답으로채우지않습니다.
    # BEGIN D22-08-I02
    # 해설: 실패한행도버리지않습니다. 모든질문의예상답을실측답으로채우지않습니다.
    rows=table_rows(runs)
    return rows
    # END D22-08-I02

def project_summary(runs):
    # TODO D22-08-I03: 실제·모의·캐시·미실행을분리하여요약하세요.
    # 입력·완료 기준: 소수관찰로P95·SLA·보편적모델우열을주장하지않습니다.
    # BEGIN D22-08-I03
    # 해설: 소수관찰로P95·SLA·보편적모델우열을주장하지않습니다.
    return summarize_runs(runs)
    # END D22-08-I03

def check_project(runs):
    # TODO D22-08-I04: 자동검사후사람미평가None을유지하고전송상한을확인하세요.
    # 입력·완료 기준: 사람평가는tools/review.py의별도파일로남깁니다. 새API·DB·RAG는만들지않습니다.
    # BEGIN D22-08-I04
    # 해설: 사람평가는tools/review.py의별도파일로남깁니다. 새API·DB·RAG는만들지않습니다.
    for run in runs:
        assert run.get("evidence_ok") is None
        assert run.get("new_api_send_count",0)<=4
    return True
    # END D22-08-I04

def compare_first_and_last(runs):
    # TODO D22-08-I05: 최초시도와마지막시도의상태를분리하여보존하세요.
    # 입력·완료 기준: 첫실패를마지막성공으로덮어쓰지않습니다.
    # BEGIN D22-08-I05
    # 해설: 첫실패를마지막성공으로덮어쓰지않습니다.
    rows=[]
    for run in runs:
        attempts=run.get("attempts",[])
        rows.append({"run_id":run["run_id"],"first_error":attempts[0].get("error") or attempts[0].get("validation_error") if attempts else None,
                     "last_status":run["run_status"],"attempt_count":len(attempts),"source_mode":run["source_mode"]})
    return rows
    # END D22-08-I05

HERE = Path(__file__).resolve().parent

def main():
    args=parse_args(HERE)
    runs=daily_project(args,prepare_cases=project_cases,make_table=project_rows,finish_summary=project_summary)
    if isinstance(runs,list):
        check_project(runs)
        write_json(args.output_dir/"first_vs_final.json",compare_first_and_last(runs))
