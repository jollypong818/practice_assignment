"""Day27 전용 DB. 역할·준비 상태·버전 조건을 SQL에서 적용하는 최소 안전 실습."""
from coursekit.config import schema_name
PURPOSE='day27-query-rerank-v1'
CATEGORIES={'학사','시설','지원'}


def validate_args(category,k,role):
    if category not in CATEGORIES:raise ValueError('category: 학사·시설·지원')
    if role not in ('learner','staff'):raise ValueError('invalid trusted principal role')
    if type(k) is not int or not 1<=k<=20:raise ValueError('candidate_k: 1~20')


def read_meta(conn):
    from psycopg import sql
    schema=schema_name()
    names=sql.Identifier(schema,'rag_meta')
    return dict(conn.execute(sql.SQL('SELECT key,value FROM {}').format(names)).fetchall())


def check_meta(conn,contract):
    meta=read_meta(conn)
    if meta.get('purpose')!=PURPOSE:raise RuntimeError('Day27 전용 Schema 목적 표식 불일치')
    if meta.get('embedding_contract')!=contract:
        raise RuntimeError('DB 벡터와 E5 Contract 불일치. 새 d27_ Schema에 다시 Indexing 하세요.')


def prepare_schema(conn,contract):
    from psycopg import sql
    from psycopg.types.json import Jsonb
    schema=schema_name()
    existing=conn.execute('SELECT 1 FROM pg_catalog.pg_namespace WHERE nspname=%s',(schema,)).fetchone()
    if existing:
        marker=conn.execute('SELECT to_regclass(%s)',(f'{schema}.rag_meta',)).fetchone()[0]
        if marker is None:raise RuntimeError('기존 Schema에 표식이 없습니다. 새 d27_* 이름을 사용하세요.')
        check_meta(conn,contract)
    else:conn.execute(sql.SQL('CREATE SCHEMA {}').format(sql.Identifier(schema)))
    m=sql.Identifier(schema,'rag_meta'); d=sql.Identifier(schema,'rag_documents'); c=sql.Identifier(schema,'rag_chunks')
    conn.execute(sql.SQL('CREATE TABLE IF NOT EXISTS {} (key TEXT PRIMARY KEY,value JSONB NOT NULL)').format(m))
    conn.execute(sql.SQL('''CREATE TABLE IF NOT EXISTS {} (
      doc_id TEXT PRIMARY KEY, category TEXT NOT NULL, current_source_version TEXT,
      access_level TEXT NOT NULL CHECK(access_level IN ('public','staff')))''').format(d))
    conn.execute(sql.SQL('''CREATE TABLE IF NOT EXISTS {c} (
      citation_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
      chunk_id TEXT UNIQUE NOT NULL, doc_id TEXT NOT NULL REFERENCES {d}(doc_id),
      source_version TEXT NOT NULL, source_locator TEXT NOT NULL, title TEXT NOT NULL,
      body TEXT NOT NULL, embedding vector(384) NOT NULL, ready BOOLEAN NOT NULL,
      is_current BOOLEAN NOT NULL, embedding_revision TEXT NOT NULL)''').format(c=c,d=d))
    for key,value in [('purpose',PURPOSE),('embedding_contract',contract)]:
        conn.execute(sql.SQL('INSERT INTO {}(key,value) VALUES(%s,%s) ON CONFLICT(key) DO NOTHING').format(m),
                     (key,Jsonb(value)))
    return schema


def publish(conn,corpus,vectors,contract):
    """CALLER transaction 내부에서 전량 저장. 실패 시 전체 Rollback."""
    from psycopg import sql
    if not corpus or len(corpus)!=len(vectors):raise ValueError('corpus/vector 크기 불일치')
    schema=prepare_schema(conn,contract)
    docs=sql.Identifier(schema,'rag_documents'); chunks=sql.Identifier(schema,'rag_chunks')
    result=[]
    for row,v in zip(corpus,vectors):
        conn.execute(sql.SQL('''INSERT INTO {}(doc_id,category,current_source_version,access_level)
            VALUES(%s,%s,%s,%s) ON CONFLICT(doc_id) DO UPDATE SET
            category=EXCLUDED.category,current_source_version=EXCLUDED.current_source_version,
            access_level=EXCLUDED.access_level''').format(docs),
            (row['doc_id'],row['category'],row['source_version'],row['access_level']))
        citation=conn.execute(sql.SQL('''INSERT INTO {}(chunk_id,doc_id,source_version,
           source_locator,title,body,embedding,ready,is_current,embedding_revision)
           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
           ON CONFLICT(chunk_id) DO UPDATE SET
             doc_id=EXCLUDED.doc_id,source_version=EXCLUDED.source_version,
             source_locator=EXCLUDED.source_locator,title=EXCLUDED.title,
             body=EXCLUDED.body,embedding=EXCLUDED.embedding,ready=EXCLUDED.ready,
             is_current=EXCLUDED.is_current,embedding_revision=EXCLUDED.embedding_revision
           RETURNING citation_id''').format(chunks),
           (row['chunk_id'],row['doc_id'],row['source_version'],row['source_locator'],
            row['title'],row['body'],v,row['ready'],row['is_current'],contract['revision'])).fetchone()[0]
        result.append({'chunk_id':row['chunk_id'],'citation_id':citation})
    return result


def search_db(conn,vector,category,k,role,contract):
    from psycopg import sql
    validate_args(category,k,role)
    check_meta(conn,contract)
    schema=schema_name()
    q=sql.SQL('''SELECT c.citation_id,c.chunk_id,c.doc_id,c.source_version,c.source_locator,
        d.category,d.access_level,c.ready,c.is_current,c.title,c.body,
        c.embedding <=> %s AS cosine_distance
      FROM {c} c JOIN {d} d ON d.doc_id=c.doc_id
      WHERE d.category=%s AND c.ready=TRUE AND c.is_current=TRUE
        AND c.source_version=d.current_source_version
        AND (%s='staff' OR d.access_level='public')
        AND c.embedding_revision=%s
      ORDER BY cosine_distance ASC,c.chunk_id ASC LIMIT %s''').format(
           c=sql.Identifier(schema,'rag_chunks'),d=sql.Identifier(schema,'rag_documents'))
    rows=conn.execute(q,(vector,category,role,contract['revision'],k)).fetchall()
    keys=['citation_id','chunk_id','doc_id','source_version','source_locator','category',
          'access_level','ready','is_current','title','body','cosine_distance']
    return [dict(zip(keys,row)) for row in rows]
