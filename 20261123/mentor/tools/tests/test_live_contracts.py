"""E5·DB 계약의 오프라인 검사. 실제 모델·네트워크·PostgreSQL은 사용하지 않습니다."""
from pathlib import Path
from types import SimpleNamespace
from copy import deepcopy
import importlib.util
import subprocess
import sys

import numpy as np
import pytest

ROLE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROLE))
from coursekit import live, db
from coursekit.data import load_hits


class FakeEncoder:
    """호출 내용을 기록하는 테스트 대역. E5 Embedding 결과라고 주장하지 않습니다."""
    max_seq_length = 8
    _day26_requested_revision = "main"
    def __init__(self, token_count=4, vector=None):
        self.token_count = token_count
        self.token_calls = []
        self.encode_calls = []
        self.vector = np.eye(1, 384, dtype=np.float32)[0] if vector is None else vector
    def get_sentence_embedding_dimension(self):
        return 384
    def __getitem__(self, index):
        return SimpleNamespace(auto_model=SimpleNamespace(config=SimpleNamespace(_commit_hash="a" * 40)))
    def tokenizer(self, text, **kwargs):
        self.token_calls.append((text, kwargs))
        return {"input_ids": list(range(self.token_count))}
    def encode(self, text, **kwargs):
        self.encode_calls.append((text, kwargs))
        return self.vector


class Result:
    def __init__(self, rows=()):
        self.rows = list(rows)
    def fetchone(self):
        return self.rows[0] if self.rows else None
    def fetchall(self):
        return self.rows


class RecordingConnection:
    """SQL·Transaction 이벤트 기록용 대역. PostgreSQL 실행 결과를 가장하지 않습니다."""
    def __init__(self, *, exists=True, marker=True, metadata=None, rows=(), fail_search=False,
                 fail_update=False, extension=True):
        self.exists, self.marker = exists, marker
        self.metadata = dict(metadata or {})
        self.rows = list(rows)
        self.fail_search, self.fail_update, self.extension = fail_search, fail_update, extension
        self.closed = False
        self.events = []
        self.calls = []
        self.ids = {}
    def execute(self, query, params=None):
        text = query.as_string() if hasattr(query, "as_string") else str(query)
        self.calls.append((text, params))
        normalized = " ".join(text.split())
        if "pg_extension" in text:
            return Result([("public",)]) if self.extension else Result()
        if normalized.startswith("SELECT EXISTS"):
            return Result([(self.exists,)])
        if normalized.startswith("SELECT to_regclass"):
            return Result([("d26_test.rag_meta" if self.marker else None,)])
        if normalized.startswith("SELECT key, value"):
            return Result(list(self.metadata.items()))
        if normalized.startswith("CREATE SCHEMA"):
            self.exists = True
        if normalized.startswith("CREATE TABLE") and "rag_meta" in text:
            self.marker = True
        if normalized.startswith("INSERT INTO") and "rag_meta" in text:
            self.metadata.setdefault(params[0], params[1].obj)
        if normalized.startswith("INSERT INTO") and "rag_chunks" in text:
            self.ids.setdefault(params[0], 5001 + len(self.ids))
            return Result([(self.ids[params[0]],)])
        if normalized.startswith("UPDATE") and self.fail_update:
            raise RuntimeError("synthetic write failure")
        if normalized.startswith("SELECT c.citation_id"):
            if self.fail_search:
                raise RuntimeError("synthetic database failure")
            return Result(self.rows)
        return Result()
    def close(self):
        self.closed = True
        self.events.append("CLOSE")
    def __enter__(self):
        return self
    def __exit__(self, kind, value, traceback):
        self.close()
        return False
    def transaction(self):
        connection = self
        class Transaction:
            def __enter__(self):
                connection.events.append("BEGIN")
                self.snapshot = deepcopy((connection.exists, connection.marker, connection.metadata, connection.ids))
            def __exit__(self, kind, value, traceback):
                if kind:
                    connection.exists, connection.marker, connection.metadata, connection.ids = self.snapshot
                    connection.events.append("ROLLBACK")
                else:
                    connection.events.append("COMMIT")
                return False
        return Transaction()


@pytest.fixture(autouse=True)
def chosen_schema(monkeypatch):
    monkeypatch.setenv("RAG_SCHEMA", "d26_test")


def ready_connection(model, **kwargs):
    return RecordingConnection(metadata={"purpose": db.PURPOSE, "embedding_contract": live.encoder_contract(model)}, **kwargs)


def test_prefix_tokenizer_and_normalization_contract():
    model = FakeEncoder()
    live.encode_query(model, "질문")
    live.encode_passage(model, "본문")
    assert [v[0] for v in model.token_calls] == ["query: 질문", "passage: 본문"]
    assert all(kwargs == {"truncation": False, "add_special_tokens": True} for _, kwargs in model.token_calls)
    assert all(kwargs["normalize_embeddings"] is True for _, kwargs in model.encode_calls)
    contract = live.encoder_contract(model)
    assert contract["revision"] == "a" * 40
    assert contract["dimension"] == 384 and contract["normalized"] is True


def test_long_input_stops_before_embedding():
    model = FakeEncoder(token_count=9)
    with pytest.raises(ValueError, match="초과"):
        live.encode_query(model, "길이 경계")
    assert model.encode_calls == []
    boundary = FakeEncoder(token_count=8)
    live.encode_query(boundary, "경계와 같은 길이")
    assert len(boundary.encode_calls) == 1


@pytest.mark.parametrize("value", [np.zeros(384), np.ones(383), np.full(384, np.nan), np.full(384, np.inf), np.ones((1, 384))])
def test_invalid_vectors_are_not_sent_to_database(value):
    with pytest.raises(ValueError):
        live.encode_passage(FakeEncoder(vector=value), "본문")


def test_encoder_load_is_explicit_cpu_and_reuses_revision(monkeypatch):
    calls = []
    model = FakeEncoder()
    monkeypatch.setitem(sys.modules, "torch", SimpleNamespace(
        set_num_threads=lambda n: calls.append(("threads", n)), manual_seed=lambda n: calls.append(("seed", n))))
    def construct(name, **kwargs):
        calls.append((name, kwargs))
        return model
    monkeypatch.setitem(sys.modules, "sentence_transformers", SimpleNamespace(SentenceTransformer=construct))
    monkeypatch.setattr(live, "load_settings", lambda: None)
    monkeypatch.setenv("E5_REVISION", "test-revision")
    live._cached_encoder.cache_clear()
    try:
        assert live.load_encoder() is live.load_encoder()
        assert ("threads", 1) in calls and ("seed", 42) in calls
        builds = [v for v in calls if v[0] == live.MODEL_ID]
        assert builds == [(live.MODEL_ID, {"revision": "test-revision", "device": "cpu"})]
    finally:
        live._cached_encoder.cache_clear()


def test_search_filters_parameters_and_row_mapping_preserve_database_id():
    model = FakeEncoder()
    connection = ready_connection(model, rows=[(9876, "real-chunk", "실제 조회 본문 예시", "actual.md#1", "DOC-X", "v9", 0.12)])
    search = live.make_search_hits(model=model, connect=lambda: connection)
    hits = search("질문을 SQL 문자열에 연결하지 않습니다", "학사", k=2)
    assert connection.closed
    assert hits[0]["citation_id"] == 9876 and hits[0]["source_version"] == "v9"
    assert hits[0]["body"] == "실제 조회 본문 예시"
    query, params = next((q,p) for q,p in connection.calls if "SELECT c.citation_id" in q)
    assert "current_source_version" in query and "current_pipeline_version" in query
    assert "c.ready = TRUE" in query and "d.category = %s" in query
    assert "ORDER BY cosine_distance ASC, c.citation_id ASC" in query
    assert params[1:] == ("학사", live.MODEL_ID, "a" * 40, 2)
    assert "질문" not in query


def test_each_search_closes_its_own_connection_and_failure_propagates():
    model = FakeEncoder()
    connections = [ready_connection(model), ready_connection(model, fail_search=True)]
    pending = iter(connections)
    search = live.make_search_hits(model=model, connect=lambda: next(pending))
    assert search("첫 질문", "학사") == []
    with pytest.raises(RuntimeError, match="synthetic database failure"):
        search("다음 질문", "학사")
    assert all(conn.closed for conn in connections)


@pytest.mark.parametrize("question,category,k", [("", "학사", 3), ("q", "알수없음", 3), ("q", "학사", 0), ("q", "학사", 21), ("q", "학사", True)])
def test_invalid_search_arguments_fail_before_connection(question, category, k):
    model = FakeEncoder()
    def must_not_connect():
        raise AssertionError("connection should not open")
    with pytest.raises(ValueError):
        live.make_search_hits(model=model, connect=must_not_connect)(question, category, k)
    assert model.encode_calls == []


def test_mismatched_embedding_contract_stops_before_candidate_query():
    model = FakeEncoder()
    conn = ready_connection(model)
    conn.metadata["embedding_contract"] = {**live.encoder_contract(model), "revision": "different"}
    with pytest.raises(RuntimeError, match="계약이 다릅니다"):
        live.make_search_hits(model=model, connect=lambda: conn)("질문", "학사")
    assert conn.closed
    assert not any("SELECT c.citation_id" in q for q,p in conn.calls)


def test_connection_setup_closes_on_failure_and_registers_vector(monkeypatch):
    import psycopg
    import pgvector.psycopg
    opened = []
    registered = []
    def connect(**kwargs):
        opened.append(kwargs)
        return conn
    monkeypatch.setattr(live, "db_parameters", lambda: {"dbname": "unit_test"})
    monkeypatch.setattr(psycopg, "connect", connect)
    monkeypatch.setattr(pgvector.psycopg, "register_vector", lambda c: registered.append(c))
    conn = RecordingConnection(extension=False)
    with pytest.raises(RuntimeError, match="서버 확장"):
        live.connect_db()
    assert conn.closed and registered == []
    conn = RecordingConnection()
    assert live.connect_db() is conn
    assert registered == [conn] and not conn.closed
    assert opened[-1]["autocommit"] is True
    conn.close()


@pytest.mark.parametrize("marker,metadata", [(False, {}), (True, {"purpose":"other-project"})])
def test_existing_unowned_schema_is_not_modified(marker, metadata):
    conn = RecordingConnection(exists=True, marker=marker, metadata=metadata)
    contract = live.encoder_contract(FakeEncoder())
    with pytest.raises(RuntimeError):
        db.prepare_schema(conn, contract)
    assert not any(q.lstrip().startswith(("CREATE", "INSERT", "UPDATE", "DROP")) for q,p in conn.calls)


def test_changed_contract_cannot_overwrite_existing_schema():
    model = FakeEncoder()
    conn = ready_connection(model)
    changed = {**live.encoder_contract(model), "max_seq_length": 9}
    with pytest.raises(RuntimeError, match="계약이 다릅니다"):
        db.prepare_schema(conn, changed)
    assert not any(q.lstrip().startswith(("CREATE", "INSERT", "UPDATE", "DROP")) for q,p in conn.calls)


def test_repeated_publication_keeps_database_ids_and_publishes_last():
    model = FakeEncoder()
    contract = live.encoder_contract(model)
    conn = RecordingConnection(exists=False, marker=False)
    vectors = [model.vector.copy() for _ in load_hits()]
    with conn.transaction():
        first = db.publish_corpus(conn, load_hits(), vectors, contract)
    with conn.transaction():
        second = db.publish_corpus(conn, load_hits(), vectors, contract)
    assert first == second
    assert [v["citation_id"] for v in first] == [5001, 5002, 5003]
    assert not any("DROP " in q for q,p in conn.calls)
    inserts = [i for i,(q,p) in enumerate(conn.calls) if "INSERT INTO" in q and "rag_chunks" in q]
    first_publish = next(i for i,(q,p) in enumerate(conn.calls) if "SET ready=TRUE" in q)
    assert first_publish > inserts[2]
    assert conn.events == ["BEGIN", "COMMIT", "BEGIN", "COMMIT"]


def load_setup():
    spec = importlib.util.spec_from_file_location("day26_setup_db_under_test", ROLE / "tools" / "setup_db.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_setup_without_apply_does_not_request_model_or_connection(monkeypatch, capsys):
    def must_not_call():
        raise AssertionError("live execution was not requested")
    monkeypatch.setattr(live, "connect_db", must_not_call)
    monkeypatch.setattr(live, "load_encoder", must_not_call)
    assert load_setup().main([]) == 0
    assert "아직 DB·모델을 실행하지 않았습니다" in capsys.readouterr().out


@pytest.mark.parametrize("fail_update", [False, True])
def test_setup_transaction_and_success_record_order(monkeypatch, tmp_path, fail_update):
    from coursekit import io
    model = FakeEncoder()
    conn = RecordingConnection(exists=False, marker=False, fail_update=fail_update)
    monkeypatch.setattr(live, "connect_db", lambda: conn)
    monkeypatch.setattr(live, "load_encoder", lambda: model)
    original_encode = live.encode_passage
    def encode(m, text):
        conn.events.append("ENCODE")
        return original_encode(m, text)
    monkeypatch.setattr(live, "encode_passage", encode)
    records = []
    def save(here, name, report):
        conn.events.append("SAVE")
        records.append(report)
        return tmp_path/name
    monkeypatch.setattr(io, "save_json", save)
    monkeypatch.setattr(io, "show_success", lambda *a: None)
    if fail_update:
        with pytest.raises(RuntimeError, match="synthetic write failure"):
            load_setup().main(["--apply"])
        assert records == [] and "ROLLBACK" in conn.events and "COMMIT" not in conn.events
        assert not conn.exists and conn.metadata == {} and conn.ids == {}
    else:
        assert load_setup().main(["--apply"]) == 0
        assert conn.events[:3] == ["ENCODE"]*3
        assert conn.events[-3:] == ["COMMIT", "CLOSE", "SAVE"]
        assert records[0]["execution"] == {"mode":"live_db_setup", "db":True, "embedding":True, "llm":False}
        assert [v["citation_id"] for v in records[0]["sources"]] == [5001,5002,5003]
    assert conn.closed
