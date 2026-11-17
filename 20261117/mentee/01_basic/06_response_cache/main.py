"""Day22 · 승인 응답 캐시 | PPT 47~52 | 01_basic
공통 제공 코드는 교시 독립 시작점입니다. 본 파일의 TODO 함수를 실행 경로에 연결합니다.
"""
from pathlib import Path
import sys
HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))

from copy import deepcopy
from coursekit.support import parse_args, guarded, cache_lab
from coursekit.io import write_json, digest
from coursekit.request import build_request as checkpoint_request
from coursekit.cache import read_cache as checkpoint_cache

def key_of(request, scope, validator_version="day21-v1"):
    # TODO D22-06-B01: 질문뿐 아니라 모델·전체요청·Schema·검증버전·scope로 캐시키를 만드세요.
    # 입력·완료 기준: API키는포함하지않습니다. 전체본문이키에들어가야같은ID의내용변경도감지합니다.
    # BEGIN D22-06-B01
    basis = {"scope": scope, "model": None, "request": request,
             "format": None, "validator_version": validator_version}
    key = None  # digest(basis): 정렬된JSON의SHA-256
    raise NotImplementedError("D22-06-B01: TODO를 완성하고 이 raise를 제거하세요")
    return key  # 위 TODO와 raise 제거를 마친 뒤 반환합니다.
    # END D22-06-B01

def approved_cache(cache, key, now, provided_ids, *, expected_source, scope):
    # TODO D22-06-B02: 현재문맥·실행출처·scope와함께 제공된 안전한캐시검사를 호출하세요.
    # 입력·완료 기준: 만료·미승인·현재출처불일치는미스입니다. 승인하려면tools/review.py로사람이기록합니다.
    # BEGIN D22-06-B02
    cached = None  # checkpoint_cache(..., expected_source=expected_source, scope=scope)
    # None은미스입니다. 새답변을가짜로만들지않습니다.
    raise NotImplementedError("D22-06-B02: TODO를 완성하고 이 raise를 제거하세요")
    return cached  # 위 TODO와 raise 제거를 마친 뒤 반환합니다.
    # END D22-06-B02

def compare_context_keys():
    # TODO D22-06-B03: 같은ID의본문변경이캐시키를바꾸는지확인하세요.
    # 입력·완료 기준: 이키비교는전송0회의모의검사입니다. 실제재사용은먼저생성·사람승인후reuse명령으로확인합니다.
    # BEGIN D22-06-B03
    from coursekit.io import input_parts
    from coursekit.config import load_settings
    case, selected, instructions = input_parts("H01")
    model = load_settings("simulated").models["fast"]
    first = checkpoint_request(model, instructions, case["question"], selected)
    changed = deepcopy(selected)  # 원본JSON파일은바꾸지않습니다.
    # changed[0]["content"]수정 → 두번째request → key비교
    raise NotImplementedError("D22-06-B03: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-06-B03

def main():
    args=parse_args(HERE)
    write_json(args.output_dir/"cache_key_checks.json",compare_context_keys())
    result=cache_lab(args,key_builder=key_of,cache_reader=approved_cache)

if __name__=="__main__":
    guarded(main)
