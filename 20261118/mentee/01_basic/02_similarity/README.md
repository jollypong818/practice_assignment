# 실습 02 · Vector·Similarity·Distance — 기본필수

**HTML 대응:** `practice-2` · Embedding · pgvector 강의  2교시
**핵심 개념:** Dot·Cosine·L2
**TODO 개수:** 3개 · `main.py`

**HTML의 목표:** (1,0)과 (0.8,0.6)의 내적·Cosine·L2를 직접 계산합니다.

## TODO 수행 순서

### 1. D23-02-B01 · `dot`

- 같은 위치의 숫자를 곱해 합산하는 내적을 구현하세요.
- 예: (1,0)·(0.8,0.6)=0.8. 입력 NumPy 배열 2개, 출력 float.

### 2. D23-02-B02 · `cosine`

- 내적을 두 벡터 길이의 곱으로 나누어 Cosine similarity를 구하세요.
- q=(1,0), A=(0.8,0.6)라면 0.8입니다.
- 입력: NumPy 배열 2개. 출력: float. 영벡터는 무조건 거부합니다.

### 3. D23-02-B03 · `l2`

- 두 벡터의 좌표 차이로 L2 거리를 구하세요. 출력 float.
- q=(1,0), A=(0.8,0.6) → sqrt(0.4) ≈ 0.6325.

## 실행

```bash
python main.py --mode fixture
```

fixture는 흐름 확인용이며 실제 E5 임베딩·PostgreSQL 성공/품질을 의미하지 않습니다.


## 예상 확인 항목 (정답 코드를 제공하지 않음)

- `outputs/exercise_02.json`이 생성되고 실습 번호·난이도·실행 출처가 구분됩니다.
- TODO가 미완성이면 `NotImplementedError`가 뜨는 것이 정상입니다.
- 값이 없는 경우를 성공값으로 임의 생성하거나, 모의 실행을 실측으로 기록하지 않습니다.
- 실습 목적과 수치 계산의 의미를 자신의 말로 설명합니다.
