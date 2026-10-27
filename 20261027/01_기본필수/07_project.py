
"""실습 07~08: 두 분류 모델의 성능을 비교하고 결과를 CSV로 저장하는 실습"""


# ==================================================
# 1. 필요한 라이브러리 가져오기
# ==================================================

# 파일과 폴더의 경로를 다루는 파이썬 표준 라이브러리
from pathlib import Path

# CSV 파일을 읽고 표(DataFrame) 형태로 데이터를 처리하는 라이브러리
import pandas as pd

# 데이터를 학습용, 검증용, 테스트용으로 나누는 함수
from sklearn.model_selection import train_test_split


# ==================================================
# 2. CSV 파일 불러오기
# ==================================================

# __file__ : 현재 실행 중인 파이썬 파일의 경로
# resolve() : 절대경로로 변환
# parent : 해당 파일이 들어 있는 폴더
#
# 터미널 실행 위치와 관계없이 같은 CSV 파일을 읽기 위해 사용한다.
HERE = Path(__file__).resolve().parent

# requests.csv 파일을 읽어 DataFrame으로 변환한다.
# raw에는 총 20건의 요청 데이터가 저장된다.
raw = pd.read_csv(HERE / "requests.csv")


# ==================================================
# 3. 학습 / 검증 / 테스트 데이터 분리
# ==================================================

# 전체 20건 중 20%를 test로 분리한다.
#
# develop : 16건 (80%)
# test    : 4건  (20%)
#
# stratify=raw["failed"]
# → 실패 여부(0/1)의 비율을 최대한 유지한다.
#
# random_state=42
# → 실행할 때마다 동일한 데이터 분할 결과가 나오도록 한다.
develop, test = train_test_split(
    raw,
    test_size=0.2,
    stratify=raw["failed"],
    random_state=42
)


# develop 16건을 train 12건, valid 4건으로 나눈다.
#
# 최종 데이터 구성
# train : 12건 (60%) → 모델 학습
# valid : 4건  (20%) → 모델 검증
# test  : 4건  (20%) → 최종 평가를 위해 보관
train, valid = train_test_split(
    develop,
    test_size=0.25,
    stratify=develop["failed"],
    random_state=42
)


# ==================================================
# 4. 입력 데이터(X)와 정답 데이터(y) 분리
# ==================================================

# 입력 특성으로 요청 글자 수를 선택한다.
# 대괄호를 두 번 사용해 2차원 DataFrame으로 반환한다.
X_train = train[["input_chars"]]
X_valid = valid[["input_chars"]]

# 정답은 failed 열이다.
#
# 0 = 성공
# 1 = 실패
y_train = train["failed"]
y_valid = valid["failed"]


# ==================================================
# 5. 머신러닝 관련 라이브러리 가져오기
# ==================================================

# DecisionTreeClassifier
# → 조건에 따라 데이터를 나누는 단일 의사결정나무 분류 모델
from sklearn.tree import DecisionTreeClassifier

# RandomForestClassifier
# → 여러 의사결정나무를 학습하고 예측을 종합하는 앙상블 모델
from sklearn.ensemble import RandomForestClassifier

# StratifiedKFold
# → 클래스 비율을 유지하면서 K개 Fold로 데이터를 분리한다.
#
# cross_val_score
# → 교차검증을 자동으로 수행하고 Fold별 점수를 반환한다.
from sklearn.model_selection import StratifiedKFold, cross_val_score

# ColumnTransformer
# → 데이터 열마다 서로 다른 전처리 방법을 적용한다.
from sklearn.compose import ColumnTransformer

# OneHotEncoder
# → 문자형 범주 데이터를 숫자 형태로 변환한다.
from sklearn.preprocessing import OneHotEncoder

# Pipeline
# → 전처리와 머신러닝 모델을 하나의 처리 과정으로 연결한다.
from sklearn.pipeline import Pipeline

# clone
# → 모델이나 전처리 객체의 설정을 복제한다.
# → 기존 학습 상태는 복사하지 않는다.
from sklearn.base import clone

# f1_score
# → 정밀도와 재현율을 함께 고려하는 분류 성능 평가 지표
from sklearn.metrics import f1_score


# ==================================================
# 6. 입력 특성(Feature) 지정
# ==================================================

# 이번 실습에서는 입력 특성을 두 개 사용한다.
#
# input_chars : 요청 글자 수 (숫자형)
# task_type   : 요청 작업 유형 (범주형)
#
# failed는 정답이므로 입력 특성에 포함하지 않는다.
# 실행시간처럼 요청 전에 알 수 없는 정보도 사용하지 않는다.
features = ["input_chars", "task_type"]


# 앞에서 만들었던 X_train, X_valid를
# 이번 실습에 사용할 두 개 특성으로 다시 지정한다.
#
# X_train : 학습용 입력 데이터
# X_valid : 검증용 입력 데이터
X_train, X_valid = train[features], valid[features]


# ==================================================
# 7. 숫자형 / 범주형 데이터 전처리 설정
# ==================================================

# ColumnTransformer는 열마다 다른 전처리를 적용한다.
#
# ("num", "passthrough", ["input_chars"])
# → input_chars는 숫자 데이터이므로 그대로 사용한다.
# → passthrough는 별도의 변환 없이 통과시킨다는 의미다.
#
# ("cat", OneHotEncoder(...), ["task_type"])
# → task_type은 문자형 데이터이므로 원핫 인코딩을 적용한다.
#
# 예: task_type이 "search", "write"라면
# search → [1, 0]
# write  → [0, 1]
#
# handle_unknown="ignore"
# → 학습할 때 보지 못한 범주가 검증 데이터에 등장해도
#   오류를 발생시키지 않고 해당 범주의 인코딩을 모두 0으로 처리한다.
#
# sparse_output=False
# → 희소행렬 대신 일반적인 밀집 배열을 반환한다.
pre = ColumnTransformer([
    (
        "num",
        "passthrough",
        ["input_chars"]
    ),
    (
        "cat",
        OneHotEncoder(
            handle_unknown="ignore",
            sparse_output=False
        ),
        ["task_type"]
    ),
])


# ==================================================
# 8. 교차검증 설정
# ==================================================

# n_splits=3
# → train 12건을 3개 Fold로 나눈다.
# → 각 Fold는 4건씩 구성된다.
#
# shuffle=True
# → 데이터를 나누기 전에 무작위로 섞는다.
#
# random_state=42
# → 무작위 분할 결과를 재현할 수 있도록 난수를 고정한다.
#
# StratifiedKFold는 각 Fold의 성공/실패 비율을
# 최대한 비슷하게 유지한다.
folds = StratifiedKFold(
    n_splits=3,
    shuffle=True,
    random_state=42
)


# ==================================================
# 9. 비교할 머신러닝 모델 2개 준비
# ==================================================

# candidates는 (모델 이름, 모델 객체) 형태의 튜플을
# 리스트에 저장한 것이다.
#
# 첫 번째 후보: Decision Tree
# → 하나의 의사결정나무를 사용한다.
# → max_depth=3으로 나무 깊이를 제한한다.
#
# 두 번째 후보: Random Forest
# → 의사결정나무 20개를 사용한다.
# → 각 나무의 최대 깊이는 3이다.
# → n_jobs=1은 CPU 작업 스레드를 1개 사용한다는 뜻이다.
#
# 두 모델 모두 random_state=42로 난수를 고정한다.
candidates = [
    (
        "Tree",
        DecisionTreeClassifier(
            max_depth=3,
            random_state=42
        )
    ),
    (
        "Forest",
        RandomForestClassifier(
            n_estimators=20,
            max_depth=3,
            random_state=42,
            n_jobs=1
        )
    )
]


# ==================================================
# 10. 결과 저장용 변수 준비
# ==================================================

# rows
# → 모델별 평균 CV F1, 표준편차, valid F1을 저장할 리스트
#
# cv_rows
# → 각 모델의 Fold별 F1 점수를 저장할 리스트
rows, cv_rows = [], []


# 검증 데이터에서 request_id와 failed 열만 복사한다.
#
# request_id : 요청을 구분하는 고유 ID
# failed     : 실제 정답
#
# .copy()를 사용해 원본과 별도의 DataFrame을 만든다.
#
# 이후 Tree와 Forest의 예측 결과를 열로 추가할 예정이다.
predictions = valid[["request_id", "failed"]].copy()


# ==================================================
# 11. 모델별 학습과 평가 반복
# ==================================================

# candidates에 저장된 두 모델을 순서대로 꺼낸다.
#
# 첫 번째 반복
# name = "Tree"
# estimator = DecisionTreeClassifier(...)
#
# 두 번째 반복
# name = "Forest"
# estimator = RandomForestClassifier(...)
for name, estimator in candidates:

    # ----------------------------------------------
    # 11-1. 전처리 + 모델을 Pipeline으로 연결
    # ----------------------------------------------

    # Pipeline은 전처리와 모델을 순서대로 실행한다.
    #
    # 첫 번째 단계: pre
    # → 숫자형 데이터 통과
    # → 문자형 데이터 원핫 인코딩
    #
    # 두 번째 단계: model
    # → 전처리된 데이터로 머신러닝 모델 학습
    #
    # clone(pre)
    # → 전처리 객체의 설정을 복제한다.
    # → 모델별로 별도의 전처리 객체를 사용하기 위한 목적이다.
    #
    # 교차검증에서는 각 Fold의 학습 데이터에 대해서만
    # 전처리 규칙을 학습하므로 데이터 누수를 방지할 수 있다.
    model = Pipeline([
        ("pre", clone(pre)),
        ("model", estimator)
    ])


    # ==============================================
    # 11-2. 3-Fold 교차검증 (TODO B07a 정답)
    # ==============================================

    # cross_val_score는 교차검증을 자동으로 수행한다.
    #
    # model
    # → 전처리와 분류 모델이 연결된 Pipeline
    #
    # X_train
    # → 학습용 입력 데이터
    #
    # y_train
    # → 학습용 실제 정답
    #
    # cv=folds
    # → 3-Fold 교차검증 수행
    #
    # scoring="f1"
    # → 실패 클래스(1)에 대한 F1 Score 계산
    #
    # 각 Fold마다:
    # 1. 학습 데이터 8건으로 전처리와 모델을 학습한다.
    # 2. 남은 4건으로 예측한다.
    # 3. 예측 결과의 F1 점수를 계산한다.
    #
    # 총 3개의 F1 점수가 반환된다.
    scores = cross_val_score(
        model,
        X_train,
        y_train,
        cv=folds,
        scoring="f1"
    )


    # ==============================================
    # 11-3. 전체 train 학습 및 valid 예측
    #      (TODO B07b 정답)
    # ==============================================

    # 전체 학습 데이터 12건으로 모델을 학습한다.
    #
    # fit()을 호출하면:
    # 1. train 데이터로 원핫 인코딩 규칙을 학습한다.
    # 2. 데이터를 변환한다.
    # 3. 변환된 데이터로 분류 모델을 학습한다.
    #
    # cross_val_score에서 학습한 모델과는 별도로
    # 현재 model 객체를 전체 train 데이터로 학습시킨다.
    model.fit(X_train, y_train)

    # 학습된 모델에 검증 데이터 4건을 전달한다.
    #
    # Pipeline이 학습된 전처리 규칙을 적용한 뒤
    # 성공(0) 또는 실패(1)를 예측한다.
    prediction = model.predict(X_valid)


    # ==============================================
    # 11-4. 모델별 성능 요약 저장
    # ==============================================

    # rows 리스트에 딕셔너리 형태로 결과를 추가한다.
    #
    # model
    # → 모델 이름(Tree 또는 Forest)
    #
    # CV_F1
    # → 3개 Fold의 F1 평균
    #
    # CV_std
    # → 3개 Fold F1의 표준편차
    #
    # valid_F1
    # → 전체 train으로 학습한 모델의 검증 F1 점수
    #
    # append()는 리스트 끝에 새로운 항목을 추가한다.
    rows.append({
        "model": name,
        "CV_F1": scores.mean(),
        "CV_std": scores.std(),
        "valid_F1": f1_score(
            y_valid,
            prediction,
            zero_division=0
        )
    })


    # ==============================================
    # 11-5. Fold별 점수 저장
    # ==============================================

    # enumerate()는 반복 가능한 데이터에서
    # 순서 번호와 값을 함께 가져오는 함수다.
    #
    # start=1
    # → 번호를 0이 아닌 1부터 시작한다.
    #
    # 예: scores = [0.5, 0.8, 1.0]이라면
    #
    # number=1, value=0.5
    # number=2, value=0.8
    # number=3, value=1.0
    #
    # 각 Fold의 F1 점수를 딕셔너리로 저장한다.
    for number, value in enumerate(scores, start=1):
        cv_rows.append({
            "model": name,
            "fold": number,
            "F1": value
        })


    # ==============================================
    # 11-6. 검증 데이터 예측 결과 저장
    # ==============================================

    # predictions DataFrame에 현재 모델의 예측 결과를
    # 새로운 열로 추가한다.
    #
    # Tree 모델 반복 시 → "Tree" 열 추가
    # Forest 모델 반복 시 → "Forest" 열 추가
    #
    # 결과적으로 각 요청에 대해 실제 정답과
    # 두 모델의 예측 결과를 비교할 수 있다.
    predictions[name] = prediction


    # ==============================================
    # 11-7. Random Forest 특성 중요도 계산
    # ==============================================

    # 현재 모델 이름이 "Forest"인 경우에만 실행한다.
    #
    # Tree와 Forest 모두 특성 중요도를 제공하지만,
    # 이번 실습에서는 Forest의 중요도만 저장한다.
    if name == "Forest":

        # model["pre"]
        # → Pipeline의 전처리 객체를 가져온다.
        #
        # get_feature_names_out()
        # → 전처리 후 생성된 특성 이름을 가져온다.
        #
        # 예:
        # num__input_chars
        # cat__task_type_search
        # cat__task_type_write
        #
        # model["model"]
        # → Pipeline의 Random Forest 모델을 가져온다.
        #
        # feature_importances_
        # → 학습된 모델이 계산한 각 특성의 중요도를 가져온다.
        #
        # 전처리 후에는 원핫 인코딩으로 특성 수가
        # 증가할 수 있으므로 변환된 특성 이름을 사용한다.
        importance = pd.DataFrame({
            "feature": model["pre"].get_feature_names_out(),
            "importance": model["model"].feature_importances_
        })


# ==================================================
# 12. 모델 비교 결과를 DataFrame으로 변환
# ==================================================

# rows에 저장한 딕셔너리들을 하나의 표로 변환한다.
#
# 각 행은 하나의 모델에 해당한다.
# 열에는 CV_F1, CV_std, valid_F1 등이 포함된다.
comparison = pd.DataFrame(rows)


# ==================================================
# 13. 모델 비교 결과 CSV 저장
# ==================================================

# to_csv()는 DataFrame을 CSV 파일로 저장하는 메서드다.
#
# HERE / "파일명"
# → 현재 파이썬 파일과 같은 폴더에 저장한다.
#
# index=False
# → DataFrame의 행 인덱스를 CSV에 저장하지 않는다.
#
# encoding="utf-8-sig"
# → UTF-8 BOM을 포함하여 저장한다.
# → Excel에서 한글이 깨지는 문제를 줄이는 데 유용하다.
comparison.to_csv(
    HERE / "classification_comparison.csv",
    index=False,
    encoding="utf-8-sig"
)


# ==================================================
# 14. 교차검증 Fold별 점수 CSV 저장
# ==================================================

# cv_rows 리스트를 DataFrame으로 변환한 뒤 CSV로 저장한다.
#
# 모델 2개 × Fold 3개 = 총 6개 행이 저장된다.
pd.DataFrame(cv_rows).to_csv(
    HERE / "cv_scores.csv",
    index=False,
    encoding="utf-8-sig"
)


# ==================================================
# 15. 검증 데이터 예측 결과 CSV 저장
# ==================================================

# 검증 데이터의 실제 정답과
# Tree / Forest의 예측 결과를 저장한다.
#
# 검증 데이터가 4건이므로 총 4개 행이 저장된다.
predictions.to_csv(
    HERE / "validation_predictions.csv",
    index=False,
    encoding="utf-8-sig"
)


# ==================================================
# 16. Random Forest 특성 중요도 CSV 저장
# ==================================================

# Forest 모델에서 계산한 특성별 중요도를 저장한다.
#
# 각 행에는 전처리된 특성 이름과 중요도가 기록된다.
importance.to_csv(
    HERE / "feature_importance.csv",
    index=False,
    encoding="utf-8-sig"
)


# ==================================================
# 17. 데이터 분할 개수 출력
# ==================================================

# len()은 데이터의 행 개수를 반환한다.
#
# 예상 출력:
# 분할: 12 4 4
print("분할:", len(train), len(valid), len(test))


# ==================================================
# 18. 모델별 성능 비교 결과 출력
# ==================================================

# comparison.round(3)
# → 숫자 값을 소수점 셋째 자리까지 반올림한다.
#
# to_string(index=False)
# → 행 인덱스를 제외하고 전체 표를 문자열로 출력한다.
print(comparison.round(3).to_string(index=False))


# ==================================================
# 19. 특성 중요도 출력
# ==================================================

# Forest 모델의 각 특성 중요도를 표로 출력한다.
print("중요도")
print(importance.round(3).to_string(index=False))


# ==================================================
# 20. 저장 결과 안내
# ==================================================

# 생성한 CSV 파일 4개의 이름을 출력한다.
print(
    "저장: classification_comparison.csv, "
    "cv_scores.csv, validation_predictions.csv, "
    "feature_importance.csv"
)


# ==================================================
# 21. Test 데이터 미사용 확인
# ==================================================

# 최종 평가용 test 데이터는 이번 실습에서
# 학습, 전처리, 예측, 평가에 사용하지 않았다.
#
# 모델 비교 과정에서 test를 사용하지 않는 이유는
# 최종 평가의 객관성을 유지하기 위해서다.
print("test는 학습·변환·예측·평가하지 않았습니다.")
