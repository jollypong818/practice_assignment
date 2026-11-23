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
    # 검색 후보 전체와 최종 Context에 포함한 문서는 다를 수 있습니다.
    # 제공 함수는 중복 chunk_id를 제외하고 문자 상한에 맞는 전체 블록만 넣습니다.
    context, included_docs = build_context(documents, max_items=max_items, max_chars=max_chars)
    # 허용 출처의 후보는 실제 포함한 문서에서만 얻습니다. 원래 후보 전체를 쓰지 않습니다.
    provided_ids = [doc.metadata["citation_id"] for doc in included_docs]
    # Prompt에는 문자열만 전달하고, 출처를 연결할 Document 객체는 별도로 보관합니다.
    return {"context": context, "included_docs": included_docs,
            "provided_ids": provided_ids,
            "inputs": {"question": question, "context": context}}
    # END D26-06-A01


def run_generation(prompt, structured_model, inputs: dict):
    """Prompt → Structured Model의 bundle. bundle 검증·승인은 다음 실습입니다."""
    # BEGIN D26-06-A02
    # 근거가 전혀 없다면 모델을 호출해 빈 자료에서 답을 만들게 하지 않습니다.
    # None은 이 함수가 생성을 생략했다는 표시입니다. 모델이 만든 답변이 아닙니다.
    if not inputs["context"].strip():
        return None
    # |는 첫 Runnable의 반환값을 다음 Runnable에 연결합니다.
    # 첫 단계는 ChatPromptValue를 만들고 둘째 단계는 raw/parsed/parsing_error를 반환합니다.
    generation = prompt | structured_model
    # 두 호출을 순서대로 실행합니다. 라이브 경로에서 LLM API 요청은 여기서 일어납니다.
    return generation.invoke(inputs)
    # END D26-06-A02


def compare_contexts(documents) -> dict:
    """같은 목록에서 중복과 선택 개수를 각각 바꿉니다. LLM 호출은 없습니다."""
    # BEGIN D26-06-A03
    # 원래 목록은 그대로 두고 첫 청크를 한 번 더 넣은 새 목록을 만듭니다.
    with_duplicate = [documents[0], documents[0], *documents[1:]] if documents else []
    # 문자 상한은 세 번 모두 같게 유지합니다. 중복과 개수의 효과를 분리해 봅니다.
    _, baseline = build_context(documents, max_items=2, max_chars=600)
    _, duplicated = build_context(with_duplicate, max_items=2, max_chars=600)
    _, one_document = build_context(documents, max_items=1, max_chars=600)
    # 전체 본문 대신 포함 ID를 나란히 기록하여 어떤 문서가 선택되었는지 확인합니다.
    return {
        "baseline_ids": [doc.metadata["citation_id"] for doc in baseline],
        "duplicate_ids": [doc.metadata["citation_id"] for doc in duplicated],
        "one_document_ids": [doc.metadata["citation_id"] for doc in one_document],
        "llm_calls": 0,
    }
    # END D26-06-A03


def inspect_boundary(document) -> dict:
    """문자 상한의 직전·정확한 경계 비교. Token 개수를 계산하는 함수가 아닙니다."""
    # BEGIN D26-06-A04
    # 실제 Context 블록의 ID, 원문 위치, 줄바꿈, 본문을 모두 길이에 포함합니다.
    meta = document.metadata
    block_text = f'[{meta["citation_id"]}] {meta["source_locator"]}\n{document.page_content}'
    size = len(block_text)
    # 한 블록이므로 블록 사이의 구분 문자열은 아직 없습니다.
    before_context, before_docs = build_context([document], max_items=1, max_chars=size - 1)
    exact_context, exact_docs = build_context([document], max_items=1, max_chars=size)
    # 상한 미만이면 일부 문장이 아니라 블록 전체가 제외되어야 합니다.
    return {"block_chars": size, "before_limit": size - 1, "exact_limit": size,
            "before_context": before_context,
            "before_ids": [doc.metadata["citation_id"] for doc in before_docs],
            "exact_context": exact_context,
            "exact_ids": [doc.metadata["citation_id"] for doc in exact_docs],
            "llm_calls": 0}
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
