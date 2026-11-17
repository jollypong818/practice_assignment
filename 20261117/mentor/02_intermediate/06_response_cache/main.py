"""Day22 · 승인 응답 캐시 | PPT 47~52 | 02_intermediate
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
# 같은 ID라도 본문이 바뀌면 답의 근거가 달라집니다. ID 목록만 캐시 키로 쓰지 않습니다.
# 자동 Schema 통과는 의미적 사실성 통과가 아닙니다. 사람이 질문·주장·인용 본문을 검토한 answered만 승인합니다.
# scope 키는 권한 검사 자체가 아닙니다. 실제 서비스에서는 인증된 권한 범위와 무효화 정책이 필요합니다.
# hit는 새로운 API 전송과 사용량이 0입니다. origin_run_id로 원래 생성 비용을 중복 합산하지 않습니다.
