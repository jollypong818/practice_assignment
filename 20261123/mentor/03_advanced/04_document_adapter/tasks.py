"""Day26 실습. 실행 위치와 관계없이 현재 역할 폴더의 지원 모듈을 사용합니다."""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))
from coursekit.io import save_json, show_success
from coursekit.data import example_hit, load_hits
from coursekit.reporting import execution_record
from langchain_core.documents import Document
import argparse

def metadata_of(hit: dict) -> dict:
    """본문과 분리해서 여섯 Metadata 필드를 그대로 반환합니다."""
    # BEGIN D26-04-A01
    # 문서·버전·위치와 두 식별자, category를 명시적으로 보존합니다.
    # 현재 조회 계약이 돌려주지 않는 pipeline_version을 추정해서 추가하지 않습니다.
    # cosine_distance는 Hit에 남아 있지만 이 최소 Document 어댑터에서는 제외합니다.
    keys = ("citation_id", "chunk_id", "doc_id", "source_version", "source_locator", "category")
    return {key: hit[key] for key in keys}
    # END D26-04-A01

def to_document(hit: dict) -> Document:
    """원문 본문을 그대로 두고 출처 Metadata와 함께 Document를 생성합니다."""
    # BEGIN D26-04-A02
    # Document는 데이터를 보관합니다. 객체를 생성했다고 Embedding이나 LLM을 실행한 것은 아닙니다.
    # 본문을 다시 요약하거나 숫자·문장을 잘라서 넣지 않습니다.
    return Document(page_content=hit["body"], metadata=metadata_of(hit))
    # END D26-04-A02

def hits_to_documents(hits: list[dict]) -> list[Document]:
    """같은 순서의 Document 목록을 반환합니다."""
    # BEGIN D26-04-A03
    # 빈 결과와 필수 필드 누락은 다릅니다. 빈 목록은 정상적인 빈 결과입니다.
    # 원문 위치가 없는 Hit는 변환 중 KeyError가 발생해야 하며 빈 결과로 숨기지 않습니다.
    documents = []
    for hit in hits:
        documents.append(to_document(hit))
    return documents
    # END D26-04-A03

def inspect_boundary_cases(hit: dict) -> dict:
    """교육용 복사본으로 빈 입력과 원문 위치 누락을 대조합니다."""
    # BEGIN D26-04-A04
    # 오류 사례용 복사본만 수정합니다. 원본 Hit를 지우면 뒤의 정상 확인에 영향을 줍니다.
    # KeyError는 이 교육용 비교에서만 포착합니다. 실제 hits_to_documents는 오류를 호출자에게 전달합니다.
    # 빈 결과를 처리할 수 있다는 것과 출처 누락을 무시하는 것은 다릅니다.
    empty = hits_to_documents([])
    incomplete = dict(hit)
    incomplete.pop("source_locator")
    try:
        hits_to_documents([incomplete])
    except KeyError as exc:
        missing_key = str(exc.args[0])
    else:
        raise AssertionError("필수 source_locator 누락을 감지하지 못했습니다.")
    return {"empty_count": len(empty), "missing_key": missing_key}
    # END D26-04-A04

def metadata_is_preserved(hit: dict, metadata: dict) -> bool:
    """제공된 관찰 함수: 여섯 필드가 모두 있고 각 값이 같은지 확인합니다."""
    required = {"citation_id", "chunk_id", "doc_id", "source_version", "source_locator", "category"}
    # 일부 필드만 복사한 결과를 '보존 완료'로 표시하지 않도록 Key 집합부터 확인합니다.
    return set(metadata) == required and all(metadata[key] == hit[key] for key in required)


def main():
    parser = argparse.ArgumentParser(description="Hit → 실제 LangChain Document 변환")
    parser.add_argument("--live-db", action="store_true", help="실제 E5·PostgreSQL 검색 결과를 입력으로 사용")
    parser.add_argument("--question", default="15분 늦으면 어떻게 기록되나요?")
    parser.add_argument("--category", default="학사", choices=["학사", "시설", "지원"])
    parser.add_argument("--candidate-k", type=int, default=3)
    args = parser.parse_args()
    if args.live_db:
        # --live-db를 선택한 경우에만 실제 모델·DB 준비 함수를 불러옵니다.
        from coursekit.live import make_search_hits
        search_hits = make_search_hits()
        hits = search_hits(args.question, args.category, k=args.candidate_k)
        mode, input_source = "live_db", "E5_PostgreSQL"
    else:
        hits = [example_hit()]
        mode, input_source = "local_adapter", "lecture_fixture"
    documents = hits_to_documents(hits)
    comparisons = []
    for hit, doc in zip(hits, documents):
        comparisons.append({
            "citation_id": doc.metadata["citation_id"],
            "body_preserved": doc.page_content == hit["body"],
            "metadata_preserved": metadata_is_preserved(hit, doc.metadata),
            "citation_id_type": type(doc.metadata["citation_id"]).__name__,
            "page_content": doc.page_content,
            "metadata": doc.metadata,
        })
    report = {
        "execution": execution_record(mode, db=args.live_db, embedding=args.live_db),
        "input_source": input_source,
        "input_count": len(hits), "document_count": len(documents),
        "documents": comparisons,
    }
    report["fixture_boundary_checks"] = inspect_boundary_cases(example_hit())
    path = save_json(HERE, "document_adapter.json", report)
    show_success("04 심화", path)

if __name__ == "__main__":
    main()
