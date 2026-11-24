"""Day27 강의 실습. 실행은 역할 폴더에서 Python으로 실행합니다."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
ROLE_ROOT=next(p for p in HERE.parents if (p/'coursekit').is_dir())
sys.path.insert(0,str(ROLE_ROOT))


import argparse

from coursekit.workshops import STAGE_RUNNERS

from coursekit.io import save_report



def create_pairs(question, docs):
    """CrossEncoder 입력은 [질문, 문서본문]의 쌍 목록입니다."""
    # BEGIN D27-05-B01
    # ANSWER D27-05-B01: CrossEncoder 입력은 [질문, 문서본문]의 쌍 목록입니다.
    # 1. 입력: question, docs (필요한 값만 받습니다.)
    # 2. 절차: CrossEncoder 입력은 [질문, 문서본문]의 쌍 목록입니다.
    # 3. 반환: 호출한 Stage가 사용할 값/상태를 반환합니다.
    # 4. 주의: 오류를 빈 결과로 숨기지 않고 출처·필터 계약을 유지합니다.
    return [(question,d.page_content) for d in docs]
    # END D27-05-B01


def rank_documents(question, docs, scorer):
    """Reranker는 후보를 새로 찾지 않고 동일 후보를 순위 변경합니다."""
    # BEGIN D27-05-B02
    # ANSWER D27-05-B02: Reranker는 후보를 새로 찾지 않고 동일 후보를 순위 변경합니다.
    # 1. 입력: question, docs, scorer (필요한 값만 받습니다.)
    # 2. 절차: Reranker는 후보를 새로 찾지 않고 동일 후보를 순위 변경합니다.
    # 3. 반환: 호출한 Stage가 사용할 값/상태를 반환합니다.
    # 4. 주의: 오류를 빈 결과로 숨기지 않고 출처·필터 계약을 유지합니다.
    from coursekit.reranking import rerank_documents
    return rerank_documents(question,docs,scorer,top_n=3)
    # END D27-05-B02


def main():
    parser=argparse.ArgumentParser(description='Day27 실습 05 · 05_cross_encoder_reranking')
    parser.add_argument('--offline',action='store_true',help='교육용 고정 데이터·점수. 모델 품질 실측이 아닙니다.')
    args=parser.parse_args()
    # Day27: 일부 진단 실습 외에는 기본 실행이 실제 모델·DB·LLM 경로입니다.
    report=STAGE_RUNNERS[5](args.offline,[create_pairs,rank_documents])
    path=save_report(HERE,'day27_05_'+('fixture' if args.offline else 'live')+'.json',report)
    print('실습 05 결과:', path)
    print('보고서를 확인하고 reports/review.md에 원문 대조·실행 모드를 기록하세요.')

if __name__=='__main__':main()
