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
    status = error.status
    codes = {error.code, error.error_type}
    if status == 401:
        result = {"kind": "auth_error", "retryable": None}  # 기다려도 키는 바뀌지 않습니다.
    elif status == 429:
        result = {}  # quota이면중단, rate_limit_exceeded면제한 재시도
    # 그 외는 checkpoint_classify(error)를 이용합니다.
    raise NotImplementedError("D22-04-B01: TODO를 완성하고 이 raise를 제거하세요")
    return result  # 위 TODO와 raise 제거를 마친 뒤 반환합니다.
    # END D22-04-B01

def make_policy():
    # TODO D22-04-B02: 생성 최대2·생성별 전송최대2·전체 전송최대4를 설정하세요.
    # 입력·완료 기준: SDK max_retries=0은 제공 코드에 설정되어 있습니다. 무한 fallback을 추가하지 않습니다.
    # BEGIN D22-04-B02
    limits = {"max_generations": None, "max_sends_per_generation": None, "max_sends_total": None}
    # RetryPolicy(**limits, elapsed_budget_s=60.0)
    raise NotImplementedError("D22-04-B02: TODO를 완성하고 이 raise를 제거하세요")
    # END D22-04-B02

def delay(attempt, retry_after_s, remaining_s, jitter=0.0):
    # TODO D22-04-B03: 제공된 대기 함수에 남은 예산을 전달하고 반환값을 유지하세요.
    # 입력·완료 기준: 서버의 최소 대기를 짧게 줄이지 않습니다.
    # BEGIN D22-04-B03
    wait = None  # checkpoint_delay(attempt, retry_after_s, remaining_s, jitter)
    # None은 이번 실행을중단한다는 뜻입니다. 0으로 바꾸지 않습니다.
    raise NotImplementedError("D22-04-B03: TODO를 완성하고 이 raise를 제거하세요")
    return wait  # 위 TODO와 raise 제거를 마친 뒤 반환합니다.
    # END D22-04-B03

def main():
    args=parse_args(HERE)
    results=failure_scenarios(args,classifier=classify,delay=delay,policy=make_policy())

if __name__=="__main__":
    guarded(main)
