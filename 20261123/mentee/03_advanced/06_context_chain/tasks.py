"""실습 06 · Context·출처를 보관하고 Runnable Chain을 실행합니다."""
from pathlib import Path
import argparse
import sys

HERE = Path(__file__).resolve().parent
# 어느 폴더에서 실행해도 이 역할 폴더의 coursekit을 사용합니다.
sys.path.insert(0, str(HERE.parents[1]))

from coursekit.data import load_hits
from coursekit.checkpoints import hits_to_documents, build_context, make_prompt, WireAnswer
from coursekit.llm import create_chat_model
from coursekit.fixtures import fixture_generation
from coursekit.reporting import execution_record, bundle_record
from coursekit.io import save_json, show_success


def prepare_context(documents, question: str, max_items=2, max_chars=600) -> dict:
    """Document 목록 → Context·포함 문서·포함 ID·Prompt 입력. 원문은 바꾸지 않습니다."""
    # BEGIN D26-06-A01
    # TODO D26-06-A01: build_context로 Context와 포함 문서를 얻고, 포함 ID 및 Prompt 입력을 함께 반환합니다.
    # 힌트: 반환 Key는 context, included_docs, provided_ids, inputs입니다. ID는 included_docs에서만 모읍니다.
    # 완료 후 아래 NotImplementedError를 제거하고 반환값을 확인하세요.
    raise NotImplementedError("D26-06-A01 TODO 미완성")
    # END D26-06-A01


def run_generation(prompt, structured_model, inputs: dict):
    """Prompt → Structured Model의 bundle. bundle 검증·승인은 다음 실습입니다."""
    # BEGIN D26-06-A02
    # TODO D26-06-A02: 빈 Context에서는 None을 반환하고, 나머지는 Prompt와 Structured Model을 연결하여 bundle을 받습니다.
    # 힌트: 빈 문자열을 먼저 확인하여 모델 호출 전에 반환합니다. 정상 Context에서는 |와 invoke를 사용합니다.
    # 완료 후 아래 NotImplementedError를 제거하고 반환값을 확인하세요.
    raise NotImplementedError("D26-06-A02 TODO 미완성")
    # END D26-06-A02


def compare_contexts(documents) -> dict:
    """같은 목록에서 중복과 선택 개수를 각각 바꿉니다. LLM 호출은 없습니다."""
    # BEGIN D26-06-A03
    # TODO D26-06-A03: 기본·중복 청크 추가·max_items=1 조건을 각각 실행하여 포함 ID를 비교합니다.
    # 힌트: 세 조건에서 한 가지 설정만 바꿉니다. 모델은 호출하지 않고 build_context 결과만 비교합니다.
    # 완료 후 아래 NotImplementedError를 제거하고 반환값을 확인하세요.
    raise NotImplementedError("D26-06-A03 TODO 미완성")
    # END D26-06-A03


def inspect_boundary(document) -> dict:
    """문자 상한의 직전·정확한 경계 비교. Token 개수를 계산하는 함수가 아닙니다."""
    # BEGIN D26-06-A04
    # TODO D26-06-A04: 첫 Document 블록 길이보다 1자 작은 상한과 정확한 길이의 상한에서 포함 여부를 비교합니다.
    # 힌트: ID·위치·줄바꿈·본문을 포함한 블록 전체 길이를 계산합니다. 본문을 슬라이스로 자르지 않습니다.
    # 완료 후 아래 NotImplementedError를 제거하고 반환값을 확인하세요.
    raise NotImplementedError("D26-06-A04 TODO 미완성")
    # END D26-06-A04


def main():
    parser = argparse.ArgumentParser(description="Context → Prompt → Structured Model 관찰")
    parser.add_argument("--offline", action="store_true", help="고정 bundle 예시만 사용; 실제 모델 미실행")
    args = parser.parse_args()
    # 앞 실습의 미완성 코드에 의존하지 않는 제공된 Document 변환 Checkpoint입니다.
    academic_hits = [hit for hit in load_hits() if hit["category"] == "학사"]
    documents = hits_to_documents(academic_hits)
    question = "15분 늦으면 어떻게 기록되나요?"
    prepared = prepare_context(documents, question)
    experiments = {}
    experiments["context_comparison"] = compare_contexts(documents)
    experiments["length_boundary"] = inspect_boundary(documents[0])
    prompt = make_prompt()
    if args.offline:
        # 이 Runnable은 제공된 고정 bundle을 반환합니다. 실제 모델 실행은 아닙니다.
        structured_model = fixture_generation()
    else:
        # 라이브 모델 설정과 Schema를 준비하는 단계입니다. 아직 API를 호출하지 않습니다.
        chat_model = create_chat_model()
        structured_model = chat_model.with_structured_output(
            WireAnswer, method="json_schema", strict=True, include_raw=True)
    bundle = run_generation(prompt, structured_model, prepared["inputs"])
    # 빈 Context 확인은 실패해야 하는 로컬 Spy로 검사합니다. 유료 모델을 다시 호출하지 않습니다.
    from langchain_core.runnables import RunnableLambda
    def forbidden_call(_):
        raise AssertionError("빈 Context에서 모델을 호출했습니다.")
    skipped = run_generation(prompt, RunnableLambda(forbidden_call),
                             {"question": question, "context": ""})
    experiments["empty_context"] = {"generation_skipped": skipped is None, "llm_calls": 0}
    if bundle is None:
        raise AssertionError("이번 정상 예시의 Context는 비어 있지 않아야 합니다.")
    parsed = bundle.get("parsed")
    cited_ids = list(parsed.source_ids) if parsed is not None else []
    result = {
        "exercise": "06_context_chain",
        "execution": execution_record("offline_fixture" if args.offline else "live", llm=not args.offline),
        "real_model_calls": 0 if args.offline else 1,
        "context": prepared["context"],
        "included_ids": prepared["provided_ids"],
        "included_sources": [dict(doc.metadata) for doc in prepared["included_docs"]],
        "prompt_input": prepared["inputs"],
        "bundle": bundle_record(bundle),
        "observed_source_ids": cited_ids,
        "source_id_membership_only": None if parsed is None else set(cited_ids).issubset(prepared["provided_ids"]),
        "experiments": experiments,
        "human_evidence_review": "pending",
        "review_note": "bundle·포함 ID를 관찰한 기록입니다. 자료형·상태·출처의 승인 검사는 실습07에서 진행합니다.",
    }
    path = save_json(HERE, "context_chain.json", result)
    show_success("06 Context·Runnable 관찰 기록", path)
    print("실제 LLM 실행:", not args.offline, "| 검증 승인 전 bundle 관찰")


if __name__ == "__main__":
    main()
