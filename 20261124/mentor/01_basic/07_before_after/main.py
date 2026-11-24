"""Day27 강의 실습. 실행은 역할 폴더에서 Python으로 실행합니다."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
ROLE_ROOT=next(p for p in HERE.parents if (p/'coursekit').is_dir())
sys.path.insert(0,str(ROLE_ROOT))


import argparse

from coursekit.workshops import STAGE_RUNNERS

from coursekit.io import save_report



def compare_rankings(before, after, gold):
    """고정한 관련 문서 ID를 Top-2에 포함했는지 확인합니다."""
    # BEGIN D27-07-B01
    # ANSWER D27-07-B01: 고정한 관련 문서 ID를 Top-2에 포함했는지 확인합니다.
    # 1. 입력: before, after, gold (필요한 값만 받습니다.)
    # 2. 절차: 고정한 관련 문서 ID를 Top-2에 포함했는지 확인합니다.
    # 3. 반환: 호출한 Stage가 사용할 값/상태를 반환합니다.
    # 4. 주의: 오류를 빈 결과로 숨기지 않고 출처·필터 계약을 유지합니다.
    from coursekit.evaluation import compare_lists
    return compare_lists(before,after,gold,k=2)
    # END D27-07-B01


def interpret_change(report):
    """순위가 바뀌어도 반드시 개선됐다는 결론을 내리지 않습니다."""
    # BEGIN D27-07-B02
    # ANSWER D27-07-B02: 순위가 바뀌어도 반드시 개선됐다는 결론을 내리지 않습니다.
    # 1. 입력: report (필요한 값만 받습니다.)
    # 2. 절차: 순위가 바뀌어도 반드시 개선됐다는 결론을 내리지 않습니다.
    # 3. 반환: 호출한 Stage가 사용할 값/상태를 반환합니다.
    # 4. 주의: 오류를 빈 결과로 숨기지 않고 출처·필터 계약을 유지합니다.
    before=report['before_contains_gold'];after=report['after_contains_gold']
    if before is None:return 'gold 없음: 인간 검토 필요'
    if before==after:return 'Top-k 관련 문서 포함 여부는 변하지 않음'
    return '관련 문서 Top-k 포함 여부가 달라짐 (추가 검증 필요)' 
    # END D27-07-B02


def main():
    parser=argparse.ArgumentParser(description='Day27 실습 07 · 07_before_after')
    parser.add_argument('--offline',action='store_true',help='교육용 고정 데이터·점수. 모델 품질 실측이 아닙니다.')
    args=parser.parse_args()
    # Day27: 일부 진단 실습 외에는 기본 실행이 실제 모델·DB·LLM 경로입니다.
    report=STAGE_RUNNERS[7](args.offline,[compare_rankings,interpret_change])
    path=save_report(HERE,'day27_07_'+('fixture' if args.offline else 'live')+'.json',report)
    print('실습 07 결과:', path)
    print('보고서를 확인하고 reports/review.md에 원문 대조·실행 모드를 기록하세요.')

if __name__=='__main__':main()
