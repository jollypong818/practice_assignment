# 실습 06 · Exact·HNSW·EXPLAIN — 기본필수

**HTML 대응:** `practice-6` · Embedding · pgvector 강의  6교시
**핵심 개념:** 인덱스·플래너
**TODO 개수:** 3개 · `main.py`

**HTML의 목표:** Exact Search와 HNSW의 원리·정렬·한계를 말로 설명합니다.

## TODO 수행 순서

### 1. D23-06-B01 · `create_index_sql`

- day23_search_docs.embedding의 Cosine HNSW 인덱스를 정의하세요.
- USING hnsw (embedding vector_cosine_ops)를 사용합니다.
- 인덱스는 선택 항목이며 9건에서 빠른 성능을 보장하지 않습니다.

### 2. D23-06-B02 · `explain_sql`

- SELECT id FROM day23_search_docs를 거리순으로 검색하는
- EXPLAIN (ANALYZE, BUFFERS) SQL을 작성하세요. 바인딩은 %s 두 개.
- 인덱스 사용 여부를 임의로 주장하면 안 됩니다.

### 3. D23-06-B03 · `read_scan_type`

- PostgreSQL EXPLAIN 텍스트에서 Index Scan / Seq Scan / 기타를 구분하세요.
- 계획이 없으면 unknown, index가 있으면 index, seq면 seq로 반환합니다.
- 작은 9건 테이블에서 Seq Scan은 오류가 아닙니다.

## 실행

```bash
python main.py --mode fixture
```

fixture는 흐름 확인용이며 실제 E5 임베딩·PostgreSQL 성공/품질을 의미하지 않습니다.

실제 실행은 필요한 패키지와 선행 단계를 확인한 뒤 `python main.py --mode live`를 사용합니다.

실제 DB 모드는 `main.py` 옆 `.env.example`을 `.env`로 복사해 pgAdmin의 정확한 DB 계정으로 설정합니다.

**실제 DB 준비:** 04에서 vector 확장 활성화 → 05에서 9개 지식 실제 E5 임베딩 저장 → 06~08에서 해당 테이블 검색.

HNSW를 실제 만들려면 `python main.py --mode live --create-index`로 **명시적** 실행해야 합니다. 9건의 작은 데이터에서 Seq Scan이어도 정상입니다.


## 예상 확인 항목 (정답 코드를 제공하지 않음)

- `outputs/exercise_06.json`이 생성되고 실습 번호·난이도·실행 출처가 구분됩니다.
- TODO가 미완성이면 `NotImplementedError`가 뜨는 것이 정상입니다.
- 값이 없는 경우를 성공값으로 임의 생성하거나, 모의 실행을 실측으로 기록하지 않습니다.
- 실습 목적과 수치 계산의 의미를 자신의 말로 설명합니다.
