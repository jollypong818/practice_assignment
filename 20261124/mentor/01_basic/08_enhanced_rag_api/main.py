"""Day27 강의 실습. 실행은 역할 폴더에서 Python으로 실행합니다."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
ROLE_ROOT=next(p for p in HERE.parents if (p/'coursekit').is_dir())
sys.path.insert(0,str(ROLE_ROOT))


import argparse

from coursekit.workshops import STAGE_RUNNERS

from coursekit.io import save_report



def make_service_chain(offline):
    """Rewrite → Retrieve → Rerank → Context → Generation·Validation을 연결합니다."""
    # BEGIN D27-08-B01
    # ANSWER D27-08-B01: Rewrite → Retrieve → Rerank → Context → Generation·Validation을 연결합니다.
    # 1. 입력: offline (필요한 값만 받습니다.)
    # 2. 절차: Rewrite → Retrieve → Rerank → Context → Generation·Validation을 연결합니다.
    # 3. 반환: 호출한 Stage가 사용할 값/상태를 반환합니다.
    # 4. 주의: 오류를 빈 결과로 숨기지 않고 출처·필터 계약을 유지합니다.
    from coursekit.runtime import create_demo_chain
    return create_demo_chain(offline=offline)
    # END D27-08-B01


def wire_fastapi(chain):
    """API 요청의 role 문자열을 신뢰하지 않고 서버에서 learner 역할을 지정합니다."""
    # BEGIN D27-08-B02
    # ANSWER D27-08-B02: API 요청의 role 문자열을 신뢰하지 않고 서버에서 learner 역할을 지정합니다.
    # 1. 입력: chain (필요한 값만 받습니다.)
    # 2. 절차: API 요청의 role 문자열을 신뢰하지 않고 서버에서 learner 역할을 지정합니다.
    # 3. 반환: 호출한 Stage가 사용할 값/상태를 반환합니다.
    # 4. 주의: 오류를 빈 결과로 숨기지 않고 출처·필터 계약을 유지합니다.
    from coursekit.api import create_app
    return create_app(chain,trusted_role='learner')
    # END D27-08-B02


def main():
    parser=argparse.ArgumentParser(description='Day27 실습 08 · 08_enhanced_rag_api')
    parser.add_argument('--offline',action='store_true',help='교육용 고정 데이터·점수. 모델 품질 실측이 아닙니다.')
    args=parser.parse_args()
    # Day27: 일부 진단 실습 외에는 기본 실행이 실제 모델·DB·LLM 경로입니다.
    report=STAGE_RUNNERS[8](args.offline,[make_service_chain,wire_fastapi])
    path=save_report(HERE,'day27_08_'+('fixture' if args.offline else 'live')+'.json',report)
    print('실습 08 결과:', path)
    print('보고서를 확인하고 reports/review.md에 원문 대조·실행 모드를 기록하세요.')

if __name__=='__main__':main()
