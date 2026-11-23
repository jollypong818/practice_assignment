# PostgreSQL + pgvector 실습 계약

## 기존 데이터 보존

- PostgreSQL 18.6 (Windows 11)에 이미 설치된 DB를 사용합니다. Docker/WSL 불필요.
- DB 전체 초기화나 DROP은 수행하지 않습니다.
- 아래 네 실습 전용 Schema만 별도로 사용합니다: `d24_basic07`, `d24_inter07`, `d24_adv07`, `d24_adv08`.
- 모든 Schema 안에는 `ingest_documents`, `ingest_versions`, `ingest_chunks` 테이블이 있습니다.
- Schema 생성 권한은 별도 필요할 수 있습니다. 같은 PostgreSQL DB에 여러 학생이 같이 접근하는 경우 사용자별 Schema/DB 권한을 별도로 분리해야 합니다. 이 강의는 각 PC의 로컬 DB를 전제로 합니다.

## 실제 SQL 실행 위치

**pgAdmin Query Tool**: 아래 SQL은 확장 상태 확인용입니다.

```sql
SELECT current_database();
SELECT extname, extversion FROM pg_extension WHERE extname='vector';
CREATE EXTENSION IF NOT EXISTS vector; -- 아직 활성화되지 않았고 권한이 있을 경우
```

**Git Bash**: `python tools/setup_db.py --apply`로 실제 연결·Schema·Table 생성. `PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER`, `PGPASSWORD`는 `.env`에서 사용합니다.

`%s` Placeholder가 포함된 Python SQL 문자열은 pgAdmin에 그대로 붙여넣지 않습니다. Psycopg `cursor.execute(sql, params)`에서 각 값으로 전달합니다.

## DB 문서/버전/청크 관계

```text
ingest_documents  (doc_id PK, current_version, current_pipeline_version)
        │
        ├─ ingest_versions (doc_id, source_version, pipeline_version PK)
        │           │
        │           └─ status: staging / ready / failed
        │
        └─ ingest_chunks (citation_id bigint identity PK, chunk_id text unique)
                    └─ doc_id + source_version + pipeline_version → ingest_versions
                    └─ body / source_locator / char_start:end / embedding vector(384)
```

## 실행 정책

1. E5 모델 ID·revision·Tokenizer·`passage:`·Normalization 정책을 기록합니다.
2. 실제로 인코딩한 문자열의 Token 길이(특수 Token 포함)를 확인합니다.
3. 벡터 개수·차원·유한값·정규화를 검사합니다.
4. 새 원문/처리 버전을 Staging합니다. 기존 Ready 데이터는 덮어쓰지 않습니다.
5. 모든 Chunk가 들어왔는지 확인 후 현재 공개 포인터를 Transaction에서 전환합니다.
6. `source_version`과 `pipeline_version`을 **함께** 필터링한 정확 검색으로 확인합니다.
7. `citation_id`는 DB가 발급하는 양의 정수입니다. 설명용 예시의 `201`을 실제 DB ID로 가정하지 않습니다.

SQL의 `vector(384)`는 수치 크기를 검사하지만, 동일 Embedding 모델로 만든 벡터라는 사실까지 증명하지는 못합니다. 모델 공간을 변경할 때 기존 벡터와 혼합하지 마세요.
