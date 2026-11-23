"""명시적으로 호출했을 때만 CPU E5·PostgreSQL을 준비합니다.

모델을 import할 때 다운로드하거나 DB에 연결하지 않습니다. 검색 Factory가
준비된 모델을 보관하고, 실제 검색마다 새 연결을 열어 사용한 뒤 닫습니다.
"""
from functools import lru_cache
import os
from coursekit.config import load_settings, db_parameters, schema_name

MODEL_ID = "intfloat/multilingual-e5-small"
DIMENSION = 384
QUERY_PREFIX = "query: "
PASSAGE_PREFIX = "passage: "


@lru_cache(maxsize=2)
def _cached_encoder(revision):
    # 큰 선택 패키지는 실제 실행 경로에 들어왔을 때만 import합니다.
    import torch
    from sentence_transformers import SentenceTransformer
    torch.set_num_threads(1)
    torch.manual_seed(42)
    model = SentenceTransformer(MODEL_ID, revision=revision, device="cpu")
    model._day26_model_id = MODEL_ID
    model._day26_requested_revision = revision
    encoder_contract(model)  # 다른 차원·잘못된 최대 길이를 바로 발견합니다.
    return model


def load_encoder():
    """동일 revision의 CPU 모델을 프로세스에서 재사용합니다."""
    load_settings()
    revision = os.getenv("E5_REVISION", "main").strip() or "main"
    return _cached_encoder(revision)


def encoder_contract(model):
    """저장 벡터와 질의 벡터가 지켜야 하는 같은 설정을 기록합니다."""
    dimension = model.get_sentence_embedding_dimension()
    if dimension != DIMENSION:
        raise ValueError(f"E5 차원은 {DIMENSION}이어야 합니다: {dimension}")
    max_length = int(model.max_seq_length)
    if max_length <= 0:
        raise ValueError("model.max_seq_length가 유효하지 않습니다.")
    model_id = getattr(model, "_day26_model_id", MODEL_ID)
    if model_id != MODEL_ID:
        raise ValueError("이 실습은 multilingual-e5-small 모델만 사용합니다.")
    # main이라는 이동 가능한 이름 대신 실제 내려받은 commit을 우선 기록합니다.
    revision = None
    try:
        revision = getattr(model[0].auto_model.config, "_commit_hash", None)
    except (AttributeError, IndexError, TypeError):
        pass
    revision = revision or getattr(model, "_day26_requested_revision", None)
    revision = revision or os.getenv("E5_REVISION", "main").strip() or "main"
    return {
        "model_id": MODEL_ID, "revision": str(revision), "dimension": DIMENSION,
        "query_prefix": QUERY_PREFIX, "passage_prefix": PASSAGE_PREFIX,
        "normalized": True, "max_seq_length": max_length,
    }


def validate_vector(value):
    """384차원·유한값·단위 길이를 확인하고 pgvector에 넘길 NumPy 배열을 반환합니다."""
    import numpy as np
    vector = np.asarray(value, dtype=np.float32)
    if vector.shape != (DIMENSION,):
        raise ValueError(f"벡터 shape은 ({DIMENSION},)이어야 합니다: {vector.shape}")
    if not np.isfinite(vector).all():
        raise ValueError("벡터에 NaN 또는 Infinity가 있습니다.")
    norm = float(np.linalg.norm(vector.astype(np.float64)))
    if abs(norm - 1.0) > 1e-3:
        raise ValueError("normalize_embeddings=True로 만든 단위 벡터가 필요합니다.")
    return vector


def _encode(model, text, prefix):
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Embedding 입력은 비어 있지 않은 문자열이어야 합니다.")
    contract = encoder_contract(model)
    full_input = prefix + text
    # Prefix와 특수 Token까지 포함한 실제 입력을 검사합니다. 조용한 잘림을 허용하지 않습니다.
    encoded = model.tokenizer(full_input, truncation=False, add_special_tokens=True)
    token_count = len(encoded["input_ids"])
    if token_count > contract["max_seq_length"]:
        raise ValueError(
            f"Embedding 입력 {token_count} tokens가 모델 한도 {contract['max_seq_length']}를 초과합니다. "
            "본문을 임의로 자르지 말고 Chunk 구성을 확인하세요.")
    vector = model.encode(full_input, normalize_embeddings=True,
                          convert_to_numpy=True, show_progress_bar=False)
    return validate_vector(vector)


def encode_query(model, question):
    return _encode(model, question, QUERY_PREFIX)


def encode_passage(model, body):
    return _encode(model, body, PASSAGE_PREFIX)


def connect_db():
    """새 autocommit 연결을 만들고 확장·Schema를 준비합니다. 호출자가 with로 닫습니다.

    autocommit=True이므로 모델 준비 시간 동안 쓰기 Transaction을 유지하지 않습니다.
    setup_db의 저장 작업은 별도의 with conn.transaction() 안에서 원자적으로 실행합니다.
    """
    import psycopg
    from pgvector.psycopg import register_vector
    from coursekit.db import use_schema
    parameters = db_parameters()
    conn = psycopg.connect(**parameters, autocommit=True)
    try:
        row = conn.execute(
            "SELECT n.nspname FROM pg_catalog.pg_extension e "
            "JOIN pg_catalog.pg_namespace n ON n.oid=e.extnamespace "
            "WHERE e.extname=%s", ("vector",)).fetchone()
        if row is None:
            raise RuntimeError("현재 DB에 pgvector 서버 확장이 없습니다. "
                               "DB 준비 안내의 CREATE EXTENSION vector를 먼저 완료하세요.")
        use_schema(conn, schema_name(), vector_schema=row[0])
        register_vector(conn)
        return conn
    except Exception:
        conn.close()
        raise


def make_search_hits(model=None, connect=None):
    """실제 E5+DB 검색 함수. 입력 오류·DB 실패를 빈 목록으로 바꾸지 않습니다."""
    from coursekit.db import search_current, validate_search_arguments
    model = load_encoder() if model is None else model
    connector = connect_db if connect is None else connect
    contract = encoder_contract(model)

    def search_hits(question, category, k=3):
        validate_search_arguments(question, category, k)
        vector = encode_query(model, question)
        # psycopg3의 연결 context는 정상/실패 모두에서 연결을 닫습니다.
        with connector() as conn:
            rows = search_current(conn, vector, category, k, contract=contract)
        hits = []
        for cid, chunk, body, locator, doc, version, distance in rows:
            hits.append({
                "citation_id": cid, "chunk_id": chunk, "body": body,
                "source_locator": locator, "doc_id": doc,
                "source_version": version, "category": category,
                "cosine_distance": float(distance),
            })
        return hits
    return search_hits
