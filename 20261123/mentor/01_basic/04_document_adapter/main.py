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

# 오늘의 최소 Metadata 계약. 여섯 값 모두 입력 Hit에서 가져옵니다.
METADATA_KEYS = ("citation_id", "chunk_id", "doc_id", "source_version", "source_locator", "category")

def to_document(hit: dict) -> Document:
    """한 Hit의 본문과 여섯 Metadata 값을 Document로 옮깁니다."""
    # BEGIN D26-04-B01
    # page_content에는 본문을, metadata에는 여섯 출처 필드를 둡니다.
    # 정수 citation_id는 입력 값을 그대로 옮기므로 문자열로 바뀌지 않습니다.
    # hit[key]는 필수 Key가 없으면 KeyError를 내며 누락된 출처를 가짜 값으로 채우지 않습니다.
    metadata = {key: hit[key] for key in METADATA_KEYS}
    return Document(page_content=hit["body"], metadata=metadata)
    # END D26-04-B01

def hits_to_documents(hits: list[dict]) -> list[Document]:
    """순서대로 변환한 Document 목록을 반환합니다. 빈 입력은 빈 목록입니다."""
    # BEGIN D26-04-B02
    # 검색 순서를 그대로 유지해 각 Hit를 한 Document로 바꿉니다.
    # 빈 입력에는 반복이 한 번도 실행되지 않으므로 빈 목록을 반환합니다.
    # 변환은 검색이 아니며 입력의 문서가 질문에 충분한지는 별도로 판단해야 합니다.
    documents = []
    for hit in hits:
        documents.append(to_document(hit))
    return documents
    # END D26-04-B02

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
    path = save_json(HERE, "document_adapter.json", report)
    show_success("04 기본필수", path)

if __name__ == "__main__":
    main()
