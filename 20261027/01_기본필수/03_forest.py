
"""실습 03 응용: 100건의 요청 데이터로 실패 여부를 예측하는 머신러닝 실습"""

# ==================================================
# 1. 필요한 라이브러리 가져오기
# ==================================================

# 파일 및 폴더 경로를 다루는 파이썬 표준 라이브러리
from pathlib import Path

# CSV 파일을 읽고 DataFrame(표 형태 데이터)으로 처리하는 라이브러리
import pandas as pd


# ==================================================
# 2. CSV 데이터 불러오기
# ==================================================

# 현재 실행 중인 파이썬 파일이 위치한 폴더의 절대경로
# 터미널 실행 위치가 달라도 동일한 파일을 읽기 위해 사용한다.
HERE = Path(__file__).resolve().parent

# requests.csv를 읽어 DataFrame으로 변환한다.
# set_index("request_id")는 request_id 열을 행 인덱스로 지정한다.
# 이후 request_id를 기준으로 원하는 행을 선택하기 위해 사용한다.
raw = pd.read_csv(
    HERE / "data/requests.csv"
).set_index("request_id")


# ==================================================
# 3. 학습용(train)과 검증용(valid) 데이터 분리
# ==================================================

# split_manifest.csv에는 각 요청이 어떤 데이터셋에 속하는지 기록되어 있다.
# 예: request_id, split(train/valid/test), position
#
# 이전에 나눠 놓은 데이터 구성을 그대로 재현하기 위해 사용한다.
split = pd.read_csv(HERE / "data/split_manifest.csv")


# split 열의 값이 "train"인 행만 선택한다.
# sort_values("position")으로 기존 행 순서를 유지한다.
# ["request_id"]로 해당 요청 ID만 가져온다.
train_ids = split.loc[
    split["split"] == "train"
].sort_values("position")["request_id"]


# 검증용 데이터도 동일한 방식으로 ID를 추출한다.
valid_ids = split.loc[
    split["split"] == "valid"
].sort_values("position")["request_id"]


# raw에서 학습용 요청 ID에 해당하는 행만 선택한다.
# .loc[]는 인덱스 이름을 기준으로 데이터를 가져온다.
train = raw.loc[train_ids]

# 검증용 요청 ID에 해당하는 행만 선택한다.
valid = raw.loc[valid_ids]


# ==================================================
# 4. 머신러닝 입력 특성(Feature) 선택
# ==================================================

# 모델이 실패 여부를 예측할 때 참고할 입력 데이터
#
# input_chars   : 요청에 포함된 글자 수 (숫자)
# allowed_tools : 사용할 수 있는 도구 수 (숫자)
# task_type     : 작업 유형 (문자/범주)
# priority      : 요청 우선순위 (문자/범주)
#
# failed는 정답이므로 입력 특성에 포함하지 않는다.
features = [
    "input_chars",
    "allowed_tools",
    "task_type",
    "priority"
]

# 학습용 입력 데이터 X
# 여러 열을 선택하므로 DataFrame(2차원)이 된다.
X_train = train[features]

# 검증용 입력 데이터 X
X_valid = valid[features]

# test 데이터는 최종 평가 전까지 사용하지 않는다.
# 검증 과정에서 test를 사용하면 평가 결과가 편향될 수 있다.


# ==================================================
# 5. 전처리 라이브러리 가져오기
# ==================================================

# 결측치(NaN)를 다른 값으로 대체하는 도구
from sklearn.impute import SimpleImputer

# StandardScaler : 평균 0, 표준편차 1이 되도록 변환
# MinMaxScaler   : 지정된 범위(기본 0~1)로 변환
# 이번 실습에서는 StandardScaler만 사용한다.
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# 문자형 범주 데이터를 머신러닝이 처리할 수 있는 숫자로 변환
from sklearn.preprocessing import OneHotEncoder

# 열마다 서로 다른 전처리를 적용하기 위한 도구
from sklearn.compose import ColumnTransformer

# 여러 처리 단계를 순서대로 연결하는 도구
from sklearn.pipeline import Pipeline

# 모델이나 전처리 객체를 복제할 때 사용하는 도구
# 이번 코드에서는 사용하지 않는다.
from sklearn.base import clone


# ==================================================
# 6. 머신러닝 모델과 평가 지표 가져오기
# ==================================================

# 로지스틱 회귀 분류 모델
# 입력 데이터를 이용해 0 또는 1의 분류 및 확률을 예측한다.
from sklearn.linear_model import LogisticRegression

# confusion_matrix : 실제값과 예측값을 비교한 혼동행렬
# f1_score         : 정밀도와 재현율의 조화평균
from sklearn.metrics import confusion_matrix, f1_score


# ==================================================
# 7. 숫자형 데이터 전처리
# ==================================================

# 숫자 데이터는 두 단계로 처리한다.
#
# 1단계: 결측치를 해당 열의 중앙값으로 대체
# 2단계: 평균 0, 표준편차 1이 되도록 표준화
#
# Pipeline은 앞 단계의 출력이 다음 단계의 입력이 되는 구조다.
num = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])


# ==================================================
# 8. 문자형(범주형) 데이터 전처리
# ==================================================

# 문자 데이터는 두 단계로 처리한다.
#
# 1단계: 결측치를 해당 열에서 가장 자주 나타난 값으로 대체
# 2단계: One-Hot Encoding으로 숫자 형태로 변환
#
# 예: task_type이 "search", "write"라면
# search -> [1, 0]
# write  -> [0, 1]
#
# handle_unknown="ignore"
# 검증 데이터에서 처음 보는 범주가 등장해도 오류를 내지 않는다.
#
# sparse_output=False
# 결과를 일반적인 밀집 배열 형태로 반환한다.
cat = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(
        handle_unknown="ignore",
        sparse_output=False
    ))
])


# ==================================================
# 9. 열 종류에 따라 전처리 방법 지정
# ==================================================

# ColumnTransformer는 각 열에 서로 다른 전처리를 적용한다.
#
# features[:2]
# → ["input_chars", "allowed_tools"]
# → 숫자형 전처리 num 적용
#
# features[2:]
# → ["task_type", "priority"]
# → 범주형 전처리 cat 적용
#
# 전처리된 결과는 하나의 입력 배열로 결합된다.
pre = ColumnTransformer([
    ("num", num, features[:2]),
    ("cat", cat, features[2:])
])


# ==================================================
# 10. 전처리 + 머신러닝 모델 연결
# ==================================================

# 전체 학습 과정을 하나의 Pipeline으로 구성한다.
#
# 1단계: pre
# → 결측치 처리, 표준화, 원핫 인코딩
#
# 2단계: model
# → 전처리된 데이터를 이용해 로지스틱 회귀 학습
#
# C=1.0
# → 규제 강도를 조절하는 하이퍼파라미터
#   C가 작을수록 규제가 강해진다.
#
# max_iter=1000
# → 모델 최적화 알고리즘의 최대 반복 횟수
model = Pipeline([
    ("pre", pre),
    ("model", LogisticRegression(
        C=1.0,
        max_iter=1000
    ))
])


# ==================================================
# 11. 모델 학습 (TODO A03 정답)
# ==================================================

# X_train : 모델에 입력할 요청 정보
# train["failed"] : 각 요청의 실제 실패 여부(정답)
#
# fit()을 실행하면:
# 1. 학습 데이터에 맞춰 전처리 규칙을 학습한다.
# 2. 학습 데이터를 변환한다.
# 3. 변환된 데이터를 이용해 로지스틱 회귀 모델을 학습한다.
model.fit(X_train, train["failed"])


# ==================================================
# 12. 검증 데이터 예측 (TODO A03 정답)
# ==================================================

# 학습이 완료된 모델에 검증용 입력 데이터를 전달한다.
#
# predict()는 전처리된 검증 데이터를 바탕으로
# 각 요청이 실패할지 성공할지 0 또는 1로 예측한다.
#
# 정답인 valid["failed"]는 예측에 전달하지 않는다.
prediction = model.predict(X_valid)


# ==================================================
# 13. 클래스 순서 확인
# ==================================================

# 모델이 분류하는 클래스의 순서를 출력한다.
# 일반적으로 [0, 1] 형태다.
print("클래스 순서:", model.classes_)


# ==================================================
# 14. 실패 확률 확인
# ==================================================

# predict_proba()는 각 클래스에 속할 확률을 반환한다.
#
# 예:
# [[0.8, 0.2],
#  [0.1, 0.9]]
#
# 첫 번째 열: 성공(0) 확률
# 두 번째 열: 실패(1) 확률
#
# [:4, 1]
# → 앞에서 4개 행을 선택
# → 각 행의 두 번째 열(실패 확률)만 가져온다.
#
# round(3) : 소수점 셋째 자리까지 반올림
print(
    "앞 4건 실패 확률:",
    model.predict_proba(X_valid)[:4, 1].round(3)
)


# ==================================================
# 15. 혼동행렬(Confusion Matrix)
# ==================================================

# 실제 정답과 모델 예측을 비교한다.
#
# labels=[0, 1]
# → 성공(0), 실패(1) 순서로 행과 열을 배치한다.
#
# 행: 실제값
# 열: 예측값
#
# [[TN, FP],
#  [FN, TP]]
#
# TN: 실제 성공 → 성공 예측
# FP: 실제 성공 → 실패 예측
# FN: 실제 실패 → 성공 예측
# TP: 실제 실패 → 실패 예측
print("혼동행렬 / 행=실제, 열=예측, 순서=[0,1]")

print(
    confusion_matrix(
        valid["failed"],
        prediction,
        labels=[0, 1]
    )
)


# ==================================================
# 16. F1 Score 계산
# ==================================================

# 실제 실패 여부와 모델 예측 결과를 비교한다.
#
# F1 Score는 정밀도(Precision)와 재현율(Recall)을
# 함께 고려하는 평가 지표다.
#
# 1에 가까울수록 좋은 성능을 의미한다.
#
# zero_division=0
# → 정밀도나 재현율 계산에서 0으로 나누는 상황이
#   발생하면 해당 값을 0으로 처리한다.
#
# round(..., 3)
# → 결과를 소수점 셋째 자리까지 반올림한다.
print(
    "valid F1:",
    round(
        f1_score(
            valid["failed"],
            prediction,
            zero_division=0
        ),
        3
    )
)
