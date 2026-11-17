"""Day22 · Streaming과 완료 판정 | PPT 24~31 | 03_advanced
공통 제공 코드는 교시 독립 시작점입니다. 본 파일의 TODO 함수를 실행 경로에 연결합니다.
"""
from pathlib import Path
from coursekit.support import parse_args, execute_case, emit
from coursekit.io import write_json

from .streaming import receive_event, streaming_choice, compare_runs, timing_view, check_no_terminal
HERE=Path(__file__).resolve().parents[1]

def main():
    args=parse_args(HERE)
    modes=compare_runs() if args.action=="compare" else [streaming_choice()]
    observations=[]
    for use_stream in modes:
        result=execute_case(args,args.case or "H01",stream=use_stream,hooks={"event":receive_event})
        emit(args,result)
        observations.append(timing_view(result))
    check_no_terminal()
    write_json(args.output_dir/"timing_comparison.json",observations)
