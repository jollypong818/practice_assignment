"""Day22 · 오류와 제한 재시도 | PPT 32~38 | 02_intermediate
공통 제공 코드는 교시 독립 시작점입니다. 본 파일의 TODO 함수를 실행 경로에 연결합니다.
"""
from pathlib import Path
from coursekit.support import parse_args
from coursekit.errors import classify_error as checkpoint_classify
from coursekit.runner import RetryPolicy
from coursekit.labs import failure_scenarios

def classify(error):
    # TODO D22-04-I01: 401·403은 중단하고, 429의 quota와 일시적 제한을 구분하세요.
    # 입력·완료 기준: 알 수 없는429는 무조건 재시도하지 않습니다. 실제로 제한을 유발하는 호출은 금지합니다.
    # BEGIN D22-04-I01
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
    # END D22-04-I01

def make_policy():
    # TODO D22-04-I02: 생성 최대2·생성별 전송최대2·전체 전송최대4를 설정하세요.
    # 입력·완료 기준: SDK max_retries=0은 제공 코드에 설정되어 있습니다. 무한 fallback을 추가하지 않습니다.
    # BEGIN D22-04-I02
    # 해설: SDK max_retries=0은 제공 코드에 설정되어 있습니다. 무한 fallback을 추가하지 않습니다.
    return RetryPolicy(max_generations=2,max_sends_per_generation=2,max_sends_total=4,elapsed_budget_s=60.0)
    # END D22-04-I02

def delay(attempt, retry_after_s, remaining_s, jitter=0.0):
    # TODO D22-04-I03: 헤더 최소 대기와 지수 대기 중 큰 값을 계산하세요.
    # 입력·완료 기준: 함수에 전달되는 헤더값은 이미 검증된 초 단위입니다.
    # BEGIN D22-04-I03
    # 해설: 함수에 전달되는 헤더값은 이미 검증된 초 단위입니다.
    hinted=0.0 if retry_after_s is None else retry_after_s
    if hinted<0 or remaining_s<=0:
        return None
    wait=max(hinted,min(8.0,2**min(attempt-1,3)))+jitter
    # END D22-04-I03
    # TODO D22-04-I04: 대기시간이 남은 작업 예산 이상이면 None으로 중단하세요.
    # 입력·완료 기준: 대기 후 실행기는 남은 예산과 횟수를 다시 검사합니다.
    # BEGIN D22-04-I04
    # 해설: 대기 후 실행기는 남은 예산과 횟수를 다시 검사합니다.
    return None if wait>=remaining_s else wait
    # END D22-04-I04

def check_attempts(results):
    # TODO D22-04-I05: 각 시도의 번호가 누락되지 않고 총4이하인지 확인하세요.
    # 입력·완료 기준: 실패한 첫 시도도 목록에서 지우지 않습니다.
    # BEGIN D22-04-I05
    # 해설: 실패한 첫 시도도 목록에서 지우지 않습니다.
    for result in results:
        attempts=result["attempts"]
        assert len(attempts)<=4
        assert [a["send_attempt"] for a in attempts]==list(range(1,len(attempts)+1))
    return True
    # END D22-04-I05

HERE = Path(__file__).resolve().parent

def main():
    args=parse_args(HERE)
    results=failure_scenarios(args,classifier=classify,delay=delay,policy=make_policy())
    check_attempts(results)
