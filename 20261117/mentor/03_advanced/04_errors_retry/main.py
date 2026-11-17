"""Day22 · 오류와 제한 재시도 | PPT 32~38 | 03_advanced
공통 제공 코드는 교시 독립 시작점입니다. 본 파일의 TODO 함수를 실행 경로에 연결합니다.
"""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from coursekit.support import guarded
from app.workflow import main
if __name__=="__main__":
    guarded(main)

# 강사용 핵심 해설
# 같은 429라도 일시적 속도 제한과 할당량 부족은 조치가 다릅니다. 원인을 모르면 자동 반복하지 않습니다.
# 모델 출력 수정 2회 × 통신 전송 2회가 총4회를 넘지 않도록 한 예산을 공유합니다.
# timeout은 서버에서 처리하지 않았다는 증거가 아닙니다. 이 수업은 중복 비용을 줄이기 위해 자동 재전송하지 않습니다.
# Retry-After가 남은 시간보다 크면 기다림을 줄이는 대신 deferred로 종료합니다.
