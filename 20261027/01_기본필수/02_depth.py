"""실습 02: 깊이만 바꾸고 같은 train·valid에서 비교합니다."""
# 파일경로를 다루기 위한 파이썬 표준 라이브러리
# 현재 실행 위치가 아니라 "이 파이썬 파일이 있는 위치"를 기준으로 requests.csv 를 찾기위해 사용한다. 
from pathlib import Path
# CSV데이터를 읽고 표(dataframe) 형태로 다루기 위한 라이브러리
import pandas as pd
# 데이터를 학습용(train), 검증용(valid), 테스트용(test)으로 나누기 위해 사용하는 함수
from sklearn.model_selection import train_test_split

# __file__ : 현재 실행 중인 파이썬 파일의 경로
# resolve() : 절대경로로 변환
# parent : 현재 파이썬 파일이 들어있는 폴더
#
# 즉 HERE에는 "현재 이 코드 파일이 있는 폴더"의 경로가 들어간다.
# 이렇게 하면 터미널을 어느 폴더에서 실행하더라도 requests.csv를 안정적으로 찾을 수 있다.
HERE = Path(__file__).resolve().parent

# 현재 파이썬 파일과 같은 폴더에 있는 requests.csv를 읽는다.
# 읽은 CSV 데이터는 pandas의 DataFrame 형태로 raw에 저장된다.
raw = pd.read_csv(HERE / "requests.csv")

# 전체 데이터를 develop(개발용 데이터)과 test(최종 테스트 데이터)로 나눈다.
#
# test_size=0.2
# → 전체 데이터의 20%를 test로 사용
# → 나머지 80%는 develop에 저장
#
# stratify=raw["failed"]
# → failed의 0/1 비율이 develop과 test에서도 최대한 비슷하게 유지되도록 나눈다.
#
# random_state=42
# → 실행할 때마다 랜덤하게 다른 결과가 나오지 않고 항상 같은 방식으로 데이터가 나뉘도록 고정한다.
develop, test = train_test_split(raw, test_size=0.2, stratify=raw["failed"], random_state=42)



# develop 데이터를 다시 train과 valid로 나눈다.
#
# develop은 원래 전체 데이터의 80%이다.
# 여기서 25%를 valid로 가져가므로:
#
# 전체 기준
# train = 60%
# valid = 20%
# test  = 20%
#
# train : 모델을 실제로 학습시키는 데이터
# valid : 어떤 모델/설정이 좋은지 비교하는 데이터
# test  : 최종 모델의 성능을 확인할 때 사용하는 데이터
train, valid = train_test_split(develop, test_size=0.25, stratify=develop["failed"], random_state=42)
# test 4건은 보관만 합니다. 입력은 실행 전에 아는 글자 수입니다.'
# ---------------------------
# 입력 데이터(X)와 정답(y) 분리
# ---------------------------

# 모델에게 입력으로 줄 데이터
# 여기서는 input_chars(입력 글자 수) 하나만 사용한다.
#
# [["input_chars"]]처럼 대괄호를 두 번 사용하는 이유는
# 머신러닝 모델의 입력 X를 2차원 형태로 만들기 위해서다.
X_train = train[["input_chars"]]
X_valid = valid[["input_chars"]]
# 모델이 맞혀야 하는 정답
# failed 값(예: 0=성공, 1=실패)을 사용한다.
y_train = train["failed"]
y_valid = valid["failed"]

# ---------------------------
# 머신러닝 모델과 평가 지표 준비
# ---------------------------
# Decision Tree(의사결정나무) 분류 모델
# input_chars를 기준으로 요청이 실패할지 성공할지를 분류한다.
from sklearn.tree import DecisionTreeClassifier
# 모델의 분류 성능을 평가하기 위한 F1 Score
from sklearn.metrics import f1_score

# ---------------------------
# 나무 깊이를 바꿔가며 실험
# -------------------------
# max_depth를 1과 3으로 각각 설정해서
# 어떤 깊이의 모델이 더 좋은지 비교한다.
for depth in [1, 3]:
    
    # 의사결정나무 모델 생성
    #
    # max_depth:
    # 나무가 얼마나 깊게 조건을 나눌 수 있는지를 제한한다.
    #
    # depth=1 → 매우 단순한 모델
    # depth=3 → 더 복잡한 규칙까지 학습할 수 있는 모델
    #
    # random_state=42는 실행할 때마다 결과가
    # 달라지는 것을 방지하기 위한 값이다.
    # TODO B02: 반복 중인 depth를 max_depth에 연결하세요.
    model = DecisionTreeClassifier(
        max_depth=depth,
        random_state=42
    )
    # 학습 데이터(X_train)와 정답(y_train)을 이용해서
    # 의사결정나무가 실패/성공을 구분하는 규칙을 학습한다.
    model.fit(X_train, y_train)


    # ---------------------------
    # 학습 데이터 성능 측정
    # ---------------------------

    # model.predict(X_train)
    # → 학습했던 데이터에 대해 모델이 정답을 예측한다.
    #
    # f1_score()
    # → 실제 정답(y_train)과 모델의 예측을 비교해서
    #   F1 점수를 계산한다.
    train_f1 = f1_score(y_train, model.predict(X_train), zero_division=0)


    # ---------------------------
    # 검증 데이터 성능 측정
    # ---------------------------

    # 이번에는 모델이 학습할 때 사용하지 않은 valid 데이터로 평가한다.
    #
    # 이 점수가 중요한 이유:
    # 학습 데이터만 잘 맞히는 게 아니라
    # 처음 보는 데이터도 잘 맞히는지를 확인할 수 있기 때문이다.
    valid_f1 = f1_score(y_valid, model.predict(X_valid), zero_division=0)
      # 깊이별 학습 성능과 검증 성능 출력
    # :.3f → 소수점 셋째 자리까지 출력
    print(f"깊이 {depth}: train F1={train_f1:.3f}, valid F1={valid_f1:.3f}")
