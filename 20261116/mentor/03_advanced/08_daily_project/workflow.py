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
    # 해설 D21-08-A01: 05에서 고정한 A/B 입력을 재사용하고 실행에 사용할 버전을 확인하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 05 outputs/dev_01/frozen_bundle.json을 선택적으로 지정. 원문을 바꾸지 않습니다.
    # 핵심: 마지막 프로젝트는 기존 흐름을 다시 연결합니다. 새 API·DB·벡터 검색을 만들지 않습니다.
    # BEGIN D21-08-A01
    if bundle_path is None:
        bundle=make_bundle()
        print("[독립 시작점] 제공 A/B를 사용합니다. D에서 개선한 결과라고 주장하지 않습니다.")
    else:
        bundle=read_json(bundle_path)
    if bundle["context_version"]!="knowledge_v1" or bundle["schema_version"]!="answer_schema_v1":
        raise ValueError("수업의 문맥·출력 계약 버전을 확인하세요")
    assert set(bundle["variants"])=={"A","B"}
    # END D21-08-A01
    # 해설 D21-08-A02: 로드한 출력 계약이 현재 검증 모델과 일치하는지 확인하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 계약이 바뀌면 같은 버전으로 비교하지 않습니다.
    # BEGIN D21-08-A02
    from coursekit.contracts import KnowledgeAnswer
    if bundle["schema"]!=KnowledgeAnswer.model_json_schema():
        raise ValueError("Prompt와 로컬 검사기의 Schema가 다릅니다")
    assert bundle["variants"]["A"]["evidence_rule"]!=bundle["variants"]["B"]["evidence_rule"]
    # END D21-08-A02
    return bundle

def choose_cases():
    # 해설 D21-08-A03: 최종 확인용 H01~H03만 골라 세 질문의 A/B 계획을 만드세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: A/B 각 3질문, 첫 응답 총 6개. H03의 세 근거를 임의로 줄이지 않습니다.
    # BEGIN D21-08-A03
    cases=read_json(DATA/"holdout_v1.json")
    assert [c["case_id"] for c in cases]==["H01","H02","H03"]
    assert cases[0]["selected_ids"]==[103]
    assert cases[1]["selected_ids"]==[102]
    assert cases[2]["selected_ids"]==[101,102,103]
    # END D21-08-A03
    return cases

def make_report(rows):
    # 해설 D21-08-A04: 검증과 사람 평가를 합치되 미실행·미평가 상태를 그대로 남기세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 정상·부족·형식 실패·참조 실패·사람 평가를 구분하고 B의 승리를 강요하지 않습니다.
    # BEGIN D21-08-A04
    report=summarize(rows)
    first=[r for r in rows if r["attempt"]==1]
    report["project"]={"name":"AI 지식 답변 생성기 v1","first_target":len(first),
        "not_run":sum(r["execution_state"]=="not_run" for r in first),
        "human_pending":sum(r.get("evidence_ok") is None for r in first),
        "max_attempt":max((r["attempt"] for r in rows),default=0),
        "completion":"실제 관찰·근거 대조 결과를 확인하세요. 자동 만점/승자 없음"}
    assert report["project"]["max_attempt"]<=2
    # END D21-08-A04
    # 해설 D21-08-A05: 첫 응답과 재시도 후 결과의 수를 분리하고 한 가지 개선안을 기록하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 개선안을 곧바로 같은 H의 독립 검증 성적이라고 주장하지 않습니다.
    # BEGIN D21-08-A05
    report["comparison"]={"first_count":len(first),"retry_count":sum(r["attempt"]==2 for r in rows),
        "next_improvement":"관찰한 실패를 읽고 지시·예제·문맥 중 하나만 고릅니다.",
        "holdout_policy":"H를 본 뒤 수정하면 새 버전·새 확인 질문 세트가 필요합니다."}
    # END D21-08-A05
    # 해설 D21-08-A06: 출처 유형과 평가 대기 수를 공개하고 실측이 없으면 결론을 보류하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: README의 예상 결과와 출력 파일을 대조합니다.
    # BEGIN D21-08-A06
    modes=sorted({r["source_mode"] for r in rows})
    report["provenance"]={"modes":modes,"manual_runs":sum(r["source_mode"]=="manual_chat" and r["execution_state"]!="not_run" for r in first),
                          "fixture_rows":sum(r["source_mode"]=="fixture" for r in rows),
                          "decision":"사람이 질문·주장·출처를 대조한 뒤 판단. 프로그램은 우열을 결정하지 않습니다."}
    # END D21-08-A06
    return report

def choose_repeats():
    # 해설 D21-08-A07: 가능하면 같은 조건의 최종 질문을 한 번 더 관찰하세요.
    # 입력·대상: 아래 함수 인자와 제공 데이터만 사용합니다.
    # 완료 기준: 기본 6개와 반복 6개를 별도 슬롯으로 기록합니다.
    # BEGIN D21-08-A07
    repeats=2
    # END D21-08-A07
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
