# 실습 06 · Exact·HNSW·EXPLAIN — 응용

**HTML 대응:** `practice-6` · Embedding · pgvector 강의  6교시
**핵심 개념:** 인덱스·플래너
**TODO 개수:** 5개 · `tasks.py`

**HTML의 목표:** 인덱스를 만들고 EXPLAIN으로 실제 Scan 종류를 확인합니다.

## TODO 수행 순서

### 1. D23-06-I01 · `create_index_sql`

- day23_search_docs.embedding의 Cosine HNSW 인덱스를 정의하세요.
- USING hnsw (embedding vector_cosine_ops)를 사용합니다.
- 인덱스는 선택 항목이며 9건에서 빠른 성능을 보장하지 않습니다.

### 2. D23-06-I02 · `explain_sql`

- SELECT id FROM day23_search_docs를 거리순으로 검색하는
- EXPLAIN (ANALYZE, BUFFERS) SQL을 작성하세요. 바인딩은 %s 두 개.
- 인덱스 사용 여부를 임의로 주장하면 안 됩니다.

### 3. D23-06-I03 · `read_scan_type`

- PostgreSQL EXPLAIN 텍스트에서 Index Scan / Seq Scan / 기타를 구분하세요.
- 계획이 없으면 unknown, index가 있으면 index, seq면 seq로 반환합니다.
- 작은 9건 테이블에서 Seq Scan은 오류가 아닙니다.

### 4. D23-06-I04 · `check_operator_compatibility`

- SQL이 cosine <=> 를 사용하면 vector_cosine_ops가 맞는지 검사하세요.
- 불일치 시 ValueError, 정상 시 True.
- L2 / negative inner product와 혼동하지 않습니다.

### 5. D23-06-I05 · `compare_topk`

- Exact Top-k와 ANN Top-k의 ID 집합 일치율을 계산하세요.
- 겹치는 ID 수 / exact_ids 수. 빈 exact_ids는 None.
- 인덱스 속도나 모델 품질을 만들어 내면 안 됩니다.

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

## 강사용 해설 순서

1. 첫 TODO에서 입력의 형식과 필수 정보를 검증하는 이유를 설명합니다.
2. 다음 TODO에서 핵심 연산·SQL 계약을 작은 예시로 적용합니다.
3. 출력 직전 데이터 ID·모델·실행 출처가 어떻게 유지되는지 설명합니다.
4. `fixture`로 코드 분기만 확인하고, `live`에서만 실제 E5/PostgreSQL의 성공을 인정합니다.
