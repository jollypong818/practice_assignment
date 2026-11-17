"""Day22 · 사용량·시간·비용 | PPT 39~46 | 03_advanced
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
# cached_tokens는 input_tokens의 일부이며 reasoning_tokens는 output_tokens의 일부입니다.
# 입력을 비캐시/캐시로 나누어 각각의 단가를 적용하고, 출력은 한 번만 더합니다.
# None은 관측하지 못했다는 뜻입니다. 실패 시 사용량을 0으로 채우면 실제보다 비용이 작아 보입니다.
# Decimal 계산은 적용한 단가표에 따른 추정이며 세금·환율·특별 과금까지 확정한 청구서가 아닙니다.
