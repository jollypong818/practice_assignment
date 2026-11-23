"""실제 PostgreSQL 18 + pgvector의 독립 실습 테이블 (ingest_ 접두어).

SQL의 %s 자리는 psycopg parameter binding 전용입니다. pgAdmin에서 그대로 실행하지 않습니다.
"""
from __future__ import annotations
import hashlib
import json
from .live import DIM

SCHEMA_SQL='''
CREATE TABLE IF NOT EXISTS ingest_documents (
  doc_id text PRIMARY KEY,
  source_uri text NOT NULL,
  current_version text,
  current_pipeline_version text
);
CREATE TABLE IF NOT EXISTS ingest_versions (
  doc_id text NOT NULL REFERENCES ingest_documents(doc_id),
  source_version text NOT NULL,
  pipeline_version text NOT NULL,
  status text NOT NULL CHECK(status IN ('staging','ready','failed')),
  expected_count integer NOT NULL CHECK(expected_count >= 1),
  PRIMARY KEY (doc_id, source_version, pipeline_version)
);
CREATE TABLE IF NOT EXISTS ingest_chunks (
  citation_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  chunk_id text NOT NULL UNIQUE,
  doc_id text NOT NULL,
  source_version text NOT NULL,
  pipeline_version text NOT NULL,
  unit_id text NOT NULL,
  category text NOT NULL,
  source_locator text NOT NULL,
  char_start integer NOT NULL,
  char_end integer NOT NULL,
  body text NOT NULL CHECK(length(body) > 0),
  embedding vector(384) NOT NULL,
  metadata jsonb NOT NULL,
  CHECK (char_start >= 0 AND char_end > char_start),
  FOREIGN KEY (doc_id, source_version, pipeline_version)
    REFERENCES ingest_versions(doc_id, source_version, pipeline_version)
);
CREATE INDEX IF NOT EXISTS ingest_chunks_category_idx ON ingest_chunks(category);
'''


PRACTICE_SCHEMAS=('d24_basic07','d24_inter07','d24_adv07','d24_adv08')


def use_schema(conn, scope: str)->None:
    """실습별 전용 schema. 같은 DB에서도 다른 난이도/과제의 데이터를 섞지 않습니다.

    DB Identifier는 사전에 허용한 네 이름만 사용할 수 있습니다.
    """
    if scope not in PRACTICE_SCHEMAS:
        raise ValueError('unknown lab DB scope')
    from psycopg import sql
    conn.execute(sql.SQL('CREATE SCHEMA IF NOT EXISTS {}').format(sql.Identifier(scope)))
    conn.execute(sql.SQL('SET search_path TO {}, public').format(sql.Identifier(scope)))


def initialize(conn):
    """테이블만 생성. pgvector 확장 활성화는 이미 pgAdmin에서 완료되어야 합니다."""
    with conn.transaction():
        for statement in SCHEMA_SQL.split(';'):
            if statement.strip():conn.execute(statement)


def stage_version(conn, doc: dict, source_uri: str, chunks: list[dict], vectors) -> None:
    """이미 계산·검증된 벡터를 저장합니다. conn.transaction() 안에서만 호출."""
    from pgvector import Vector
    from psycopg.types.json import Jsonb
    if len(chunks)!=len(vectors) or not chunks:raise ValueError('rows/vectors mismatch or empty')
    key=(doc['doc_id'],doc['source_version'],chunks[0]['pipeline_version'])
    for row in chunks:
        if (row['doc_id'],row['source_version'],row['pipeline_version'])!=key:
            raise ValueError('mixed contract/versions')
    conn.execute('INSERT INTO ingest_documents (doc_id,source_uri) VALUES (%s,%s) '
                 'ON CONFLICT(doc_id) DO NOTHING',(doc['doc_id'],source_uri))
    conn.execute('INSERT INTO ingest_versions (doc_id,source_version,pipeline_version,status,expected_count) '
                 "VALUES (%s,%s,%s,'staging',%s) ON CONFLICT DO NOTHING",(*key,len(chunks)))
    state=conn.execute('SELECT expected_count FROM ingest_versions WHERE doc_id=%s AND source_version=%s '
                       'AND pipeline_version=%s',key).fetchone()
    if state is None or state[0]!=len(chunks):raise ValueError('version reused with different chunk count')
    for row,vec in zip(chunks,vectors,strict=True):
        params=(row['chunk_id'],*key,row['unit_id'],row['category'],row['source_locator'],
                row['char_start'],row['char_end'],row['body'],Vector(vec),Jsonb({
                    'section_title':row.get('section_title',''),
                    'page_number':row.get('page_number'),
                    'model':'intfloat/multilingual-e5-small',
                    'embedding_contract':row['pipeline_version']}))
        conn.execute('''INSERT INTO ingest_chunks
           (chunk_id,doc_id,source_version,pipeline_version,unit_id,category,source_locator,
            char_start,char_end,body,embedding,metadata)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (chunk_id) DO NOTHING''', params)
        saved=conn.execute('SELECT doc_id,source_version,pipeline_version,body FROM ingest_chunks '
                           'WHERE chunk_id=%s',(row['chunk_id'],)).fetchone()
        if saved!=(*key,row['body']):raise ValueError('chunk ID collision / body changed under same version')
    actual={r[0] for r in conn.execute('SELECT chunk_id FROM ingest_chunks WHERE doc_id=%s AND '
        'source_version=%s AND pipeline_version=%s',key).fetchall()}
    if actual!={r['chunk_id'] for r in chunks}:
        raise ValueError('existing version contains stale/missing chunk IDs')


def publish_version(conn, doc_id: str, source_version: str, pipeline_version: str) -> None:
    """ready 검사와 현재 포인터 변경은 호출자의 짧은 transaction에서 처리."""
    key=(doc_id,source_version,pipeline_version)
    row=conn.execute('SELECT expected_count FROM ingest_versions WHERE doc_id=%s AND '
                     'source_version=%s AND pipeline_version=%s FOR UPDATE',key).fetchone()
    if row is None:raise ValueError('no staged version')
    count=conn.execute('SELECT count(*) FROM ingest_chunks WHERE doc_id=%s AND source_version=%s '
                       'AND pipeline_version=%s',key).fetchone()[0]
    if count!=row[0]:raise ValueError('version not fully staged')
    conn.execute("UPDATE ingest_versions SET status='ready' WHERE doc_id=%s AND source_version=%s AND pipeline_version=%s",key)
    updated=conn.execute('''UPDATE ingest_documents d
        SET current_version=v.source_version, current_pipeline_version=v.pipeline_version
        FROM ingest_versions v
        WHERE d.doc_id=v.doc_id AND v.doc_id=%s AND v.source_version=%s
          AND v.pipeline_version=%s AND v.status='ready'
        RETURNING d.doc_id''',key).fetchone()
    if updated is None:raise ValueError('publication refused')


def search_current(conn, query_vector, category: str, k: int=3):
    from pgvector import Vector
    if type(k) is not int or not 1<=k<=20:raise ValueError('invalid k')
    if not category or type(category) is not str:raise ValueError('invalid category')
    # 현재 공개 포인터가 가리키는 문서·처리 버전만 사용합니다.
    return conn.execute('''SELECT c.citation_id, c.chunk_id, c.body, c.source_locator,
            c.doc_id, c.source_version, c.embedding <=> %s AS cosine_distance
       FROM ingest_chunks c JOIN ingest_documents d ON c.doc_id=d.doc_id
       JOIN ingest_versions v ON (v.doc_id=c.doc_id AND v.source_version=c.source_version
                                  AND v.pipeline_version=c.pipeline_version)
       WHERE c.source_version=d.current_version
         AND c.pipeline_version=d.current_pipeline_version AND v.status='ready'
         AND c.category=%s
       ORDER BY c.embedding <=> %s ASC, c.chunk_id ASC LIMIT %s''',
       (Vector(query_vector), category, Vector(query_vector), k)).fetchall()
