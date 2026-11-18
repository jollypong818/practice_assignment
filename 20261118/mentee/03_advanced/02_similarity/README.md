# 실습 02 · Vector·Similarity·Distance — 심화

**HTML 대응:** `practice-2` · Embedding · pgvector 강의  2교시
**핵심 개념:** Dot·Cosine·L2
**TODO 개수:** 6개 · `app/` 안의 두 책임별 모듈

**HTML의 목표:** 영벡터·차원 불일치·NaN을 오류 원인별로 구분합니다.

## TODO 수행 순서

### 1. D23-02-A01 · `dot`

- 같은 위치의 숫자를 곱해 합산하는 내적을 구현하세요.
- 예: (1,0)·(0.8,0.6)=0.8. 입력 NumPy 배열 2개, 출력 float.

### 2. D23-02-A02 · `cosine`

- 내적을 두 벡터 길이의 곱으로 나누어 Cosine similarity를 구하세요.
- q=(1,0), A=(0.8,0.6)라면 0.8입니다.
- 입력: NumPy 배열 2개. 출력: float. 영벡터는 무조건 거부합니다.

### 3. D23-02-A03 · `l2`

- 두 벡터의 좌표 차이로 L2 거리를 구하세요. 출력 float.
- q=(1,0), A=(0.8,0.6) → sqrt(0.4) ≈ 0.6325.

### 4. D23-02-A04 · `normalize`

- 임의 벡터 a를 길이가 1인 단위 벡터로 변환하세요.
- 기존 배열을 직접 변경하지 않습니다. 영벡터는 ValueError.

### 5. D23-02-A05 · `rank_dot_vs_cosine`

- 후보 {이름:벡터}를 Dot 내림차순과 Cosine 내림차순으로 각각 정렬하세요.
- 결과: {'dot':[이름...], 'cosine':[이름...]}.
- 크기가 큰 벡터가 Dot 순위를 바꿀 수 있음을 확인합니다.

### 6. D23-02-A06 · `validate_pair`

- 배열 1차원·shape 일치·유한값·영벡터 여부를 검증하세요.
- 각각 dimension_mismatch, nonfinite, zero_vector ValueError로 구분합니다.
- 양쪽 입력이 올바르면 True.

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
