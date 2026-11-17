"""Day22 · AI 지식 답변 생성기 v2 | PPT 60~68 | 02_intermediate
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
# H질문은 전날 보았던 연동·회귀 확인 사례입니다. 새로운 holdout 일반화 성능으로 주장하지 않습니다.
# H01은 Streaming으로 보내므로 별도 유료 예시 호출을 늘리지 않아도 됩니다.
# Schema/출처 규칙을 통과한 뒤에도 evidence_ok는 사람이 검토하기 전까지 None입니다.
# 실패·미실행 행을 삭제하지 말고, 캐시 원출처와 실제/모의 지표를 분리해서 설명하게 합니다.
