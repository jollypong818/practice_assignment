# 실습 01 · 검색 대상과 ID — 응용

**HTML 대응:** `practice-1` · Embedding · pgvector 강의  1교시
**핵심 개념:** Embedding 입력과 기존 지식 보존
**TODO 개수:** 5개 · `tasks.py`

**HTML의 목표:** 새 가상 지식 104~109를 포함해 중복 ID·누락된 본문을 점검합니다.

## TODO 수행 순서

### 1. D23-01-I01 · `select_original`

- 기존 수업에서 사용한 101·102·103만 ID 오름차순으로 선택합니다.
- 입력: 전체 지식 목록(list[dict]). 출력: 원래 지식 3개를 담은 list.
- 원본 딕셔너리의 id/title/content를 수정하지 마세요.
- 개념: 원문 ID 고정·검색할 자료의 범위.

### 2. D23-01-I02 · `make_passage_input`

- E5 문서 입력 텍스트를 "passage: 제목 본문" 형식으로 만드세요.
- 입력: 지식 한 행. 출력: 문자열. 제목과 본문을 공백 하나로 구분하세요.
- 개념: FAQ 질문과 달리 지식 본문을 검색 대상으로 사용합니다.

### 3. D23-01-I03 · `make_mapping`

- 각 지식의 id/title/content/category/source_version 및 passage_input을 기록하세요.
- 입력: 선택된 지식 목록. 출력: 딕셔너리 목록.
- 개념: 벡터를 생성하기 전에도 원문·ID·버전을 추적해야 합니다.

### 4. D23-01-I04 · `reject_duplicate_ids`

- 모든 9개 지식의 ID 중복 여부를 점검하고 중복이면 ValueError를 내세요.
- 단순 len만 비교하지 말고 id의 타입이 int(True 제외)인지도 확인합니다.
- 출력: 중복이 없으면 실제 ID 집합(set).

### 5. D23-01-I05 · `reject_missing_fields`

- title/content/category/source_version의 누락 또는 공백 문자열을 거부하세요.
- 입력: 전체 지식 목록. 정상 출력: True. 잘못된 항목은 ValueError.
- 개념: 잘못된 원문은 정상적인 Embedding 입력이 될 수 없습니다.

## 실행

```bash
python main.py --mode fixture
```

fixture는 흐름 확인용이며 실제 E5 임베딩·PostgreSQL 성공/품질을 의미하지 않습니다.


## 예상 확인 항목 (정답 코드를 제공하지 않음)

- `outputs/exercise_01.json`이 생성되고 실습 번호·난이도·실행 출처가 구분됩니다.
- TODO가 미완성이면 `NotImplementedError`가 뜨는 것이 정상입니다.
- 값이 없는 경우를 성공값으로 임의 생성하거나, 모의 실행을 실측으로 기록하지 않습니다.
- 실습 목적과 수치 계산의 의미를 자신의 말로 설명합니다.
