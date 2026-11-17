"""Day22 · AI 지식 답변 생성기 v2 | PPT 60~68 | 01_basic
공통 제공 코드는 교시 독립 시작점입니다. 본 파일의 TODO 함수를 실행 경로에 연결합니다.
"""
from pathlib import Path
import sys
HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))

from coursekit.support import parse_args, guarded, daily_project
from coursekit.metrics import summarize_runs
from coursekit.records import table_rows

def project_cases():
    # TODO D22-08-B01: 최종연동확인질문H01·H02·H03을같은순서로지정하세요.
    # 입력·완료 기준: 이미본질문이므로새holdout의일반화성능이라고부르지않습니다.
    # BEGIN D22-08-B01
    cases = []  # H01→H02→H03. H01은Streaming입니다.
    raise NotImplementedError("D22-08-B01: TODO를 완성하고 이 raise를 제거하세요")
    return cases  # 위 TODO와 raise 제거를 마친 뒤 반환합니다.
    # END D22-08-B01

def project_rows(runs):
    # TODO D22-08-B02: 각실행의상태·사용량·시간을표행으로연결하세요.
    # 입력·완료 기준: 실패한행도버리지않습니다. 모든질문의예상답을실측답으로채우지않습니다.
    # BEGIN D22-08-B02
    rows = []  # table_rows(runs)는unknown과source구분에필요한필드를제공합니다.
    raise NotImplementedError("D22-08-B02: TODO를 완성하고 이 raise를 제거하세요")
    return rows  # 위 TODO와 raise 제거를 마친 뒤 반환합니다.
    # END D22-08-B02

def project_summary(runs):
    # TODO D22-08-B03: 실제·모의·캐시·미실행을분리하여요약하세요.
    # 입력·완료 기준: 소수관찰로P95·SLA·보편적모델우열을주장하지않습니다.
    # BEGIN D22-08-B03
    summary = {}  # summarize_runs(runs)
    raise NotImplementedError("D22-08-B03: TODO를 완성하고 이 raise를 제거하세요")
    return summary  # 위 TODO와 raise 제거를 마친 뒤 반환합니다.
    # END D22-08-B03

def check_project(runs):
    # TODO D22-08-B04: 자동검사후사람미평가None을유지하고전송상한을확인하세요.
    # 입력·완료 기준: 사람평가는tools/review.py의별도파일로남깁니다. 새API·DB·RAG는만들지않습니다.
    # BEGIN D22-08-B04
    for run in runs:
        evidence = run.get("evidence_ok")  # 사람평가전None
        sends = run.get("new_api_send_count", 0)
        # None유지·전송4이하를assert합니다.
        pass
    raise NotImplementedError("D22-08-B04: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-08-B04

def main():
    args=parse_args(HERE)
    runs=daily_project(args,prepare_cases=project_cases,make_table=project_rows,finish_summary=project_summary)
    if isinstance(runs,list):
        check_project(runs)

if __name__=="__main__":
    guarded(main)
