"""Day22 · Streaming과 완료 판정 | PPT 24~31 | 02_intermediate
공통 제공 코드는 교시 독립 시작점입니다. 본 파일의 TODO 함수를 실행 경로에 연결합니다.
"""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from coursekit.support import guarded
from logic import main
if __name__=="__main__":
    guarded(main)

# 강사용 핵심 해설
# delta는 텍스트 조각이며 Token 1개와 대응하지 않습니다. 조각 수로 비용을 계산하지 않습니다.
# first_text_ms는 첫 비어 있지 않은 delta를 관측한 시간입니다. 소켓 연결 완료 시간과 다릅니다.
# output_text.done은 문자열 한 부분의 종료일 수 있습니다. 최종 Response의 상태도 확인해야 합니다.
# 중간 출력은 콘솔에 미검증으로 표시하며 DB·캐시에 저장 승인하지 않습니다.
