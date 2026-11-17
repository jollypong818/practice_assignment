"""Day22 · 승인 응답 캐시 | PPT 47~52 | 03_advanced
공통 제공 코드는 교시 독립 시작점입니다. 본 파일의 TODO 함수를 실행 경로에 연결합니다.
"""
from pathlib import Path
from coursekit.support import parse_args, cache_lab
from coursekit.io import write_json

from .cache import key_of, approved_cache, compare_context_keys, model_key_check, ttl_check, scope_and_version_check, check_cache_accounting
HERE=Path(__file__).resolve().parents[1]

def main():
    args=parse_args(HERE)
    write_json(args.output_dir/"cache_key_checks.json",compare_context_keys())
    model_key_check()
    ttl_check()
    scope_and_version_check()
    result=cache_lab(args,key_builder=key_of,cache_reader=approved_cache)
    check_cache_accounting(result)
