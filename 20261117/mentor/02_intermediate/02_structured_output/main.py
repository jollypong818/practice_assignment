"""Day22 · 메시지와 출력 계약 | PPT 14~23 | 02_intermediate
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
# instructions는 작업 규칙, input은 이번 질문과 선택된 근거입니다. 예상 정답은 전송하지 않습니다.
# 공급자 Wire Schema와 로컬 KnowledgeAnswer를 나눕니다. 로컬 길이·양수 ID·상태 조합은 계속 검사합니다.
# 공급자 status=completed와 JSON 안의 status=answered는 다른 값입니다.
# 거절은 refusal 콘텐츠로 올 수 있으며 이를 JSON 오류로 바꿔 재시도해서는 안 됩니다.
