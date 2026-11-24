"""Day27 강의 실습. 실행은 역할 폴더에서 Python으로 실행합니다."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
ROLE_ROOT=next(p for p in HERE.parents if (p/'coursekit').is_dir())
sys.path.insert(0,str(ROLE_ROOT))


import argparse

from coursekit.workshops import STAGE_RUNNERS

from coursekit.io import save_report



def apply_rewrite(question, history, offline):
    """offline이면 고정 예시, 기본 실행이면 실제 ChatPromptTemplate → Chat Model을 호출합니다."""
    # BEGIN D27-02-B01
    # ANSWER D27-02-B01: offline이면 고정 예시, 기본 실행이면 실제 ChatPromptTemplate → Chat Model을 호출합니다.
    # 1. 입력: question, history, offline (필요한 값만 받습니다.)
    # 2. 절차: offline이면 고정 예시, 기본 실행이면 실제 ChatPromptTemplate → Chat Model을 호출합니다.
    # 3. 반환: 호출한 Stage가 사용할 값/상태를 반환합니다.
    # 4. 주의: 오류를 빈 결과로 숨기지 않고 출처·필터 계약을 유지합니다.
    from coursekit.rewrite import rewrite_query
    return rewrite_query(question,history,offline=offline)
    # END D27-02-B01


def record_rewrite(original, result):
    """원래 질문을 검색 질문으로 덮어쓰지 않습니다."""
    # BEGIN D27-02-B02
    # ANSWER D27-02-B02: 원래 질문을 검색 질문으로 덮어쓰지 않습니다.
    # 1. 입력: original, result (필요한 값만 받습니다.)
    # 2. 절차: 원래 질문을 검색 질문으로 덮어쓰지 않습니다.
    # 3. 반환: 호출한 Stage가 사용할 값/상태를 반환합니다.
    # 4. 주의: 오류를 빈 결과로 숨기지 않고 출처·필터 계약을 유지합니다.
    return {'original_question':original,'search_query':result.search_query,
            'status':result.status,'reason':result.reason}
    # END D27-02-B02


def main():
    parser=argparse.ArgumentParser(description='Day27 실습 02 · 02_query_rewrite')
    parser.add_argument('--offline',action='store_true',help='교육용 고정 데이터·점수. 모델 품질 실측이 아닙니다.')
    args=parser.parse_args()
    # Day27: 일부 진단 실습 외에는 기본 실행이 실제 모델·DB·LLM 경로입니다.
    report=STAGE_RUNNERS[2](args.offline,[apply_rewrite,record_rewrite])
    path=save_report(HERE,'day27_02_'+('fixture' if args.offline else 'live')+'.json',report)
    print('실습 02 결과:', path)
    print('보고서를 확인하고 reports/review.md에 원문 대조·실행 모드를 기록하세요.')

if __name__=='__main__':main()
