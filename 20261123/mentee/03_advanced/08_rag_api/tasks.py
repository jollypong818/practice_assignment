"""Day26 실습 8 · 심화. 실행 위치와 무관하게 현재 역할 폴더를 사용합니다."""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))

import argparse
from fastapi.testclient import TestClient
from langchain_core.runnables import RunnableLambda
from coursekit.io import save_json, show_success
from coursekit.checkpoints import (
    make_retriever, build_context, make_rag_service, create_app,
)
from coursekit.fixtures import fixture_retriever, fixture_generation
from coursekit.reporting import execution_record

MAX_CHARS = 600
NORMAL_QUERY = "15분 늦으면 어떻게 기록되나요?"
MISSING_QUERY = "내 과제의 정확한 마감 날짜는?"


def wire_app(retriever, generation):
    """Runnable 두 개를 서비스 함수와 FastAPI 앱으로 연결합니다."""
    # BEGIN D26-08-A01
    # TODO D26-08-A01: retriever와 generation을 make_rag_service에 연결한 뒤 create_app의 결과를 반환합니다.
    # 힌트: max_chars에는 MAX_CHARS를 사용합니다. 서비스를 호출한 결과가 아니라 서비스 함수 자체를 create_app에 넘깁니다.
    # 아래 NotImplementedError를 지우고 이 블록을 완성하세요.
    raise NotImplementedError("D26-08-A01 TODO 미완성")
    # END D26-08-A01


def make_request(query, category, candidate_k=3, context_k=2):
    """POST /rag/answer에 보낼 JSON용 dict. 두 k는 각각 상한입니다."""
    # BEGIN D26-08-A02
    # TODO D26-08-A02: query/category/candidate_k/context_k를 같은 이름의 네 Key로 묶어 반환합니다.
    # 힌트: 별도의 ID나 기본 답변을 추가하지 않습니다. 입력의 두 k를 서로 바꾸지 마세요.
    # 아래 NotImplementedError를 지우고 이 블록을 완성하세요.
    raise NotImplementedError("D26-08-A02 TODO 미완성")
    # END D26-08-A02


def comparison_request(original):
    """같은 질문·category·candidate_k에서 context_k만 2→1로 바꿉니다."""
    # BEGIN D26-08-A03
    # TODO D26-08-A03: 원본 요청을 복사하고 context_k만 1로 바꾼 요청을 반환합니다.
    # 힌트: dict(original)은 얕은 복사본을 만듭니다. 이번 요청 값은 모두 문자열/정수입니다.
    # 아래 NotImplementedError를 지우고 이 블록을 완성하세요.
    raise NotImplementedError("D26-08-A03 TODO 미완성")
    # END D26-08-A03


def failure_examples():
    """항상 Fixture로 검사합니다. 실제 API Timeout이나 DB 장애를 유발하지 않습니다."""
    # BEGIN D26-08-A04
    # TODO D26-08-A04: 빈 검색 결과와 Timeout을 각각 run_fixed_failure로 실행한 두 결과를 반환합니다.
    # 힌트: 빈 검색은 RunnableLambda(lambda request: [])이고, Timeout에는 fixture_generation("timeout")을 사용합니다. 모든 사례는 Fixture입니다.
    # 아래 NotImplementedError를 지우고 이 블록을 완성하세요.
    raise NotImplementedError("D26-08-A04 TODO 미완성")
    # END D26-08-A04


# 아래는 실행·관찰을 위한 제공 코드입니다. 먼저 위쪽 TODO 함수만 완성합니다.
# 구조가 궁금할 때 prepare_components → run_smoke 순서로 읽습니다.
def prepare_components(offline):
    """라이브 경로는 환경 검사를 통과한 뒤 실제 E5와 DB 검색을 준비합니다."""
    if offline:
        return fixture_retriever(), fixture_generation()
    # 여기까지는 기본 import만 수행하므로 파일을 읽는 것만으로 연결되지 않습니다.
    from coursekit.llm import create_generation
    from coursekit.live import load_encoder, make_search_hits
    generation = create_generation()
    encoder = load_encoder()
    retriever = make_retriever(make_search_hits(model=encoder))
    return retriever, generation


def trace_components(retriever, generation, trace):
    """한 번에 한 요청만 보내는 smoke 관찰용. --serve에서는 사용하지 않습니다."""
    def retrieve(request):
        trace["retrieval_attempts"] += 1
        docs = retriever.invoke(request)
        trace["documents"] = docs
        trace["retrieval_completed"] = True
        return docs

    def generate(prompt_input):
        trace["generation_attempts"] += 1
        bundle = generation.invoke(prompt_input)
        trace["generation_completed"] = True
        return bundle

    return RunnableLambda(retrieve), RunnableLambda(generate)


def new_trace():
    return {"retrieval_attempts": 0, "generation_attempts": 0,
            "retrieval_completed": False, "generation_completed": False,
            "documents": []}


def observe_response(name, payload, response, trace, offline):
    """검색 후보·실제 Context 포함 문서·응답 출처의 세 경계를 기록합니다."""
    docs = trace["documents"]
    # 422이면 서비스가 실행되지 않았으므로 Context 구성도 생략합니다.
    included = []
    observation_error = None
    if trace["retrieval_completed"]:
        try:
            _, included = build_context(docs, max_items=payload["context_k"],
                                        max_chars=MAX_CHARS)
        except (KeyError, TypeError, ValueError):
            # 서비스의 502 결과를 관찰 코드의 오류로 덮어쓰지 않습니다.
            observation_error = "context_observation_failed"
    body = response.json()
    included_ids = [doc.metadata["citation_id"] for doc in included]
    source_ids = [source["citation_id"] for source in body.get("sources", [])]
    answer_ids = body.get("result", {}).get("source_ids", [])
    source_check = (source_ids == answer_ids and set(source_ids).issubset(included_ids))
    return {
        "case": name, "request": payload, "http_status": response.status_code,
        "response": body,
        "candidate_ids": [doc.metadata.get("citation_id") for doc in docs],
        "observation_error": observation_error,
        "included_ids": included_ids, "response_source_ids": source_ids,
        "source_mapping_consistent": source_check if response.status_code == 200 else None,
        "retrieval_attempts": trace["retrieval_attempts"],
        "generation_attempts": trace["generation_attempts"],
        "execution": execution_record(
            "offline" if offline else "live",
            db=not offline and trace["retrieval_completed"],
            embedding=not offline and trace["retrieval_completed"],
            llm=not offline and trace["generation_completed"],
        ),
    }


def run_fixed_failure(name, retriever, generation):
    """실제 실행 범위는 FastAPI 경로와 Fixture입니다. 외부 서비스 실측이 아닙니다."""
    # Fixture 호출 횟수만 셉니다. 실제 모델 사용량이 아닙니다.
    trace = new_trace()
    observed = trace_components(retriever, generation, trace)
    app = wire_app(*observed)
    payload = make_request(NORMAL_QUERY, "학사")
    with TestClient(app) as client:
        response = client.post("/rag/answer", json=payload)
    row = observe_response(name, payload, response, trace, offline=True)
    row["source_mode"] = "fixed_failure_example"
    return row


def common_failure_examples():
    return [run_fixed_failure("timeout", fixture_retriever(),
                              fixture_generation("timeout"))]


def run_smoke(offline=False, compare_k=False):
    # 요청 TODO를 먼저 확인합니다. 미완성 상태에서 외부 연결을 준비하지 않습니다.
    normal = make_request(NORMAL_QUERY, "학사")
    # 앱을 조립하는 것만으로 모델을 호출하지 않습니다. wiring TODO도 먼저 확인합니다.
    wire_app(fixture_retriever(), fixture_generation())
    retriever, generation = prepare_components(offline)
    trace = new_trace()
    app = wire_app(*trace_components(retriever, generation, trace))
    cases = [
        ("normal", normal, 200, "answered"),
        ("missing_date", make_request(MISSING_QUERY, "학사"), 200, "insufficient_context"),
        ("invalid_request", {**normal, "candidate_k": 0}, 422, None),
    ]
    if compare_k:
        cases.append(("context_k_1", comparison_request(normal), 200, "answered"))
    rows = []
    checks = []
    with TestClient(app) as client:
        for name, payload, expected_http, expected_status in cases:
            trace.clear()
            trace.update(new_trace())
            response = client.post("/rag/answer", json=payload)
            row = observe_response(name, payload, response, trace, offline)
            rows.append(row)
            checks.append({
                "case": name,
                "http_matches": response.status_code == expected_http,
                "status_matches": (expected_status is None or
                    row["response"].get("result", {}).get("status") == expected_status),
                "sources_match": row["source_mapping_consistent"] is not False,
            })
    return {
        "source_mode": "fixture_api_smoke" if offline else "live_api_smoke",
        "api_transport": "FastAPI TestClient (in-process; TCP server not started)",
        "api_cases": rows,
        "fixed_failure_examples": failure_examples(),
        "checks": checks,
        "checks_passed": all(all(value for key, value in check.items() if key != "case")
                             for check in checks),
        "human_review_required": True,
        "note": "검사 통과 후에도 reports/review.md에서 원문·숫자·예외를 대조합니다.",
    }


def main():
    parser = argparse.ArgumentParser(description="실습08 RAG API: 기본은 실제 DB·E5·LLM")
    parser.add_argument("--offline", action="store_true", help="외부 호출 없이 고정 Fixture 사용")
    parser.add_argument("--serve", action="store_true", help="사용자 PC에서 실제 RAG HTTP 서버 실행")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--compare-k", action="store_true", help="동일 질문의 k 비교 요청 1회 추가")
    args = parser.parse_args()
    if args.serve and args.offline:
        parser.error("--serve는 실제 연동용입니다. 고정 예시는 --offline으로 확인하세요.")
    if not 1 <= args.port <= 65535:
        parser.error("port는 1~65535 정수입니다.")
    if args.serve:
        import uvicorn
        retriever, generation = prepare_components(False)
        # 서버 요청끼리는 smoke용 trace dict를 공유하지 않습니다.
        app = wire_app(retriever, generation)
        uvicorn.run(app, host="127.0.0.1", port=args.port)
        return
    print("Fixture 실행" if args.offline else "실제 연동: 기본 모델 invoke 최대2회, --compare-k 사용 시 1회 추가")
    report = run_smoke(offline=args.offline, compare_k=args.compare_k)
    filename = "api_fixture_report.json" if args.offline else "api_live_report.json"
    path = save_json(HERE, filename, report)
    show_success("08 · API 요청 결과 기록", path)
    for row in report["api_cases"]:
        print(row["case"], row["http_status"], row["included_ids"], row["response_source_ids"])
    if not report["checks_passed"]:
        print("기대 상태 또는 출처 연결이 다릅니다. 저장한 결과와 원문을 확인하세요.")
        raise SystemExit(1)
    print("요청·상태·출처 검사 완료. 원문 대조는 reports/review.md에 기록하세요.")


if __name__ == "__main__":
    main()
