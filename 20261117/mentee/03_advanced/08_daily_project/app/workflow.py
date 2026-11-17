"""Day22 · AI 지식 답변 생성기 v2 | PPT 60~68 | 03_advanced
공통 제공 코드는 교시 독립 시작점입니다. 본 파일의 TODO 함수를 실행 경로에 연결합니다.
"""
from pathlib import Path
from coursekit.support import parse_args, daily_project
from coursekit.io import write_json

from .project import project_cases, project_rows, project_summary, check_project, compare_first_and_last, shared_limits, missing_usage_check
HERE=Path(__file__).resolve().parents[1]

def main():
    args=parse_args(HERE)
    runs=daily_project(args,prepare_cases=project_cases,make_table=project_rows,finish_summary=project_summary,policy=shared_limits())
    if isinstance(runs,list):
        check_project(runs)
        write_json(args.output_dir/"first_vs_final.json",compare_first_and_last(runs))
    assert shared_limits().max_sends_total==4
    missing_usage_check()
