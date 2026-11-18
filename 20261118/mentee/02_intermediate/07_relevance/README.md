# 실습 07 · 검색 결과 정성평가 — 응용

**HTML 대응:** `practice-7` · Embedding · pgvector 강의  7교시
**핵심 개념:** 관련성·정보 부족·정상 0건
**TODO 개수:** 5개 · `tasks.py`

**HTML의 목표:** k와 분류 조건을 바꾸고 결과·관련성 변화를 설명합니다.

## TODO 수행 순서

### 1. D23-07-I01 · `make_casebook`

- 강의의 질문 3종과 확인할 지식 ID를 구성하세요.
- server(102), retention(101: 보관 기간 없음), error(103/108).
- 자동 생성한 정답이 아니라 사람이 평가할 고정 기준 샘플임을 표시합니다.

### 2. D23-07-I02 · `judge_training_reference`

- 교안에 미리 주어진 원문 근거로 관련/부분 관련/무관을 수동 기준표로 판정하세요.
- server:102 관련,106 부분 관련. retention:101 부분 관련(기간 없음).
- error:103,108 관련. 그 밖에는 무관.
- *이 표는 사람이 만든 교육용 기준이며 모델 검색 평가점수가 아닙니다.*

### 3. D23-07-I03 · `make_review_row`

- 질문 ID·검색된 ID·본문·거리·교재 기준 라벨을 한 행으로 만드세요.
- distance는 정답 확률로 표현하지 않습니다.
- human_reviewed는 False로 두어 실제 수강생의 근거 검토 전임을 표시합니다.

### 4. D23-07-I04 · `classify_search_state`

- 데이터베이스 예외(error)는 error, 정상 조회 결과 []는 empty,
- 후보가 있으면 candidates를 반환하세요. 결과 없음과 DB 장애를 섞지 마세요.

### 5. D23-07-I05 · `review_filter_effect`

- 필터 전후 ID 목록을 비교해 빠진 ID와 추가된 ID를 반환하세요.
- 출력 {'removed': [...], 'added': [...]} 정렬된 목록.
- 필터 때문에 k보다 적게 반환될 수 있습니다.

## 실행

```bash
python main.py --mode fixture
```

fixture는 흐름 확인용이며 실제 E5 임베딩·PostgreSQL 성공/품질을 의미하지 않습니다.

실제 실행은 필요한 패키지와 선행 단계를 확인한 뒤 `python main.py --mode live`를 사용합니다.

실제 DB 모드는 `main.py` 옆 `.env.example`을 `.env`로 복사해 pgAdmin의 정확한 DB 계정으로 설정합니다.

**실제 DB 준비:** 04에서 vector 확장 활성화 → 05에서 9개 지식 실제 E5 임베딩 저장 → 06~08에서 해당 테이블 검색.

정성평가의 `teaching_reference`는 사람이 미리 만든 기준입니다. 이 필드는 검색 모델의 실측 성능이나 사람이 이번에 직접 평가했다는 증거가 아닙니다.


## 예상 확인 항목 (정답 코드를 제공하지 않음)

- `outputs/exercise_07.json`이 생성되고 실습 번호·난이도·실행 출처가 구분됩니다.
- TODO가 미완성이면 `NotImplementedError`가 뜨는 것이 정상입니다.
- 값이 없는 경우를 성공값으로 임의 생성하거나, 모의 실행을 실측으로 기록하지 않습니다.
- 실습 목적과 수치 계산의 의미를 자신의 말로 설명합니다.
