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
    # TODO D26-07-A01: included_docs의 metadata에서 citation_id를 모아 set으로 반환합니다.
    # 힌트: Document 목록을 순회하고 doc.metadata["citation_id"]를 읽으세요. 검색 후보 목록은 사용하지 않습니다.
    # 아래 NotImplementedError를 지우고 이 블록을 완성하세요.
    raise NotImplementedError("D26-07-A01 TODO 미완성")
    # END D26-07-A01


def inspect_case(case, provided_ids):
    """검증 결과를 JSON으로 기록합니다. 원문 의미의 참/거짓은 자동 판정하지 않습니다."""
    # BEGIN D26-07-A02
    # TODO D26-07-A02: receive_bundle로 검사한 결과를 accepted/rejected 형식으로 기록합니다.
    # 힌트: 성공 시 KnowledgeAnswer.model_dump(), RagServiceError 시 str(exc)를 사용합니다. 반환 Key는 docstring 아래 호출부와 expected를 확인하세요.
    # 아래 NotImplementedError를 지우고 이 블록을 완성하세요.
    raise NotImplementedError("D26-07-A02 TODO 미완성")
    # END D26-07-A02


def type_and_duplicate_cases():
    """같은 답변의 ID 자료형과 중복 여부만 바꾸어 검사 지점을 비교합니다."""
    # BEGIN D26-07-A03
    # TODO D26-07-A03: 정상 입력에서 ID만 문자열 또는 중복 정수로 바꾼 두 fixture_bundle 사례를 반환합니다.
    # 힌트: case 이름은 string_id와 duplicate_id입니다. 다른 네 필드는 정상 예시와 같게 유지하세요.
    # 아래 NotImplementedError를 지우고 이 블록을 완성하세요.
    raise NotImplementedError("D26-07-A03 TODO 미완성")
    # END D26-07-A03


def receipt_and_grounding_cases():
    """수신 미완료와 의미 오류를 서로 다른 사례로 만듭니다."""
    # BEGIN D26-07-A04
    # TODO D26-07-A04: incomplete 완료 상태 사례와 올바른 ID의 잘못된 주장 사례를 반환합니다.
    # 힌트: case 이름은 incomplete와 wrong_claim입니다. 후자는 20분까지 지각이라고 주장하도록 하되 ID는 201입니다.
    # 아래 NotImplementedError를 지우고 이 블록을 완성하세요.
    raise NotImplementedError("D26-07-A04 TODO 미완성")
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
