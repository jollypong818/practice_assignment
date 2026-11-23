"""Day26 전용 Schema의 문서 공개와 현재 버전 검색.

SQL 값은 parameters로, Schema/Table 이름은 psycopg.sql.Identifier로 전달합니다.
기존 Day24나 다른 프로젝트의 테이블을 읽거나 삭제하지 않습니다.
"""
from coursekit.config import schema_name

PURPOSE = "day26-basic-rag-v1"
PIPELINE_VERSION = "d26-rag-v1"
CATEGORIES = {"학사", "시설", "지원"}


def use_schema(conn, schema, vector_schema="public"):
    from psycopg import sql
    # 이 함수로 임의 Schema를 선택하지 않도록 동일 이름 규칙을 적용합니다.
    import re
    if not re.fullmatch(r"d26_[a-z0-9_]{1,50}", schema):
        raise ValueError("Day26의 d26_ 전용 Schema만 사용할 수 있습니다.")
    conn.execute(sql.SQL("SET search_path TO {}, {}, pg_catalog").format(
        sql.Identifier(schema), sql.Identifier(vector_schema)))


def validate_search_arguments(question, category, k):
    if not isinstance(question, str) or not question.strip():
        raise ValueError("question은 비어 있지 않은 문자열이어야 합니다.")
    if category not in CATEGORIES:
        raise ValueError("category는 학사·시설·지원 중 하나여야 합니다.")
    if type(k) is not int or not 1 <= k <= 20:
        raise ValueError("k는 1~20 범위의 정수여야 합니다.")


def read_metadata(conn, schema):
    from psycopg import sql
    rows = conn.execute(sql.SQL("SELECT key, value FROM {} WHERE key IN (%s, %s)").format(
        sql.Identifier(schema, "rag_meta")), ("purpose", "embedding_contract")).fetchall()
    return dict(rows)


def check_metadata(metadata, contract):
    if metadata.get("purpose") != PURPOSE:
        raise RuntimeError("Day26 목적 표식이 없는 Schema입니다. 다른 d26_ 이름을 사용하세요.")
    if metadata.get("embedding_contract") != contract:
        raise RuntimeError("저장 벡터와 질의의 Embedding 계약이 다릅니다. "
                           "모델·revision·Prefix·차원·정규화·최대 길이를 확인하세요. "
                           "다른 설정은 새 d26_ Schema에 다시 준비하세요.")


def search_current(conn, vector, category, k=3, *, contract):
    """현재 공개 버전·ready·Category가 맞는 후보를 Cosine Distance 순으로 반환합니다."""
    from psycopg import sql
    validate_search_arguments("validated query", category, k)
    schema = schema_name()
    check_metadata(read_metadata(conn, schema), contract)
    query = sql.SQL("""
        SELECT c.citation_id, c.chunk_id, c.body, c.source_locator,
               c.doc_id, c.source_version, c.embedding <=> %s AS cosine_distance
        FROM {chunks} AS c
        JOIN {documents} AS d ON d.doc_id = c.doc_id
        WHERE d.category = %s
          AND c.source_version = d.current_source_version
          AND c.pipeline_version = d.current_pipeline_version
          AND c.ready = TRUE
          AND c.embedding_model = %s AND c.embedding_revision = %s
        ORDER BY cosine_distance ASC, c.citation_id ASC
        LIMIT %s
    """).format(chunks=sql.Identifier(schema, "rag_chunks"),
                  documents=sql.Identifier(schema, "rag_documents"))
    return conn.execute(query, (vector, category, contract["model_id"],
                                contract["revision"], k)).fetchall()


def prepare_schema(conn, contract):
    """호출자의 단일 Transaction 안에서만 호출합니다."""
    from psycopg import sql
    from psycopg.types.json import Jsonb
    schema = schema_name()
    exists = conn.execute(
        "SELECT EXISTS (SELECT 1 FROM pg_catalog.pg_namespace WHERE nspname=%s)",
        (schema,)).fetchone()[0]
    if exists:
        marker = conn.execute("SELECT to_regclass(%s)", (f"{schema}.rag_meta",)).fetchone()[0]
        if marker is None:
            raise RuntimeError("기존 Schema에 Day26 목적 표식 테이블이 없습니다. 새 d26_ 이름을 선택하세요.")
        # 기존 데이터를 변경하기 전에 목적과 Embedding 설정이 일치하는지 확인합니다.
        check_metadata(read_metadata(conn, schema), contract)
    else:
        conn.execute(sql.SQL("CREATE SCHEMA {}").format(sql.Identifier(schema)))
    meta = sql.Identifier(schema, "rag_meta")
    documents = sql.Identifier(schema, "rag_documents")
    chunks = sql.Identifier(schema, "rag_chunks")
    conn.execute(sql.SQL("CREATE TABLE IF NOT EXISTS {} (key TEXT PRIMARY KEY, value JSONB NOT NULL)").format(meta))
    conn.execute(sql.SQL("""CREATE TABLE IF NOT EXISTS {} (
        doc_id TEXT PRIMARY KEY, category TEXT NOT NULL,
        current_source_version TEXT, current_pipeline_version TEXT
    )""").format(documents))
    conn.execute(sql.SQL("""CREATE TABLE IF NOT EXISTS {chunks} (
        citation_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        chunk_id TEXT UNIQUE NOT NULL, doc_id TEXT NOT NULL REFERENCES {documents}(doc_id),
        source_version TEXT NOT NULL, pipeline_version TEXT NOT NULL,
        source_locator TEXT NOT NULL, body TEXT NOT NULL,
        embedding_model TEXT NOT NULL, embedding_revision TEXT NOT NULL,
        embedding vector(384) NOT NULL, ready BOOLEAN NOT NULL DEFAULT FALSE
    )""").format(chunks=chunks, documents=documents))
    for key, value in [("purpose", PURPOSE), ("embedding_contract", contract)]:
        conn.execute(sql.SQL("INSERT INTO {} (key,value) VALUES (%s,%s) "
                            "ON CONFLICT (key) DO NOTHING").format(meta), (key, Jsonb(value)))
    return schema


def publish_corpus(conn, hits, vectors, contract):
    """검증된 벡터를 저장한 뒤 ready와 현재 버전 Pointer를 같은 Transaction으로 공개합니다.

    함수 안에서 commit하지 않습니다. 호출자의 Transaction이 전체 성공 시 한 번 commit합니다.
    동일 chunk_id를 upsert하므로 재실행해도 기존 citation_id를 그대로 사용합니다.
    """
    from psycopg import sql
    if len(hits) != len(vectors) or not hits:
        raise ValueError("Hit와 실제 벡터의 개수가 같고 비어 있지 않아야 합니다.")
    schema = prepare_schema(conn, contract)
    documents = sql.Identifier(schema, "rag_documents")
    chunks = sql.Identifier(schema, "rag_chunks")
    sources = []
    for hit, vector in zip(hits, vectors):
        conn.execute(sql.SQL("INSERT INTO {} (doc_id,category) VALUES (%s,%s) "
                            "ON CONFLICT (doc_id) DO UPDATE SET category=EXCLUDED.category").format(documents),
                     (hit["doc_id"], hit["category"]))
        row = conn.execute(sql.SQL("""
            INSERT INTO {chunks} (chunk_id,doc_id,source_version,pipeline_version,source_locator,
                                  body,embedding_model,embedding_revision,embedding,ready)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,FALSE)
            ON CONFLICT (chunk_id) DO UPDATE SET
                doc_id=EXCLUDED.doc_id, source_version=EXCLUDED.source_version,
                pipeline_version=EXCLUDED.pipeline_version, source_locator=EXCLUDED.source_locator,
                body=EXCLUDED.body, embedding_model=EXCLUDED.embedding_model,
                embedding_revision=EXCLUDED.embedding_revision, embedding=EXCLUDED.embedding, ready=FALSE
            RETURNING citation_id
        """).format(chunks=chunks),
            (hit["chunk_id"], hit["doc_id"], hit["source_version"], PIPELINE_VERSION,
             hit["source_locator"], hit["body"], contract["model_id"], contract["revision"], vector)).fetchone()
        sources.append({"citation_id": row[0], "chunk_id": hit["chunk_id"],
                        "doc_id": hit["doc_id"], "source_version": hit["source_version"],
                        "source_locator": hit["source_locator"], "category": hit["category"]})
    # 모든 벡터가 준비된 후에만 ready와 현재 버전을 공개합니다.
    for source in sources:
        conn.execute(sql.SQL("UPDATE {} SET ready=TRUE WHERE citation_id=%s").format(chunks),
                     (source["citation_id"],))
        conn.execute(sql.SQL("UPDATE {} SET current_source_version=%s, current_pipeline_version=%s "
                            "WHERE doc_id=%s").format(documents),
                     (source["source_version"], PIPELINE_VERSION, source["doc_id"]))
    return sources
