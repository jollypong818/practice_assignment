"""Day27 강의 실습. 실행은 역할 폴더에서 Python으로 실행합니다."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
ROLE_ROOT=next(p for p in HERE.parents if (p/'coursekit').is_dir())
sys.path.insert(0,str(ROLE_ROOT))


import argparse

from coursekit.workshops import STAGE_RUNNERS

from coursekit.io import save_report



def make_candidate_request(case):
    """candidate_k와 context_k는 다른 제한값입니다."""
    # BEGIN D27-04-B01
    # ANSWER D27-04-B01: candidate_k와 context_k는 다른 제한값입니다.
    # 1. 입력: case (필요한 값만 받습니다.)
    # 2. 절차: candidate_k와 context_k는 다른 제한값입니다.
    # 3. 반환: 호출한 Stage가 사용할 값/상태를 반환합니다.
    # 4. 주의: 오류를 빈 결과로 숨기지 않고 출처·필터 계약을 유지합니다.
    return {'query':case['question'],'category':case['category'],
            'candidate_k':5,'context_k':2}
    # END D27-04-B01


def fetch_documents(retriever, payload):
    """Day26에서 배운 Runnable.invoke로 후보 Document를 받아옵니다."""
    # BEGIN D27-04-B02
    # ANSWER D27-04-B02: Day26에서 배운 Runnable.invoke로 후보 Document를 받아옵니다.
    # 1. 입력: retriever, payload (필요한 값만 받습니다.)
    # 2. 절차: Day26에서 배운 Runnable.invoke로 후보 Document를 받아옵니다.
    # 3. 반환: 호출한 Stage가 사용할 값/상태를 반환합니다.
    # 4. 주의: 오류를 빈 결과로 숨기지 않고 출처·필터 계약을 유지합니다.
    docs=retriever.invoke(payload)
    if len(docs)>payload['candidate_k']:raise ValueError('candidate_k 초과')
    return docs
    # END D27-04-B02


def main():
    parser=argparse.ArgumentParser(description='Day27 실습 04 · 04_candidate_retrieval')
    parser.add_argument('--offline',action='store_true',help='교육용 고정 데이터·점수. 모델 품질 실측이 아닙니다.')
    args=parser.parse_args()
    # Day27: 일부 진단 실습 외에는 기본 실행이 실제 모델·DB·LLM 경로입니다.
    report=STAGE_RUNNERS[4](args.offline,[make_candidate_request,fetch_documents])
    path=save_report(HERE,'day27_04_'+('fixture' if args.offline else 'live')+'.json',report)
    print('실습 04 결과:', path)
    print('보고서를 확인하고 reports/review.md에 원문 대조·실행 모드를 기록하세요.')

if __name__=='__main__':main()
