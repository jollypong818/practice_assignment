"""Windows 11 · PostgreSQL 18 · pgvector 설치 확인용, 데이터 수정 없음."""
from pathlib import Path
import psycopg
from dotenv import dotenv_values
from pgvector import Vector
from pgvector.psycopg import register_vector

# .env는 현재 파이썬 파일과 같은 폴더에서만 읽습니다.
cfg = dotenv_values(Path(__file__).with_name(".env"), interpolate=False)
required = ("PGHOST", "PGPORT", "PGDATABASE", "PGUSER", "PGPASSWORD")
missing = [key for key in required if not cfg.get(key)]
if missing:
    raise RuntimeError(".env 설정 누락: " + ", ".join(missing))

with psycopg.connect(
    host=cfg["PGHOST"],
    port=int(cfg["PGPORT"]),
    dbname=cfg["PGDATABASE"],
    user=cfg["PGUSER"],
    password=cfg["PGPASSWORD"],
) as conn:
    # 중요: PostgreSQL 연결마다 vector 타입을 등록합니다.
    register_vector(conn)

    q = Vector([1.0, 0.0, 0.0])
    database, dimensions, distance = conn.execute(
        "SELECT current_database(), vector_dims(%s::vector), "
        "%s::vector <=> %s::vector",
        (q, q, q),
    ).fetchone()

    assert dimensions == 3, f"잘못된 차원: {dimensions}"
    assert abs(float(distance)) < 1e-6, f"잘못된 거리: {distance}"
    print("연결 DB:", database)
    print("벡터 차원:", dimensions)
    print("자기 자신과의 코사인 거리:", distance)
    print("DB 연결 및 pgvector 확인 완료")