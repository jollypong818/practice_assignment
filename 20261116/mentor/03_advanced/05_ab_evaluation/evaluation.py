"""Day21 실습 05: 개선용 질문 A/B 비교. 실행: python main.py"""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))
from coursekit.io import DATA, read_json, write_json
from coursekit.prompting import BASE_RULE, ADDED_RULE, make_bundle

# 기준: Day21 PPT 37~45장. 실제 모델 호출/실습 데이터 수정은 하지 않습니다.
# outputs는 실행 시 생성됩니다. 05/08의 모델 응답은 직접 수집한 원문만 등록합니다.
from coursekit.experiments import prepare_experiment, review_experiment, summarize, write_summary
from coursekit.retry import run_fixture_scenarios
from coursekit.io import check_name

def choose_bundle(bundle_path=None):
    if bundle_path is not None:
        raise ValueError("05는 새 A/B를 설계합니다. --bundle은 08에서 사용하세요.")
    # 해설 D21-05-A01: A의 규칙을 유지하면서 B에 근거 부족 규칙 한 개만 추가하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 질문·문맥·계약·예제는 같고 B의 근거 규칙 1개만 다릅니다.
    # 핵심: 02의 예제 교체 실험과 05의 근거 규칙 실험을 한 비교로 섞지 않습니다.
    # BEGIN D21-05-A01
    rule_a=BASE_RULE
    rule_b=rule_a+"\n"+ADDED_RULE
    bundle=make_bundle(rule_a=rule_a,rule_b=rule_b,examples=[])
    # END D21-05-A01
    return bundle

def choose_cases():
    # 해설 D21-05-A02: 개선용 D01~D03 세 질문만 선택하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 기본필수 3질문 × A/B = 첫 응답 6개. 예상 행동을 Prompt에 넣지 않습니다.
    # BEGIN D21-05-A02
    cases=read_json(DATA/"dev_v1.json")
    assert [c["case_id"] for c in cases]==["D01","D02","D03"]
    # END D21-05-A02
    return cases

def make_report(rows):
    # 해설 D21-05-A03: 첫 응답만 골라 통과·미실행·미평가 개수를 기록하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 재시도 응답은 첫 응답 점수에 섞이지 않습니다. 실패를 분모에서 빼지 않습니다.
    # 핵심: None과 False는 다릅니다. 미평가를 0점으로 대체하지 않습니다.
    # BEGIN D21-05-A03
    first=[r for r in rows if r["attempt"]==1]
    counts={}
    for variant in ("A","B"):
        subset=[r for r in first if r["variant"]==variant]
        counts[variant]={"N":len(subset),"json_passed":sum(r["json_ok"] is True for r in subset),
                         "not_run":sum(r["execution_state"]=="not_run" for r in subset),
                         "human_pending":sum(r["evidence_ok"] is None for r in subset)}
    report=summarize(rows)
    report["learner_first_counts"]=counts
    # END D21-05-A03
    # 해설 D21-05-A04: source_mode별 결과를 분리하고 fixture 지표를 실모델 품질로 해석하지 마세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: manual_chat·fixture를 섞어 하나의 실제 성능 수치로 발표하지 않습니다.
    # BEGIN D21-05-A04
    modes=sorted({r["source_mode"] for r in rows})
    report["source_modes"]=modes
    report["model_claim_allowed"]=modes==["manual_chat"] and all(r["execution_state"]!="not_run" for r in first)
    report["conclusion"]="실제 관찰·사람 평가를 읽고 작성합니다. 자동 승자는 없습니다."
    # END D21-05-A04
    # 해설 D21-05-A05: 같은 질문·반복의 A/B 문맥 해시가 같은지 대조하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 비교 중 문맥 내용·순서가 달라졌으면 중단합니다.
    # BEGIN D21-05-A05
    pairs={}
    for row in first:
        key=(row["source_mode"],row["case_id"],row["repeat"])
        pairs.setdefault(key,{})[row["variant"]]=row["context_sha256"]
    assert all(set(pair)=={"A","B"} and pair["A"]==pair["B"] for pair in pairs.values())
    report["paired_contexts_checked"]=len(pairs)
    # END D21-05-A05
    return report

def choose_repeats():
    # 해설 D21-05-A06: 같은 조건을 한 번 더 관찰하도록 반복 수를 설정하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 총 첫 응답 슬롯 3×2×2=12개. 시간 부족은 미실행으로 남깁니다.
    # BEGIN D21-05-A06
    repeats=2
    # END D21-05-A06
    return repeats

def validate_frozen_design(bundle):
    # 해설 D21-05-A07: 버전 정보·가설·변경점이 비어 있지 않은지 확인하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: README의 예상 결과와 출력 파일을 대조합니다.
    # BEGIN D21-05-A07
    assert bundle["context_version"]=="knowledge_v1"
    assert bundle["schema_version"]=="answer_schema_v1"
    assert bundle["changed"].strip() and bundle["hypothesis"].strip()
    assert bundle["variants"]["A"]["prompt_version"]!=bundle["variants"]["B"]["prompt_version"]
    # END D21-05-A07
    return True

def main():
    import argparse
    parser=argparse.ArgumentParser(description="모델 호출 없이 Prompt 준비 또는 실제 수동 응답 검토")
    parser.add_argument("command",choices=["prepare","review","fixtures"],nargs="?",default="prepare")
    parser.add_argument("--run",default="dev_01",help="영문 실험 폴더명; 기존 실험 덮어쓰기 금지")
    parser.add_argument("--bundle",type=Path,help="05에서 고정한 frozen_bundle.json. 미지정 시 제공 독립 시작점 사용")
    args=parser.parse_args()
    check_name(args.run)
    folder=HERE/"outputs"/args.run
    if args.command=="prepare":
        bundle=choose_bundle(args.bundle)
        validate_frozen_design(bundle)
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
