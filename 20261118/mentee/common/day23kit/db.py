"""실제 Windows PostgreSQL 18.6/pgvector 연결만 담당합니다.
fixture 데이터는 이 모듈을 호출하지 않도록 실습의 명시적 mode로 구분합니다.
"""
from __future__ import annotations
from pathlib import Path
from .data import TABLE_NAME, E5_MODEL_ID, DIMS

ENV_NAMES=('PGHOST','PGPORT','PGDATABASE','PGUSER','PGPASSWORD')
TABLE_SQL="""CREATE TABLE IF NOT EXISTS day23_search_docs (
    id integer PRIMARY KEY,
    title text NOT NULL,
    content text NOT NULL,
    category text NOT NULL,
    source_version text NOT NULL,
    embedding_model text NOT NULL,
    embedding vector(384) NOT NULL
)"""
UPSERT_SQL="""INSERT INTO day23_search_docs
(id,title,content,category,source_version,embedding_model,embedding)
VALUES (%s,%s,%s,%s,%s,%s,%s)
ON CONFLICT (id) DO UPDATE SET title=EXCLUDED.title,
  content=EXCLUDED.content,category=EXCLUDED.category,
  source_version=EXCLUDED.source_version,
  embedding_model=EXCLUDED.embedding_model,embedding=EXCLUDED.embedding"""
SQL_TOPK="""SELECT id,title,content,category,source_version,
     embedding_model,embedding <=> %s AS distance
FROM day23_search_docs WHERE embedding_model=%s
ORDER BY embedding <=> %s ASC LIMIT %s"""
SQL_CATEGORY="""SELECT id,title,content,category,source_version,
     embedding_model,embedding <=> %s AS distance
FROM day23_search_docs
WHERE embedding_model=%s AND category=%s
ORDER BY embedding <=> %s ASC LIMIT %s"""
HNSW_SQL="""CREATE INDEX IF NOT EXISTS day23_search_docs_hnsw
ON day23_search_docs USING hnsw (embedding vector_cosine_ops)"""

def connect_db(env_path):
    """실습 실행파일 옆 .env만 읽음. OS의 다른 DB 비밀번호를 섞지 않음."""
    from dotenv import dotenv_values
    import psycopg
    from pgvector.psycopg import register_vector
    path=Path(env_path)
    if not path.is_file():raise FileNotFoundError(f'{path} 파일이 없습니다. .env.example을 복사하세요.')
    cfg=dotenv_values(path,encoding='utf-8-sig',interpolate=False)
    missing=[k for k in ENV_NAMES if not cfg.get(k) or str(cfg[k]).strip() in {'본인_DB계정','본인_DB비밀번호'}]
    if missing:raise ValueError('DB 환경 설정 누락: '+', '.join(missing))
    conn=psycopg.connect(host=cfg['PGHOST'],port=int(cfg['PGPORT']),dbname=cfg['PGDATABASE'],user=cfg['PGUSER'],password=cfg['PGPASSWORD'],connect_timeout=8)
    try:register_vector(conn)
    except Exception:
        conn.close();raise
    return conn

def ensure_table(conn):
    conn.execute(TABLE_SQL)
    # 같은 이름의 기존 테이블이 있을 수 있으므로 타입·차원도 확인.
    found=conn.execute("""SELECT format_type(a.atttypid,a.atttypmod)
      FROM pg_attribute a WHERE a.attrelid='day23_search_docs'::regclass
      AND a.attname='embedding' AND NOT a.attisdropped""").fetchone()
    if not found or found[0]!='vector(384)':
        raise ValueError('day23_search_docs.embedding 은 vector(384)이어야 합니다')

def upsert_rows(conn,rows,vectors,model_id=E5_MODEL_ID):
    if model_id!=E5_MODEL_ID:raise ValueError('실제 DB에 모의/다른 모델 벡터를 저장하지 않습니다')
    if len(rows)!=len(vectors):raise ValueError('ID와 벡터의 행 개수가 다릅니다')
    for row,vec in zip(rows,vectors):
        conn.execute(UPSERT_SQL,(row['id'],row['title'],row['content'],row['category'],row['source_version'],model_id,vec))

def exact_topk(conn,qvec,k=3,category=None):
    if type(k) is not int or not (1<=k<=9):raise ValueError('k 범위 1~9')
    if category is not None and category not in {'course','development','support'}:raise ValueError('category 오류')
    if category is None:
        sql=SQL_TOPK; params=(qvec,E5_MODEL_ID,qvec,k)
    else:
        sql=SQL_CATEGORY;params=(qvec,E5_MODEL_ID,category,qvec,k)
    rows=conn.execute(sql,params).fetchall()
    return [dict(id=r[0],title=r[1],content=r[2],category=r[3],source_version=r[4],embedding_model=r[5],distance=float(r[6]),source_mode='pgvector_exact') for r in rows]

def check_data_ready(conn):
    exists=conn.execute("SELECT to_regclass('day23_search_docs')").fetchone()[0]
    if not exists:raise RuntimeError('실습 05 --mode live를 먼저 실행하여 검색 테이블과 문서 벡터를 저장하세요.')
    total=conn.execute('SELECT COUNT(*) FROM day23_search_docs WHERE embedding_model=%s',(E5_MODEL_ID,)).fetchone()[0]
    if total<9:raise RuntimeError(f'현재 검색 문서 {total}건. 실습 05 --mode live로 9건을 준비하세요.')
    return total
