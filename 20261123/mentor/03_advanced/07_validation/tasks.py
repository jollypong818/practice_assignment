"""Day26 실습 7 · 심화. 실행 위치와 무관하게 현재 역할 폴더를 사용합니다."""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))

from coursekit.io import save_json, show_success
from coursekit.data import example_hit
from coursekit.checkpoints import (
    hits_to_documents, build_context, NO_ANSWER, RagServiceError, receive_bundle,
)
from coursekit.fixtures import fixture_bundle
from coursekit.reporting import execution_record


def common_cases():
    """의도적으로 만든 세 입력입니다. 실제 모델의 응답 로그가 아닙니다."""
    answered = {
        "status": "answered",
        "answer": "일반 기준으로 15분까지는 지각입니다. 사전 승인을 받았다면 운영실에 확인합니다.",
        "source_ids": [201], "missing_information": "",
    }
    insufficient = {
        "status": "insufficient_context", "answer": NO_ANSWER,
        "source_ids": [], "missing_information": "정확한 과제 마감 날짜가 자료에 없습니다.",
    }
    unknown = {**answered, "source_ids": [999]}
    return [
        {"name": "normal", "bundle": fixture_bundle(answered)},
        {"name": "insufficient", "bundle": fixture_bundle(insufficient)},
        {"name": "unknown_source", "bundle": fixture_bundle(unknown)},
    ]


def allowed_source_ids(included_docs):
    """입력: 실제 Context에 포함된 Document 목록 / 출력: set[int]."""
    # BEGIN D26-07-A01
    # 해설: 검색 후보 전체의 ID를 허용하면 Context 밖 문서를 인용할 수 있습니다.
    # build_context의 두 번째 반환값인 included_docs만 순회합니다.
    return {doc.metadata["citation_id"] for doc in included_docs}
    # END D26-07-A01


def inspect_case(case, provided_ids):
    """검증 결과를 JSON으로 기록합니다. 원문 의미의 참/거짓은 자동 판정하지 않습니다."""
    # BEGIN D26-07-A02
    # 해설: raw 완료 상태 → WireAnswer 파싱 → 로컬 Schema/업무 규칙 순서입니다.
    # 검증 거절은 결과표에 기록하되, 예상하지 못한 프로그래밍 오류는 감추지 않습니다.
    try:
        answer = receive_bundle(case["bundle"], provided_ids)
    except RagServiceError as exc:
        return {"case": case["name"], "outcome": "rejected", "error": str(exc),
                "result": None, "human_review_required": False}
    return {"case": case["name"], "outcome": "accepted", "error": None,
            "result": answer.model_dump(), "human_review_required": True}
    # END D26-07-A02


def type_and_duplicate_cases():
    """같은 답변의 ID 자료형과 중복 여부만 바꾸어 검사 지점을 비교합니다."""
    # BEGIN D26-07-A03
    # 해설: 문자열 ID는 strict WireAnswer 파싱에서 실패합니다.
    # 정수 중복은 Schema 파싱 후 validate_answer의 업무 규칙에서 실패합니다.
    data = {"status": "answered", "answer": "15분까지는 지각입니다.",
            "source_ids": [201], "missing_information": ""}
    return [
        {"name": "string_id", "bundle": fixture_bundle({**data, "source_ids": ["201"]})},
        {"name": "duplicate_id", "bundle": fixture_bundle({**data, "source_ids": [201, 201]})},
    ]
    # END D26-07-A03


def receipt_and_grounding_cases():
    """수신 미완료와 의미 오류를 서로 다른 사례로 만듭니다."""
    # BEGIN D26-07-A04
    # 해설: incomplete는 답변 근거 부족이 아니라 생성 완료 상태 오류입니다.
    # wrong_claim은 ID와 형식을 맞췄지만 15분 기준을 20분으로 바꾼 고정 반례입니다.
    # 이 문장을 검증기가 통과시켜도 원문이 답변을 지지한다는 뜻은 아닙니다.
    data = {"status": "answered", "answer": "15분까지는 지각입니다.",
            "source_ids": [201], "missing_information": ""}
    wrong = {**data, "answer": "사전 승인과 무관하게 20분까지는 지각입니다."}
    return [
        {"name": "incomplete", "bundle": fixture_bundle(data, status="incomplete")},
        {"name": "wrong_claim", "bundle": fixture_bundle(wrong)},
    ]
    # END D26-07-A04


def run():
    documents = hits_to_documents([example_hit()])
    context, included_docs = build_context(documents)
    provided_ids = allowed_source_ids(included_docs)
    cases = common_cases() + type_and_duplicate_cases() + receipt_and_grounding_cases()
    return {
        "source_mode": "validation_fixtures",
        "execution": execution_record("offline"),
        "context": context, "included_ids": sorted(provided_ids),
        "cases": [inspect_case(case, provided_ids) for case in cases],
        "grounding_review": "reports/review.md에서 숫자·조건·예외와 원문 위치를 직접 대조합니다.",
    }


def main():
    report = run()
    path = save_json(HERE, "validation_report.json", report)
    show_success("07 · 고정 입력 검증표 (모델·DB 미실행)", path)
    for row in report["cases"]:
        print(row["case"], row["outcome"], row["error"])
    print("accepted는 기계 검사를 통과했다는 뜻입니다. 원문 대조를 마쳐야 학습이 완료됩니다.")


if __name__ == "__main__":
    main()
