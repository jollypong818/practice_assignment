
"""실습 07~08 기본필수: 같은 파일을 완성하고 다시 실행합니다."""


# pathlib는 Python에 기본 포함된 경로 처리 라이브러리이다.
# Path는 파일과 폴더의 경로를 다루는 데 사용한다.
from pathlib import Path

# pandas는 CSV 파일을 읽고 표 형태의 데이터를 처리하는 라이브러리이다.
import pandas as pd

# train_test_split은 데이터를 학습용과 평가용으로 분리한다.
from sklearn.model_selection import train_test_split


# -------------------------------------------------
# 1. CSV 파일 읽기
# -------------------------------------------------

# __file__은 현재 Python 파일의 경로이다.
# resolve()는 절대경로를 구한다.
# parent는 해당 파일이 위치한 폴더를 의미한다.
#
# 예: C:/workspace/practice/ex07.py
# HERE = C:/workspace/practice
HERE = Path(__file__).resolve().parent


# 현재 Python 파일과 같은 폴더에 있는 requests.csv를 읽는다.
#
# read_csv()는 CSV를 pandas DataFrame으로 변환한다.
# raw에는 전체 요청 데이터 20건이 저장된다.
raw = pd.read_csv(HERE / "requests.csv")


# -------------------------------------------------
# 2. Train / Valid / Test 데이터 분할
# -------------------------------------------------

# 전체 20건 중 20%를 test로 분리한다.
#
# develop = 16건
# test    = 4건
#
# random_state=42:
#   같은 데이터와 조건으로 실행할 때 동일하게 분할되도록 난수 시드를 고정한다.
#
# stratify=raw["failed"]:
#   성공(0)과 실패(1)의 비율을 가능한 한 유지하면서 분할한다.
develop, test = train_test_split(
    raw,
    test_size=0.2,
    random_state=42,
    stratify=raw["failed"]
)


# develop 16건 중 25%를 valid로 분리한다.
#
# train = 12건
# valid = 4건
#
# train은 모델 학습에 사용한다.
# valid는 모델의 성능 비교에 사용한다.
# test는 최종 평가를 위해 보관한다.
train, valid = train_test_split(
    develop,
    test_size=0.25,
    random_state=42,
    stratify=develop["failed"]
)


# -------------------------------------------------
# 3. 머신러닝 라이브러리 가져오기
# -------------------------------------------------

# ColumnTransformer는 열마다 서로 다른 전처리를 적용한다.
#
# 예:
# 숫자 열(input_chars) → StandardScaler
# 문자 열(task_type)  → OneHotEncoder
from sklearn.compose import ColumnTransformer


# StandardScaler:
#   숫자 데이터의 평균과 표준편차를 이용해 표준화한다.
#
# OneHotEncoder:
#   문자로 된 범주 데이터를 0과 1로 변환한다.
#
# 예: 작업 종류가 "요약", "분석", "생성"이라면
# "요약" → [1, 0, 0]
# "분석" → [0, 1, 0]
# "생성" → [0, 0, 1]
#
# 실제 열 순서는 학습 데이터에서 정해진 범주 순서에 따른다.
from sklearn.preprocessing import StandardScaler, OneHotEncoder


# Pipeline은 전처리와 머신러닝 모델을 하나로 연결한다.
#
# 예:
# 입력 데이터 → 전처리 → 모델 학습/예측
from sklearn.pipeline import Pipeline


# clone은 전처리 객체 등을 동일한 설정으로 새로 복제한다.
#
# 각 모델이 독립적인 전처리 객체를 사용하도록 만든다.
from sklearn.base import clone


# DummyRegressor:
#   기본적으로 학습 데이터 정답의 평균값을 예측한다.
#
# DummyClassifier:
#   지정한 단순한 규칙으로 클래스를 예측한다.
#
# 실제 모델이 이런 단순한 기준보다 좋은지 비교하기 위해 사용한다.
from sklearn.dummy import DummyRegressor, DummyClassifier


# LinearRegression:
#   입력과 숫자 정답 사이의 선형 관계를 학습하는 회귀 모델
#
# LogisticRegression:
#   입력으로부터 클래스별 확률을 계산하고 분류하는 모델
from sklearn.linear_model import LinearRegression, LogisticRegression


# mean_absolute_error:
#   회귀 예측의 평균 절대 오차(MAE)를 계산한다.
#
# f1_score:
#   분류 예측의 정밀도와 재현율을 함께 평가한다.
from sklearn.metrics import mean_absolute_error, f1_score


# -------------------------------------------------
# 4. 모델에 사용할 입력 특징 선택
# -------------------------------------------------

# features는 모델에 입력할 열 이름을 지정한다.
#
# input_chars = AI 요청의 글자 수 (숫자)
# task_type   = AI 작업 종류 (문자/범주)
#
# elapsed_ms와 failed는 예측하려는 정답이므로 입력 특징에 포함하지 않는다.
#
# 정답을 입력에 포함하면 데이터 누수가 발생할 수 있다.
features = ["input_chars", "task_type"]


# 학습 데이터에서 두 입력 열을 선택한다.
#
# X_train에는 input_chars와 task_type만 저장된다.
X_train = train[features]


# 검증 데이터에서도 같은 두 열을 선택한다.
#
# 학습에 사용하지 않은 데이터로 모델을 평가하기 위해 사용한다.
X_valid = valid[features]


# -------------------------------------------------
# 5. 열마다 서로 다른 전처리 설정
# -------------------------------------------------

# ColumnTransformer는 데이터의 열마다 서로 다른 전처리 방법을 적용할 수 있게 해준다.
#
# ("num", StandardScaler(), ["input_chars"])
#   "num"은 이 전처리 단계의 이름이다.
#   input_chars 숫자 열을 표준화한다.
#
# ("cat", OneHotEncoder(...), ["task_type"])
#   "cat"은 이 전처리 단계의 이름이다.
#   task_type 문자 열을 원-핫 인코딩한다.
#
# sparse_output=False:
#   원-핫 인코딩 결과를 일반적인 밀집 배열로 반환한다.
#
# 예를 들어 입력이 다음과 같다면
# input_chars = 500
# task_type = "요약"
#
# 전처리 후에는
# [표준화된 글자 수, 1, 0, 0] 같은 숫자 배열이 된다.
#
# 주의:
# 실제 변환된 열의 개수와 순서는 학습 데이터에 따라 달라진다.
pre = ColumnTransformer([
    ("num", StandardScaler(), ["input_chars"]),
    ("cat", OneHotEncoder(sparse_output=False), ["task_type"]),
])


# -------------------------------------------------
# 6. 평가 결과를 저장할 변수 준비
# -------------------------------------------------

# 회귀 모델별 MAE를 저장할 리스트이다.
#
# 예:
# [
#   {"model": "Dummy", "MAE_ms": 300},
#   {"model": "Linear", "MAE_ms": 120}
# ]
regression_rows = []


# 분류 모델별 F1 Score를 저장할 리스트이다.
#
# 예:
# [
#   {"model": "Dummy", "F1": 0.0},
#   {"model": "Logistic", "F1": 0.667}
# ]
classification_rows = []


# valid에서 요청 ID와 실제 정답을 복사한다.
#
# request_id = 요청 식별자
# elapsed_ms = 실제 실행시간
# failed     = 실제 실패 여부
#
# 여기에 모델별 예측 결과를 새로운 열로 추가할 예정이다.
#
# copy()는 원본 valid와 별도의 DataFrame을 만든다.
result = valid[["request_id", "elapsed_ms", "failed"]].copy()


# -------------------------------------------------
# 7. 회귀 모델 비교: 실행시간 예측
# -------------------------------------------------

# 두 모델을 차례로 실행한다.
#
# 첫 번째 반복:
# name = "Dummy"
# estimator = DummyRegressor()
#
# 두 번째 반복:
# name = "Linear"
# estimator = LinearRegression()
#
# 같은 데이터로 비교하므로
# 어떤 모델이 실행시간을 더 잘 예측하는지 확인할 수 있다.
for name, estimator in [
    ("Dummy", DummyRegressor()),
    ("Linear", LinearRegression())
]:

    # 전처리와 회귀 모델을 하나의 Pipeline으로 연결한다.
    #
    # ("pre", clone(pre)):
    #   숫자 표준화와 문자 원-핫 인코딩을 수행한다.
    #   clone(pre)는 같은 설정의 새 전처리 객체를 만든다.
    #
    # ("model", estimator):
    #   현재 반복에서 선택한 회귀 모델을 사용한다.
    model = Pipeline([
        ("pre", clone(pre)),
        ("model", estimator)
    ])

    # 모델을 학습한다.
    #
    # X_train = 글자 수와 작업 종류 (입력)
    # train["elapsed_ms"] = 실제 실행시간 (정답)
    #
    # Pipeline 내부에서:
    # 1. input_chars의 평균/표준편차를 train으로 계산
    # 2. task_type의 범주를 train으로 학습
    # 3. 입력 데이터를 숫자 형태로 변환
    # 4. 변환된 데이터로 회귀 모델을 학습
    model.fit(X_train, train["elapsed_ms"])

    # 학습한 모델로 valid의 실행시간을 예측한다.
    #
    # Pipeline은 valid에도 train에서 정한 전처리 기준을 그대로 적용한다.
    #
    # prediction에는 valid 4건의 예측 실행시간이 저장된다.
    prediction = model.predict(X_valid)

    # 회귀 모델의 예측 오차를 계산하여 리스트에 추가한다.
    #
    # valid["elapsed_ms"] = 실제 실행시간
    # prediction = 예측 실행시간
    #
    # MAE는 예측값과 실제값의 차이의 절댓값을 평균 낸 것이다. 
    # MAE가 낮을수록 실제 실행시간에 가깝게 예측한 것이다.
    regression_rows.append({
        "model": name,
        "MAE_ms": mean_absolute_error(
            valid["elapsed_ms"],
            prediction
        )
    })

    # 모델의 예측 결과를 result DataFrame에 추가한다.
    #
    # name이 "Dummy"이면 "Dummy_ms" 열 생성
    # name이 "Linear"이면 "Linear_ms" 열 생성
    #
    # 나중에 실제 실행시간과 모델별 예측값을 CSV 파일에서 비교할 수 있다.
    result[name + "_ms"] = prediction


# -------------------------------------------------
# 8. 분류 모델 비교: 실패 여부 예측
# -------------------------------------------------

# 이번에는 실행시간이 아니라 실패 여부를 예측한다.
#
# DummyClassifier(strategy="most_frequent"):
#   train에서 가장 자주 등장한 클래스를 예측한다.
#
# LogisticRegression(max_iter=1000):
#   로지스틱 회귀 모델을 사용한다.
#   max_iter=1000은 최적화 반복 횟수의 상한이다.
#   학습이 수렴할 기회를 충분히 주기 위해 설정한다.
for name, estimator in [
    ("Dummy", DummyClassifier(strategy="most_frequent")),
    ("Logistic", LogisticRegression(max_iter=1000))
]:

    # 회귀와 동일한 전처리 과정을 사용한다.
    #
    # 다만 마지막 단계에 회귀 모델 대신 분류 모델이 들어간다.
    model = Pipeline([
        ("pre", clone(pre)),
        ("model", estimator)
    ])

    # 분류 모델을 학습한다.
    #
    # X_train = 글자 수와 작업 종류 (입력)
    # train["failed"] = 실제 실패 여부 (정답)
    #
    # failed가 0이면 성공, 1이면 실패이다.
    model.fit(X_train, train["failed"])

    # 학습한 모델로 valid의 실패 여부를 예측한다.
    #
    # 예측 결과는 0 또는 1이다.
    #
    # 0 = 성공
    # 1 = 실패
    prediction = model.predict(X_valid)

    # F1 Score를 계산해 분류 모델의 성능을 평가한다.
    #
    # valid["failed"] = 실제 정답
    # prediction = 예측한 클래스
    #
    # F1은 0~1 사이의 값이며 높을수록 좋다.
    #
    # zero_division=0:
    # 정밀도나 재현율을 계산할 때 분모가 0인 경우 해당 값을 0으로 처리한다.
    classification_rows.append({
        "model": name,
        "F1": f1_score(
            valid["failed"],
            prediction,
            zero_division=0
        )
    })

    # 모델별 분류 예측 결과를 result에 추가한다.
    #
    # "Dummy_failed" 열
    # "Logistic_failed" 열
    #
    # 실제 실패 여부와 예측 결과를 비교할 수 있다.
    result[name + "_failed"] = prediction


# -------------------------------------------------
# 9. 결과를 DataFrame으로 변환
# -------------------------------------------------

# 회귀 모델별 평가 결과 리스트를 DataFrame으로 변환한다.
#
# 열:
# model, MAE_ms
regression = pd.DataFrame(regression_rows)


# 분류 모델별 평가 결과 리스트를 DataFrame으로 변환한다.
#
# 열:
# model, F1
classification = pd.DataFrame(classification_rows)


# -------------------------------------------------
# 10. 결과를 CSV 파일로 저장
# -------------------------------------------------

# 회귀 모델의 MAE 비교 결과를 저장한다.
#
# index=False:
#   pandas가 자동 생성하는 행 번호를 CSV에 저장하지 않는다.
#
# encoding="utf-8-sig":
#   UTF-8 BOM을 포함하여 저장한다.
#   Excel 등에서 한글을 열 때 인코딩 문제를 줄이는 데 도움된다.
regression.to_csv(
    HERE / "regression_comparison.csv",
    index=False,
    encoding="utf-8-sig"
)


# 분류 모델의 F1 비교 결과를 저장한다.
classification.to_csv(
    HERE / "classification_comparison.csv",
    index=False,
    encoding="utf-8-sig"
)


# valid 4건의 실제 정답과 모델별 예측값을 저장한다.
result.to_csv(
    HERE / "validation_predictions.csv",
    index=False,
    encoding="utf-8-sig"
)


# -------------------------------------------------
# 11. 실행 결과 출력
# -------------------------------------------------

# 데이터가 12 / 4 / 4로 나뉘었는지 확인한다.
print("분할:", len(train), len(valid), len(test))


# 회귀 모델별 MAE를 출력한다.
#
# round(3)은 소수점 셋째 자리까지 반올림한다.
# to_string(index=False)는 행 번호 없이 표를 출력한다.
print("회귀 비교 / 낮은 MAE가 좋음")
print(regression.round(3).to_string(index=False))


# 분류 모델별 F1 Score를 출력한다.
print("분류 비교 / 높은 F1이 좋음")
print(classification.round(3).to_string(index=False))


# 생성된 CSV 파일 이름을 안내한다.
print(
    "저장: regression_comparison.csv, "
    "classification_comparison.csv, "
    "validation_predictions.csv"
)


# test 데이터는 최종 평가를 위해 보관했으며 이번 실습에서는 학습이나 예측에 사용하지 않았다.
print("test는 학습·예측하지 않았습니다.")
