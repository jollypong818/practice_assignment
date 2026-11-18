# 실습 08 · AI Agent용 Retriever — 기본필수

**HTML 대응:** `practice-8` · Embedding · pgvector 강의  8교시
**핵심 개념:** 질문 → 후보 ID·원문
**TODO 개수:** 3개 · `main.py`

**HTML의 목표:** 질문 하나로 Embedding·Top-k·원문 출력까지 연결하고 설명합니다.

## TODO 수행 순서

### 1. D23-08-B01 · `validate_question`

- 질문은 1자 이상의 문자열이어야 하며 앞뒤 공백을 제거하세요.
- 빈 값/공백만 있는 값이면 ValueError. 반환은 정리된 질문.
- API가 연결되어 있지 않아도 검사 가능한 순수 함수입니다.

### 2. D23-08-B02 · `retrieve_candidates`

- fixture면 교육용 fixture_search, live면 E5 query Embedding → pgvector Exact SQL을 사용하세요.
- 실제 live는 exercise05에서 9개 자료를 먼저 저장해야 합니다.
- DB 연결 실패를 빈 결과 []로 바꾸지 말고 예외를 전달하세요.

### 3. D23-08-B03 · `format_candidates`

- 후보의 id/title/content/category/source_version/distance를 반환하세요.
- 검색된 원문을 요약·변조하지 않고, distance는 숫자 그대로 둡니다.
- 답변 상태(answered)를 자동으로 부여하지 마세요.

## 실행

```bash
python main.py --mode fixture
```

fixture는 흐름 확인용이며 실제 E5 임베딩·PostgreSQL 성공/품질을 의미하지 않습니다.

실제 실행은 필요한 패키지와 선행 단계를 확인한 뒤 `python main.py --mode live`를 사용합니다.

실제 DB 모드는 `main.py` 옆 `.env.example`을 `.env`로 복사해 pgAdmin의 정확한 DB 계정으로 설정합니다.

**실제 DB 준비:** 04에서 vector 확장 활성화 → 05에서 9개 지식 실제 E5 임베딩 저장 → 06~08에서 해당 테이블 검색.

**최종 출력 범위**: `retrieved`의 ID·title·content·category·source_version·distance. GPT API 호출은 이번 실습의 필수 목표가 아닙니다.


## 예상 확인 항목 (정답 코드를 제공하지 않음)

- `outputs/exercise_08.json`이 생성되고 실습 번호·난이도·실행 출처가 구분됩니다.
- TODO가 미완성이면 `NotImplementedError`가 뜨는 것이 정상입니다.
- 값이 없는 경우를 성공값으로 임의 생성하거나, 모의 실행을 실측으로 기록하지 않습니다.
- 실습 목적과 수치 계산의 의미를 자신의 말로 설명합니다.

## 강사용 해설 순서

1. 첫 TODO에서 입력의 형식과 필수 정보를 검증하는 이유를 설명합니다.
2. 다음 TODO에서 핵심 연산·SQL 계약을 작은 예시로 적용합니다.
3. 출력 직전 데이터 ID·모델·실행 출처가 어떻게 유지되는지 설명합니다.
4. `fixture`로 코드 분기만 확인하고, `live`에서만 실제 E5/PostgreSQL의 성공을 인정합니다.
