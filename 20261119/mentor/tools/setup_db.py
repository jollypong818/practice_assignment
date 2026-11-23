"""실제 DB에서 ingest_ 테이블만 생성합니다. 기존 테이블 DROP은 하지 않습니다.
사용법: python tools/setup_db.py --apply
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from coursekit.live import connect_db
from coursekit.db import initialize,use_schema,PRACTICE_SCHEMAS
if __name__=='__main__':
    if '--apply' not in sys.argv:
        print('실제 PostgreSQL에 연결하여 ingest_ 전용 테이블을 준비합니다.')
        print('실행: python tools/setup_db.py --apply')
        raise SystemExit(0)
    with connect_db() as conn:
        for scope in PRACTICE_SCHEMAS:
            use_schema(conn,scope)
            initialize(conn)
            print('Prepared schema:',scope)
        print('Current database:',conn.execute('SELECT current_database()').fetchone()[0])
        print('Extension:',conn.execute("SELECT extversion FROM pg_extension WHERE extname='vector'").fetchone()[0])
        print('Day24 ingest_ tables ready (other tables untouched)')
