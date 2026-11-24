"""Day27 강의 실습. 실행은 역할 폴더에서 Python으로 실행합니다."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
ROLE_ROOT=next(p for p in HERE.parents if (p/'coursekit').is_dir())
sys.path.insert(0,str(ROLE_ROOT))


import argparse

from coursekit.workshops import STAGE_RUNNERS

from coursekit.io import save_report



from chains.rewrite import apply_rewrite

from schemas.result import record_rewrite

from validation.constraints import check_semantics

from services.audit import audit_rewrite

def main():
    parser=argparse.ArgumentParser(description='Day27 실습 02 · 02_query_rewrite')
    parser.add_argument('--offline',action='store_true',help='교육용 고정 데이터·점수. 모델 품질 실측이 아닙니다.')
    args=parser.parse_args()
    # Day27: 일부 진단 실습 외에는 기본 실행이 실제 모델·DB·LLM 경로입니다.
    report=STAGE_RUNNERS[2](args.offline,[apply_rewrite,record_rewrite,check_semantics,audit_rewrite])
    path=save_report(HERE,'day27_02_'+('fixture' if args.offline else 'live')+'.json',report)
    print('실습 02 결과:', path)
    print('보고서를 확인하고 reports/review.md에 원문 대조·실행 모드를 기록하세요.')

if __name__=='__main__':main()
