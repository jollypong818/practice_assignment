# 실습 03 · E5 문장 Embedding — 응용

**HTML 대응:** `practice-3` · Embedding · pgvector 강의  3교시
**핵심 개념:** query/passage·384차원
**TODO 개수:** 5개 · `tasks.py`

**HTML의 목표:** 지식 ID와 Embedding 행의 순서를 대조하고 query: / passage: 입력을 비교합니다.

## TODO 수행 순서

### 1. D23-03-I01 · `make_passages`

- 지식 목록을 E5 문서 입력 문자열 목록으로 변환하세요.
- 문서에는 'passage: ' + 제목 + ' ' + 본문을 사용합니다.
- 한 행마다 정확히 한 문자열을 만들어 순서를 유지하세요.

### 2. D23-03-I02 · `make_queries`

- 질문 목록 각 요소 앞에 query: 공백을 붙이세요.
- 출력: 입력과 동일한 순서의 문자열 리스트.
- 빈 질문을 추가해 그럴듯한 벡터를 만들지 마세요.

### 3. D23-03-I03 · `encode_both`

- 같은 Encoder에 문서와 질문을 나누어 encode하세요.
- 반드시 normalize_embeddings=True, convert_to_numpy=True를 전달합니다.
- 결과: (doc_vectors, query_vectors). 기본필수의 모의 모드와
- --mode live의 E5 실측을 구분하여 같은 API를 사용합니다.

### 4. D23-03-I04 · `verify_alignment`

- 지식 행 수와 벡터 행 수가 같은지 확인하고 [(ID,행번호),...]를 반환하세요.
- ID가 중복되어 있거나 행 수가 다르면 ValueError.
- 예: 지식 102는 vectors[1]과 짝입니다.

### 5. D23-03-I05 · `check_shapes_vectors`

- 문서 벡터 shape=(doc_count,384), 질문 shape=(1,384)를 검사하세요.
- 두 배열 모두 유한하고 길이가 1인지 검증합니다.
- 정상일 때 True, 오류일 때 ValueError.

## 실행

```bash
python main.py --mode fixture
```

fixture는 흐름 확인용이며 실제 E5 임베딩·PostgreSQL 성공/품질을 의미하지 않습니다.

실제 실행은 필요한 패키지와 선행 단계를 확인한 뒤 `python main.py --mode live`를 사용합니다.


## 예상 확인 항목 (정답 코드를 제공하지 않음)

- `outputs/exercise_03.json`이 생성되고 실습 번호·난이도·실행 출처가 구분됩니다.
- TODO가 미완성이면 `NotImplementedError`가 뜨는 것이 정상입니다.
- 값이 없는 경우를 성공값으로 임의 생성하거나, 모의 실행을 실측으로 기록하지 않습니다.
- 실습 목적과 수치 계산의 의미를 자신의 말로 설명합니다.
