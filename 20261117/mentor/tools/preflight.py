"""외부 호출 없이 설치·안전한 설정 상태만 확인합니다."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from coursekit.config import load_settings,SetupError
from coursekit.io import environment
import json

print(json.dumps(environment(),ensure_ascii=False,indent=2))
try:
    settings=load_settings("live")
    print("API 키: 설정됨 (값은 출력하지 않음)")
    print("fast 모델:",settings.models["fast"])
    print("quality 모델:",settings.models["quality"] or "미설정 — 실제 비교하지 않음")
    print("SDK 버전이 표시돼도 실제 인증/모델 권한이 확인된 것은 아닙니다.")
except SetupError as exc:
    print("설정 점검:",str(exc))
print("실제 전송 횟수: 0")
