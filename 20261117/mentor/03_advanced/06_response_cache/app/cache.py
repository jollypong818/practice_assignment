"""Day22 · 승인 응답 캐시 | PPT 47~52 | 03_advanced
공통 제공 코드는 교시 독립 시작점입니다. 본 파일의 TODO 함수를 실행 경로에 연결합니다.
"""
from copy import deepcopy
from coursekit.io import digest
from coursekit.request import build_request as checkpoint_request
from coursekit.cache import read_cache as checkpoint_cache

def key_of(request, scope, validator_version="day21-v1"):
    # TODO D22-06-A01: 질문뿐 아니라 모델·전체요청·Schema·검증버전·scope로 캐시키를 만드세요.
    # 입력·완료 기준: API키는포함하지않습니다. 전체본문이키에들어가야같은ID의내용변경도감지합니다.
    # BEGIN D22-06-A01
    # 해설: API키는포함하지않습니다. 전체본문이키에들어가야같은ID의내용변경도감지합니다.
    basis={"scope":scope,"model":request["model"],"request":request,
           "format":request.get("text",{}).get("format"),"validator_version":validator_version}
    return digest(basis)
    # END D22-06-A01

def approved_cache(cache, key, now, provided_ids, *, expected_source, scope):
    # TODO D22-06-A02: 현재문맥·실행출처·scope와함께 제공된 안전한캐시검사를 호출하세요.
    # 입력·완료 기준: 만료·미승인·현재출처불일치는미스입니다. 승인하려면tools/review.py로사람이기록합니다.
    # BEGIN D22-06-A02
    # 해설: 만료·미승인·현재출처불일치는미스입니다. 승인하려면tools/review.py로사람이기록합니다.
    return checkpoint_cache(cache,key,now,provided_ids,expected_source=expected_source,scope=scope)
    # END D22-06-A02

def compare_context_keys():
    # TODO D22-06-A03: 같은ID의본문변경이캐시키를바꾸는지확인하세요.
    # 입력·완료 기준: 이키비교는전송0회의모의검사입니다. 실제재사용은먼저생성·사람승인후reuse명령으로확인합니다.
    # BEGIN D22-06-A03
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
    # END D22-06-A03

def model_key_check():
    # TODO D22-06-A04: 모델선택만바뀌어도다른키가되는지확인하세요.
    # 입력·완료 기준: 스트리밍여부는출력전달방식이며요청내생성설정은같게유지합니다.
    # BEGIN D22-06-A04
    # 해설: 스트리밍여부는출력전달방식이며요청내생성설정은같게유지합니다.
    from coursekit.io import input_parts
    from coursekit.config import load_settings
    case,rows,prompt=input_parts("H01")
    models=load_settings("simulated").models
    a=checkpoint_request(models["fast"],prompt,case["question"],rows)
    b=checkpoint_request(models["quality"],prompt,case["question"],rows)
    assert key_of(a,"classroom-demo")!=key_of(b,"classroom-demo")
    return True
    # END D22-06-A04

def ttl_check():
    # TODO D22-06-A05: 만료시간에같거나지난캐시가재사용되지않는지검사하세요.
    # 입력·완료 기준: TTL을읽을때마다연장하지않습니다.
    # BEGIN D22-06-A05
    # 해설: TTL을읽을때마다연장하지않습니다.
    fake={"k":{"expires_at":10.0,"human_approved":True}}
    assert approved_cache(fake,"k",10.0,{103},expected_source="simulated",scope="classroom-demo") is None
    return True
    # END D22-06-A05

def scope_and_version_check():
    # TODO D22-06-A06: 권한범위와검증버전의변경이키를바꾸는지검사하세요.
    # 입력·완료 기준: scope 문자열은실제인증시스템대체물이아닙니다. 학습용권한경계입니다.
    # BEGIN D22-06-A06
    # 해설: scope 문자열은실제인증시스템대체물이아닙니다. 학습용권한경계입니다.
    from coursekit.io import input_parts
    from coursekit.config import load_settings
    case,rows,prompt=input_parts("H01")
    req=checkpoint_request(load_settings("simulated").models["fast"],prompt,case["question"],rows)
    assert key_of(req,"group-a")!=key_of(req,"group-b")
    assert key_of(req,"group-a","v1")!=key_of(req,"group-a","v2")
    return True
    # END D22-06-A06

def check_cache_accounting(result):
    # TODO D22-06-A07: 캐시히트는새전송0·현재사용량0·원래실행ID를남기는지확인하세요.
    # 입력·완료 기준: 캐시데이터의원출처api_live/simulated를함께보존합니다.
    # BEGIN D22-06-A07
    # 해설: 캐시데이터의원출처api_live/simulated를함께보존합니다.
    if result["source_mode"]=="app_cache":
        assert result["new_api_send_count"]==0 and result["estimated_usd"]=="0"
        assert result["usage"]["input_tokens"]==0 and result.get("origin_run_id")
    return True
    # END D22-06-A07
