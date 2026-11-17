"""Day22 · 오류와 제한 재시도 | PPT 32~38 | 01_basic
공통 제공 코드는 교시 독립 시작점입니다. 본 파일의 TODO 함수를 실행 경로에 연결합니다.
"""
from pathlib import Path
import sys
HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))

from coursekit.support import parse_args, guarded
from coursekit.errors import classify_error as checkpoint_classify, retry_delay as checkpoint_delay
from coursekit.runner import RetryPolicy
from coursekit.labs import failure_scenarios

def classify(error):
    # TODO D22-04-B01: 401·403은 중단하고, 429의 quota와 일시적 제한을 구분하세요.
    # 입력·완료 기준: 알 수 없는429는 무조건 재시도하지 않습니다. 실제로 제한을 유발하는 호출은 금지합니다.
    # BEGIN D22-04-B01
    # 해설: 알 수 없는429는 무조건 재시도하지 않습니다. 실제로 제한을 유발하는 호출은 금지합니다.
    if error.status==401:
        return {"kind":"auth_error","retryable":False}
    if error.status==403:
        return {"kind":"permission_error","retryable":False}
    codes={error.code,error.error_type}
    if error.status==429 and codes & {"insufficient_quota","billing_hard_limit_reached","billing_not_active","usage_limit_reached"}:
        return {"kind":"quota_error","retryable":False}
    if error.status==429 and codes & {"rate_limit_exceeded","rate_limit_error","requests","tokens"}:
        return {"kind":"rate_limit","retryable":True}
    return checkpoint_classify(error)
    # END D22-04-B01

def make_policy():
    # TODO D22-04-B02: 생성 최대2·생성별 전송최대2·전체 전송최대4를 설정하세요.
    # 입력·완료 기준: SDK max_retries=0은 제공 코드에 설정되어 있습니다. 무한 fallback을 추가하지 않습니다.
    # BEGIN D22-04-B02
    # 해설: SDK max_retries=0은 제공 코드에 설정되어 있습니다. 무한 fallback을 추가하지 않습니다.
    return RetryPolicy(max_generations=2,max_sends_per_generation=2,max_sends_total=4,elapsed_budget_s=60.0)
    # END D22-04-B02

def delay(attempt, retry_after_s, remaining_s, jitter=0.0):
    # TODO D22-04-B03: 제공된 대기 함수에 남은 예산을 전달하고 반환값을 유지하세요.
    # 입력·완료 기준: 서버의 최소 대기를 짧게 줄이지 않습니다.
    # BEGIN D22-04-B03
    # 해설: 서버의 최소 대기를 짧게 줄이지 않습니다.
    wait=checkpoint_delay(attempt,retry_after_s,remaining_s,jitter)
    return wait
    # END D22-04-B03

# 강사용 핵심 해설
# 같은 429라도 일시적 속도 제한과 할당량 부족은 조치가 다릅니다. 원인을 모르면 자동 반복하지 않습니다.
# 모델 출력 수정 2회 × 통신 전송 2회가 총4회를 넘지 않도록 한 예산을 공유합니다.
# timeout은 서버에서 처리하지 않았다는 증거가 아닙니다. 이 수업은 중복 비용을 줄이기 위해 자동 재전송하지 않습니다.
# Retry-After가 남은 시간보다 크면 기다림을 줄이는 대신 deferred로 종료합니다.

def main():
    args=parse_args(HERE)
    results=failure_scenarios(args,classifier=classify,delay=delay,policy=make_policy())

if __name__=="__main__":
    guarded(main)
