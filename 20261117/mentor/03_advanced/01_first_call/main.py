"""Day22 · 첫 실제 응답 | PPT 6~13 | 03_advanced
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
# model은 문서의 후보 식별자이며 계정 접근권까지 보장하지 않습니다.
# create 한 번은 전송 한 번입니다. 재시도는 공통 실행기 한 곳에서만 관리합니다.
# 첫 성공은 연결 확인이고, 사실에 맞는 답인지와 출력 계약은 별도 검사입니다.
