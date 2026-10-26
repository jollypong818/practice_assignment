
"""실습 06 기본필수: 전날의 20건에서 같은 분할로 K만 비교합니다."""


# pathlib는 Python에 기본 포함된 경로 처리 라이브러리이다.
# Path는 파일이나 폴더의 위치를 다루는 데 사용한다.
#
# requests.csv가 현재 Python 파일과 같은 폴더에 있으므로 해당 파일의 경로를 안전하게 찾기 위해 사용한다.
from pathlib import Path


# pandas는 표 형태의 데이터를 읽고 처리하는 라이브러리이다.
#
# CSV 파일을 읽으면 DataFrame이라는 표 형태로 변환할 수 있다.
# DataFrame은 행과 열을 가진 데이터 구조이다.
#
# pd는 pandas를 짧게 사용하기 위한 별칭이다.
import pandas as pd


# scikit-learn에서 데이터를 학습용과 평가용으로
# 나눠주는 train_test_split 함수를 가져온다.
#
# 직접 데이터를 하나씩 나누지 않아도
# 원하는 비율에 따라 데이터를 분할할 수 있다.
from sklearn.model_selection import train_test_split


# -------------------------------------------------
# 1. CSV 파일 읽기
# -------------------------------------------------

# __file__은 현재 실행 중인 Python 파일의 경로이다.
#
# Path(__file__) → 현재 Python 파일의 경로를 Path 객체로 변환
# resolve()      → 절대경로로 변환
# parent         → 해당 파일이 들어 있는 폴더
#
# 예:
# C:/workspace/practice/ex06.py
# → C:/workspace/practice
#
# 이렇게 하면 프로그램을 어느 폴더에서 실행하든 Python 파일이 위치한 폴더를 기준으로 CSV를 찾을 수 있다.
HERE = Path(__file__).resolve().parent


# pd.read_csv()는 CSV 파일을 읽어 DataFrame으로 변환한다.
#
# HERE / "requests.csv"는 현재 Python 파일이 있는 폴더 안의 requests.csv 경로를 의미한다.
#
# raw에는 CSV 파일의 전체 요청 데이터 20건이 저장된다.
raw = pd.read_csv(HERE / "requests.csv")


# -------------------------------------------------
# 2. 데이터 분할
# -------------------------------------------------

# 전체 데이터 20건을 develop과 test로 나눈다.
#
# test_size=0.2
#   전체 데이터의 20%를 test로 분리한다.
#   20건 × 0.2 = 4건
#
# develop = 16건
# test    = 4건
#
# random_state=42
#   데이터를 무작위로 나눌 때 사용할 난수 시드를 고정한다.
#   같은 데이터와 조건으로 다시 실행하면 동일한 분할 결과를 재현할 수 있다.
#   숫자 42 자체에 특별한 머신러닝 의미는 없다.
#
# stratify=raw["failed"]
#   성공(0)과 실패(1)의 비율을 가능한 한 유지하면서 데이터를 분할한다.
#
# 예를 들어 전체 데이터에서 실패가 50%라면 각 분할에서도 비슷한 실패 비율을 유지하려고 한다.
develop, test = train_test_split(
    raw,
    test_size=0.2,
    random_state=42,
    stratify=raw["failed"]
)


# develop 16건을 다시 train과 valid로 나눈다.
#
# test_size=0.25
#   develop 16건 중 25%를 valid로 분리한다.
#
# train = 12건
# valid = 4건
#
# stratify=develop["failed"]
#   train과 valid에서도 성공/실패 비율을 가능한 한 유지한다.
#
# 최종 분할:
# train = 12건 (60%)
# valid = 4건  (20%)
# test  = 4건  (20%)
train, valid = train_test_split(
    develop,
    test_size=0.25,
    random_state=42,
    stratify=develop["failed"]
)


# test는 최종 성능 평가를 위해 따로 보관한다.
# 이번 실습에서는 test를 학습이나 예측에 사용하지 않는다.


# -------------------------------------------------
# 3. 머신러닝에 필요한 라이브러리 가져오기
# -------------------------------------------------

# make_pipeline은 여러 데이터 처리 단계를
# 하나의 모델처럼 연결해주는 함수이다.
#
# 예:
# StandardScaler → KNeighborsClassifier
#
# 이렇게 연결하면 모델 학습과 예측 과정에서
# 표준화가 자동으로 적용된다.
from sklearn.pipeline import make_pipeline


# StandardScaler는 데이터의 평균과 표준편차를 이용해 숫자의 크기를 표준화하는 전처리 도구이다.
#
# KNN은 거리로 이웃을 찾기 때문에 입력 특징들의 숫자 크기가 다를 때 표준화가 중요하다.
from sklearn.preprocessing import StandardScaler


# KNeighborsClassifier는 KNN 분류 모델이다.
#
# 새로운 요청과 가장 가까운 K개의 과거 요청을 찾아 성공(0)인지 실패(1)인지 다수결로 예측한다.
from sklearn.neighbors import KNeighborsClassifier


# f1_score는 분류 모델의 성능을 평가하는 함수이다.
#
# 정밀도(Precision)와 재현율(Recall)을 함께 고려한다.
#
# 이번 실습에서는 실패(1)를 얼마나 잘 예측했는지 평가하기 위해 사용한다.
from sklearn.metrics import f1_score


# -------------------------------------------------
# 4. 모델에 사용할 입력 데이터 준비
# -------------------------------------------------

# train 데이터에서 input_chars 열만 선택한다.
#
# input_chars는 AI에게 전달한 요청의 글자 수이다.
#
# 예:
# 요청 글자 수 100자 → 성공
# 요청 글자 수 800자 → 실패
#
# 이번 실습에서는 글자 수 하나만 이용해 성공/실패를 예측한다.
#
# [["input_chars"]]처럼 대괄호를 두 번 사용하는 이유는
# 결과를 2차원 DataFrame으로 유지하기 위해서이다.
#
# ["input_chars"]는 Series(1차원)를 반환하지만,
# [["input_chars"]]는 DataFrame(2차원)을 반환한다.
X_train = train[["input_chars"]]


# valid에서도 동일한 input_chars 열을 선택한다.
#
# train은 모델 학습에 사용하고
# valid는 학습된 모델의 성능 평가에 사용한다.
X_valid = valid[["input_chars"]]


# -------------------------------------------------
# 5. K값을 바꾸면서 모델 비교
# -------------------------------------------------

# KNN의 이웃 수를 1, 3, 5로 바꾸면서 반복한다.
#
# 첫 번째 반복 → k = 1
# 두 번째 반복 → k = 3
# 세 번째 반복 → k = 5
#
# 같은 train과 valid를 사용하므로
# K값에 따른 성능 차이를 비교할 수 있다.
for k in [1, 3, 5]:

    # 머신러닝 처리 과정을 하나의 Pipeline으로 만든다.
    #
    # 첫 번째 단계: StandardScaler()
    #   입력 글자 수를 표준화한다.
    #
    # 두 번째 단계: KNeighborsClassifier()
    #   가장 가까운 K개의 요청을 이용해 실패 여부를 예측한다.
    #
    # n_neighbors=k
    #   반복문에서 전달받은 k를 이웃 수로 설정한다.
    #
    # 따라서 반복할 때마다 서로 다른 KNN 모델이 생성된다.
    model = make_pipeline(
        StandardScaler(),
        KNeighborsClassifier(n_neighbors=k)
    )

    # 모델을 학습한다.
    #
    # X_train       → 요청 글자 수 (입력)
    # train["failed"] → 실제 실패 여부 (정답)
    #
    # Pipeline 내부에서는 다음 순서로 실행된다.
    #
    # 1. StandardScaler가 train의 평균과 표준편차 계산
    # 2. train의 input_chars를 표준화
    # 3. KNN이 표준화된 학습 데이터와 정답을 저장
    #
    # 여기서는 valid나 test를 학습에 사용하지 않는다.
    model.fit(X_train, train["failed"])

    # 학습한 모델로 valid 데이터의 실패 여부를 예측한다.
    #
    # Pipeline 내부에서 자동으로 다음 작업을 수행한다.
    #
    # 1. train에서 계산한 기준으로 X_valid를 표준화
    # 2. KNN으로 가까운 이웃을 찾음
    # 3. 각 요청의 성공(0)/실패(1)를 예측
    #
    # prediction에는 valid 4건에 대한 예측 결과가 저장된다.
    prediction = model.predict(X_valid)

    # F1 Score를 계산하여 모델 성능을 확인한다.
    #
    # valid["failed"] → 실제 정답
    # prediction      → 모델이 예측한 결과
    #
    # 두 값을 비교하여 F1 Score를 계산한다.
    #
    # F1은 0~1 사이의 값이며 높을수록 좋다.
    #
    # zero_division=0
    #   정밀도나 재현율 계산에서 분모가 0이 되는 경우 해당 값을 0으로 처리하도록 설정한다.
    #
    # model[-1]은 Pipeline의 마지막 단계인 KNeighborsClassifier를 의미한다.
    #
    # .n_neighbors는 현재 모델에 설정된 K값이다.
    #
    # round(..., 3)은 소수점 셋째 자리까지 표시한다.
    print(
        "K:", model[-1].n_neighbors,
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


# 데이터가 의도한 개수로 나뉘었는지 확인한다.
#
# len(train) → 12
# len(valid) → 4
# len(test)  → 4
#
# 출력 결과: 분할: 12 4 4
print("분할:", len(train), len(valid), len(test))
