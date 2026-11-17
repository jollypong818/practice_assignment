"""Day21 실습 08: AI 지식 답변 생성기 v1. 실행: python main.py"""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))
from coursekit.io import DATA, read_json, write_json
from coursekit.prompting import make_bundle

# 기준: Day21 PPT 64~72장. 실제 모델 호출/실습 데이터 수정은 하지 않습니다.
# outputs는 실행 시 생성됩니다. 05/08의 모델 응답은 직접 수집한 원문만 등록합니다.
from coursekit.experiments import prepare_experiment, review_experiment, summarize, write_summary
from coursekit.retry import run_fixture_scenarios
from coursekit.io import check_name

def choose_bundle(bundle_path=None):
    # TODO D21-08-I01: 05에서 고정한 A/B 입력을 재사용하고 실행에 사용할 버전을 확인하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 05 outputs/dev_01/frozen_bundle.json을 선택적으로 지정. 원문을 바꾸지 않습니다.
    # 핵심: 마지막 프로젝트는 기존 흐름을 다시 연결합니다. 새 API·DB·벡터 검색을 만들지 않습니다.
    # BEGIN D21-08-I01
    if bundle_path is None:
        bundle = make_bundle()  # 앞 교시 미완성자를 위한 제공 체크포인트
        print("[독립 시작점] 실제 D 실험을 개선한 결과가 아닙니다.")
    else:
        bundle = {}  # TODO: read_json(bundle_path)
    # TODO: context_version, schema_version, A/B 버전의 존재를 확인
    # H 결과를 보고 이 파일을 덮어쓰지 마세요.
    raise NotImplementedError("D21-08-I01: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-08-I01
    return bundle

def choose_cases():
    # TODO D21-08-I02: 최종 확인용 H01~H03만 골라 세 질문의 A/B 계획을 만드세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: A/B 각 3질문, 첫 응답 총 6개. H03의 세 근거를 임의로 줄이지 않습니다.
    # BEGIN D21-08-I02
    cases = read_json(DATA/"holdout_v1.json")
    expected_ids = []  # TODO: H01, H02, H03
    # TODO: 세 질문과 선택 ID를 확인. expected_behavior를 Prompt에 넣지 않습니다.
    raise NotImplementedError("D21-08-I02: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-08-I02
    return cases

def make_report(rows):
    # TODO D21-08-I03: 검증과 사람 평가를 합치되 미실행·미평가 상태를 그대로 남기세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 정상·부족·형식 실패·참조 실패·사람 평가를 구분하고 B의 승리를 강요하지 않습니다.
    # BEGIN D21-08-I03
    report = summarize(rows)
    first = []  # TODO: attempt == 1만 선택
    report["project"] = {
        "name":"AI 지식 답변 생성기 v1", "first_target":len(first),
        "not_run":0,         # TODO: 미실행 수
        "human_pending":0,   # TODO: evidence_ok가 None인 수
        "max_attempt":0,     # TODO: 최대 attempt
        "completion":"실제 관찰과 근거 대조 필요",
    }
    # TODO: max_attempt <= 2 확인. 샘플 통과를 모델 우수성으로 적지 마세요.
    raise NotImplementedError("D21-08-I03: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-08-I03
    # TODO D21-08-I04: 첫 응답과 재시도 후 결과의 수를 분리하고 한 가지 개선안을 기록하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 개선안을 곧바로 같은 H의 독립 검증 성적이라고 주장하지 않습니다.
    # BEGIN D21-08-I04
    report["comparison"] = {"first_count":0,"retry_count":0,"next_improvement":"","holdout_policy":""}
    # TODO: 실제 개수와 이후 개선 규칙 작성. H 결과를 보고 현재 버전을 고치지 않습니다.
    raise NotImplementedError("D21-08-I04: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-08-I04
    return report

def choose_repeats():
    # TODO D21-08-I05: 가능하면 같은 조건의 최종 질문을 한 번 더 관찰하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 기본 6개와 반복 6개를 별도 슬롯으로 기록합니다.
    # BEGIN D21-08-I05
    repeats = 1  # TODO: 총 2회. 실제로 못한 항목은 not_run으로 보존
    raise NotImplementedError("D21-08-I05: 골격의 TODO를 채운 뒤 이 줄을 삭제하세요")
    # END D21-08-I05
    return repeats

def main():
    import argparse
    parser=argparse.ArgumentParser(description="모델 호출 없이 Prompt 준비 또는 실제 수동 응답 검토")
    parser.add_argument("command",choices=["prepare","review","fixtures"],nargs="?",default="prepare")
    parser.add_argument("--run",default="holdout_01",help="영문 실험 폴더명; 기존 실험 덮어쓰기 금지")
    parser.add_argument("--bundle",type=Path,help="05에서 고정한 frozen_bundle.json. 미지정 시 제공 독립 시작점 사용")
    args=parser.parse_args()
    check_name(args.run)
    folder=HERE/"outputs"/args.run
    if args.command=="prepare":
        bundle=choose_bundle(args.bundle)
        cases=choose_cases()
        repeats=choose_repeats()
        prepare_experiment(folder,bundle,cases,repeats=repeats)
        print("[준비]",folder)
        print("prompts의 원문을 각각 새 대화에 입력하세요. 아직 실제 응답은 0개입니다.")
    elif args.command=="review":
        rows=review_experiment(folder)
        report=make_report(rows)
        write_summary(folder,report)
        print("[검토]",folder/"summary.md")
        print("raw가 없는 항목은 미실행, 사람 평가 null은 미평가입니다.")
    else:
        results=run_fixture_scenarios(read_json(DATA/"validation_fixtures.json"))
        write_json(HERE/"outputs"/"fixture_checks.json",{"source_mode":"fixture","results":results})
        print("[샘플 검사] 호출 수 2·2·1·1. 모델의 실제 복구율이 아닙니다.")
