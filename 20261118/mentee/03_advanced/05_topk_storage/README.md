# 실습 05 · 원문·벡터 저장과 Top-k — 심화

**HTML 대응:** `practice-5` · Embedding · pgvector 강의  5교시
**핵심 개념:** SQL·Metadata·거리
**TODO 개수:** 6개 · `app/` 안의 두 책임별 모듈

**HTML의 목표:** 중복·누락·원문 버전·쿼리 파라미터 순서를 검사합니다.

## TODO 수행 순서

### 1. D23-05-A01 · `schema_sql`

- 기존 knowledge 테이블을 건드리지 않는 day23_search_docs의 CREATE TABLE SQL을 작성하세요.
- 필드: id(PK),title,content,category,source_version,embedding_model,embedding vector(384).
- DROP/TRUNCATE를 사용하지 않습니다.

### 2. D23-05-A02 · `prepare_document_rows`

- 지식 101~109의 ID/제목/본문/분류/버전 및 passage 입력을 순서대로 묶으세요.
- 반환: [{'id', 'passage_input', ...}, ...]. 같은 ID를 새로 만들지 않습니다.

### 3. D23-05-A03 · `topk_sql`

- Cosine distance(<=>) 오름차순, k개 제한 SQL을 작성하세요.
- SELECT에 id,title,content,category,source_version,embedding_model,distance 포함.
- E5 외 다른 공간 혼합을 막도록 embedding_model을 필터합니다.

### 4. D23-05-A04 · `filtered_sql`

- category 필터가 포함된 Top-k SQL을 작성하세요.
- 쿼리 벡터와 category, 모델, k는 문자열 합치기가 아닌 %s 바인딩입니다.

### 5. D23-05-A05 · `check_search_options`

- k는 bool을 제외한 정수 1~9, category는 None 또는 course/development/support인지 검사하세요.
- 잘못된 값은 ValueError. 정상 시 {'k':k,'category':category} 반환.

### 6. D23-05-A06 · `check_id_vector_integrity`

- 지식 ID 중복·누락·벡터 행 수/차원/유한값/norm을 검사하세요.
- 기존 원문과 행 순서를 유지하며 정상일 때 True를 반환합니다.
- 실제 DB 저장 전 검증에 사용합니다.

## 실행

```bash
python main.py --mode fixture
```

fixture는 흐름 확인용이며 실제 E5 임베딩·PostgreSQL 성공/품질을 의미하지 않습니다.

실제 실행은 필요한 패키지와 선행 단계를 확인한 뒤 `python main.py --mode live`를 사용합니다.

실제 DB 모드는 `main.py` 옆 `.env.example`을 `.env`로 복사해 pgAdmin의 정확한 DB 계정으로 설정합니다.

**실제 DB 준비:** 04에서 vector 확장 활성화 → 05에서 9개 지식 실제 E5 임베딩 저장 → 06~08에서 해당 테이블 검색.


## 예상 확인 항목 (정답 코드를 제공하지 않음)

- `outputs/exercise_05.json`이 생성되고 실습 번호·난이도·실행 출처가 구분됩니다.
- TODO가 미완성이면 `NotImplementedError`가 뜨는 것이 정상입니다.
- 값이 없는 경우를 성공값으로 임의 생성하거나, 모의 실행을 실측으로 기록하지 않습니다.
- 실습 목적과 수치 계산의 의미를 자신의 말로 설명합니다.
