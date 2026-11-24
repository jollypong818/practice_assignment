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
    # TODO D27-04-B01: candidate_k와 context_k는 다른 제한값입니다.
    # 반환값과 예외 조건은 README.md의 수행 기준을 따르세요.
    raise NotImplementedError("D27-04-B01 미완성")
    # END D27-04-B01


def fetch_documents(retriever, payload):
    """Day26에서 배운 Runnable.invoke로 후보 Document를 받아옵니다."""
    # BEGIN D27-04-B02
    # TODO D27-04-B02: Day26에서 배운 Runnable.invoke로 후보 Document를 받아옵니다.
    # 반환값과 예외 조건은 README.md의 수행 기준을 따르세요.
    raise NotImplementedError("D27-04-B02 미완성")
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
