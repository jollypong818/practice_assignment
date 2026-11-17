"""Day22 · 명시적 모델 선택 | PPT 53~59 | 03_advanced
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
# fast/quality는 수업 설정 이름입니다. quality가 항상 정확하다는 뜻이 아닙니다.
# 모델 선택은 호출 전에 명시적으로 하며, 권한 오류를 숨기기 위해 다른 모델을 자동 호출하지 않습니다.
# 비교할 때는 질문·문맥·출력 계약을 같게 하고 검증 및 사용량 기록 형식을 유지합니다.
