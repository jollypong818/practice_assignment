"""Day22 · 오류와 제한 재시도 | PPT 32~38 | 03_advanced
공통 제공 코드는 교시 독립 시작점입니다. 본 파일의 TODO 함수를 실행 경로에 연결합니다.
"""
from pathlib import Path
from coursekit.support import parse_args
from coursekit.labs import failure_scenarios

from .policy import classify, make_policy, delay, check_attempts, check_terminal, check_shared_budget
HERE=Path(__file__).resolve().parents[1]

def main():
    args=parse_args(HERE)
    results=failure_scenarios(args,classifier=classify,delay=delay,policy=make_policy())
    check_attempts(results)
    check_terminal(results)
    check_shared_budget(results)
