"""Day27 강의 실습. 실행은 역할 폴더에서 Python으로 실행합니다."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
ROLE_ROOT=next(p for p in HERE.parents if (p/'coursekit').is_dir())
sys.path.insert(0,str(ROLE_ROOT))


import argparse

from coursekit.workshops import STAGE_RUNNERS

from coursekit.io import save_report



def plan_queries(base, extras):
    """원 질문을 포함한 서로 다른 질문 2개로 시작합니다."""
    # BEGIN D27-03-B01
    # ANSWER D27-03-B01: 원 질문을 포함한 서로 다른 질문 2개로 시작합니다.
    # 1. 입력: base, extras (필요한 값만 받습니다.)
    # 2. 절차: 원 질문을 포함한 서로 다른 질문 2개로 시작합니다.
    # 3. 반환: 호출한 Stage가 사용할 값/상태를 반환합니다.
    # 4. 주의: 오류를 빈 결과로 숨기지 않고 출처·필터 계약을 유지합니다.
    from coursekit.multi_query import unique_queries
    return unique_queries(base,extras[:1],max_queries=2)
    # END D27-03-B01


def merge_candidates(pairs):
    """chunk_id를 중복 제거 키로 사용하고 found_by_query를 Metadata에 기록합니다."""
    # BEGIN D27-03-B02
    # ANSWER D27-03-B02: chunk_id를 중복 제거 키로 사용하고 found_by_query를 Metadata에 기록합니다.
    # 1. 입력: pairs (필요한 값만 받습니다.)
    # 2. 절차: chunk_id를 중복 제거 키로 사용하고 found_by_query를 Metadata에 기록합니다.
    # 3. 반환: 호출한 Stage가 사용할 값/상태를 반환합니다.
    # 4. 주의: 오류를 빈 결과로 숨기지 않고 출처·필터 계약을 유지합니다.
    from coursekit.multi_query import merge_found
    return merge_found(pairs)
    # END D27-03-B02


def main():
    parser=argparse.ArgumentParser(description='Day27 실습 03 · 03_multi_query')
    parser.add_argument('--offline',action='store_true',help='교육용 고정 데이터·점수. 모델 품질 실측이 아닙니다.')
    args=parser.parse_args()
    # Day27: 일부 진단 실습 외에는 기본 실행이 실제 모델·DB·LLM 경로입니다.
    report=STAGE_RUNNERS[3](args.offline,[plan_queries,merge_candidates])
    path=save_report(HERE,'day27_03_'+('fixture' if args.offline else 'live')+'.json',report)
    print('실습 03 결과:', path)
    print('보고서를 확인하고 reports/review.md에 원문 대조·실행 모드를 기록하세요.')

if __name__=='__main__':main()
