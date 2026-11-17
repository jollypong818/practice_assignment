"""Day22 · 사용량·시간·비용 | PPT 39~46 | 03_advanced
공통 제공 코드는 교시 독립 시작점입니다. 본 파일의 TODO 함수를 실행 경로에 연결합니다.
"""
from pathlib import Path
from coursekit.support import parse_args
from coursekit.labs import usage_lab

from .metrics import usage_of, calculate, make_row, unknown_checks, summarize, check_unknown_total
HERE=Path(__file__).resolve().parents[1]

def main():
    args=parse_args(HERE)
    usage_lab(args,usage_reader=usage_of,calculator=calculate,row_builder=make_row,summarizer=summarize)
    unknown_checks()
    check_unknown_total()
