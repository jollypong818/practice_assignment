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
    # 해설: API키는포함하지않습니다. 전체본문이키에들어가야같은ID의내용변경도감지합니다.
    basis={"scope":scope,"model":request["model"],"request":request,
           "format":request.get("text",{}).get("format"),"validator_version":validator_version}
    return digest(basis)
    # END D22-06-B01

def approved_cache(cache, key, now, provided_ids, *, expected_source, scope):
    # TODO D22-06-B02: 현재문맥·실행출처·scope와함께 제공된 안전한캐시검사를 호출하세요.
    # 입력·완료 기준: 만료·미승인·현재출처불일치는미스입니다. 승인하려면tools/review.py로사람이기록합니다.
    # BEGIN D22-06-B02
    # 해설: 만료·미승인·현재출처불일치는미스입니다. 승인하려면tools/review.py로사람이기록합니다.
    return checkpoint_cache(cache,key,now,provided_ids,expected_source=expected_source,scope=scope)
    # END D22-06-B02

def compare_context_keys():
    # TODO D22-06-B03: 같은ID의본문변경이캐시키를바꾸는지확인하세요.
    # 입력·완료 기준: 이키비교는전송0회의모의검사입니다. 실제재사용은먼저생성·사람승인후reuse명령으로확인합니다.
    # BEGIN D22-06-B03
    # 해설: 이키비교는전송0회의모의검사입니다. 실제재사용은먼저생성·사람승인후reuse명령으로확인합니다.
    from coursekit.io import input_parts
    from coursekit.config import load_settings
    case,selected,instructions=input_parts("H01")
    model=load_settings("simulated").models["fast"]
    first=checkpoint_request(model,instructions,case["question"],selected)
    selected[0]["content"]+=" 실행 환경도 함께 적습니다."
    second=checkpoint_request(model,instructions,case["question"],selected)
    assert key_of(first,"classroom-demo") != key_of(second,"classroom-demo")
    return {"changed_context_miss":True,"source_mode":"simulated","new_api_send_count":0}
    # END D22-06-B03

# 강사용 핵심 해설
# 같은 ID라도 본문이 바뀌면 답의 근거가 달라집니다. ID 목록만 캐시 키로 쓰지 않습니다.
# 자동 Schema 통과는 의미적 사실성 통과가 아닙니다. 사람이 질문·주장·인용 본문을 검토한 answered만 승인합니다.
# scope 키는 권한 검사 자체가 아닙니다. 실제 서비스에서는 인증된 권한 범위와 무효화 정책이 필요합니다.
# hit는 새로운 API 전송과 사용량이 0입니다. origin_run_id로 원래 생성 비용을 중복 합산하지 않습니다.

def main():
    args=parse_args(HERE)
    write_json(args.output_dir/"cache_key_checks.json",compare_context_keys())
    result=cache_lab(args,key_builder=key_of,cache_reader=approved_cache)

if __name__=="__main__":
    guarded(main)
