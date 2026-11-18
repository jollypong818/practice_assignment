# 실습 04 · 서버 확장과 Python 연결 — 기본필수

**HTML 대응:** `practice-4` · Embedding · pgvector 강의  4교시
**핵심 개념:** Windows PostgreSQL 18.6/pgvector
**TODO 개수:** 3개 · `main.py`

**HTML의 목표:** pgAdmin에서 확장 제공 상태를 조회하고, 준비된 지침에 따라 활성화·거리 계산을 확인합니다.

## TODO 수행 순서

### 1. D23-04-B01 · `sql_server_info`

- pgAdmin에서 실행할 서버 버전·현재 DB 조회 SQL을 작성하세요.
- 반드시 SELECT version()과 current_database()를 포함하세요.
- DB 변경이나 DROP/CREATE DATABASE는 하지 않습니다.

### 2. D23-04-B02 · `sql_extension_state`

- vector 확장의 제공 여부와 설치 여부를 확인하는 SQL 문자열을 작성하세요.
- pg_available_extensions, installed_version, WHERE name='vector' 사용.

### 3. D23-04-B03 · `sql_distance_probe`

- SQL에서 3차원 벡터 [1,0,0]과 [0,1,0]의 Cosine distance를 계산하세요.
- 문자열 반환. CAST는 ::vector, 연산자는 <=>를 사용합니다.
- 예상값 1.0이며 384차원 E5 출력이 아닙니다.

## 실행

```bash
python main.py --mode fixture
```

fixture는 흐름 확인용이며 실제 E5 임베딩·PostgreSQL 성공/품질을 의미하지 않습니다.

**pgvector 설치는 먼저** `../../docs/WINDOWS_PGVECTOR_SETUP.md`를 확인하세요. `python main.py`만 실행해서 Windows 서버 확장이 자동 설치되지는 않습니다.

실제 실행은 필요한 패키지와 선행 단계를 확인한 뒤 `python main.py --mode live`를 사용합니다.

실제 DB 모드는 `main.py` 옆 `.env.example`을 `.env`로 복사해 pgAdmin의 정확한 DB 계정으로 설정합니다.


## 예상 확인 항목 (정답 코드를 제공하지 않음)

- `outputs/exercise_04.json`이 생성되고 실습 번호·난이도·실행 출처가 구분됩니다.
- TODO가 미완성이면 `NotImplementedError`가 뜨는 것이 정상입니다.
- 값이 없는 경우를 성공값으로 임의 생성하거나, 모의 실행을 실측으로 기록하지 않습니다.
- 실습 목적과 수치 계산의 의미를 자신의 말로 설명합니다.

## 강사용 해설 순서

1. 첫 TODO에서 입력의 형식과 필수 정보를 검증하는 이유를 설명합니다.
2. 다음 TODO에서 핵심 연산·SQL 계약을 작은 예시로 적용합니다.
3. 출력 직전 데이터 ID·모델·실행 출처가 어떻게 유지되는지 설명합니다.
4. `fixture`로 코드 분기만 확인하고, `live`에서만 실제 E5/PostgreSQL의 성공을 인정합니다.
