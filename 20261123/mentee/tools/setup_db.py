"""오늘의 세 문서를 Day26 전용 Schema에 준비합니다. --apply가 있어야 실제 실행합니다."""
from pathlib import Path
import sys
import argparse

ROLE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROLE_ROOT))


def main(argv=None):
    parser = argparse.ArgumentParser(description="Day26 전용 E5·pgvector 데이터 준비")
    parser.add_argument("--apply", action="store_true", help="실제 DB·E5 모델을 사용해 저장·공개")
    args = parser.parse_args(argv)
    if not args.apply:
        print("아직 DB·모델을 실행하지 않았습니다.")
        print("역할 폴더의 .env, pgvector 서버 확장, requirements_live.txt 준비를 확인하세요.")
        print("실제 준비: python tools/setup_db.py --apply")
        print("RAG_SCHEMA 기본값은 d26_rag이며 기존 Day24 Schema는 사용하지 않습니다.")
        return 0

    from coursekit.live import connect_db, load_encoder, encoder_contract, encode_passage
    from coursekit.db import publish_corpus
    from coursekit.config import schema_name
    from coursekit.data import load_hits
    from coursekit.io import save_json, show_success
    from coursekit.reporting import execution_record

    hits = load_hits()
    # 연결은 autocommit=True. 확장이 있는지 확인한 뒤 쓰기 Transaction 밖에서 모델·벡터를 준비합니다.
    with connect_db() as conn:
        model = load_encoder()
        contract = encoder_contract(model)
        vectors = [encode_passage(model, hit["body"]) for hit in hits]
        # 아래 블록 중 하나라도 실패하면 전체 쓰기가 rollback됩니다.
        with conn.transaction():
            sources = publish_corpus(conn, hits, vectors, contract)
    # 여기까지 와야 commit과 연결 종료가 끝난 것입니다. 성공 기록은 이 시점에만 저장합니다.
    report = {
        "execution": execution_record("live_db_setup", db=True, embedding=True),
        "schema": schema_name(), "embedding_contract": contract,
        "document_count": len(hits), "sources": sources,
        "note": "실제 E5·PostgreSQL 준비 결과. citation_id는 DB가 생성한 값을 보존합니다.",
    }
    path = save_json(ROLE_ROOT, "db_setup.json", report)
    show_success("Day26 DB 준비 완료", path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
