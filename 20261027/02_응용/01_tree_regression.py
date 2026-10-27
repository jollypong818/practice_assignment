"""실습 01 응용: 잎 안 정답의 평균으로 숫자를 예측합니다."""
from sklearn.tree import DecisionTreeRegressor

X = [[100], [200], [300], [700], [800], [900]]
y = [100, 120, 140, 700, 720, 740]
model = DecisionTreeRegressor(max_depth=1, random_state=42)
# TODO A01: 회귀 트리를 학습하고 세 입력을 예측하세요.
pass
prediction = None
# TODO 끝
print("분기 기준:", model.tree_.threshold[0])
print("250·850·1200 예측:", prediction.tolist())
print("왼쪽 평균:", sum(y[:3]) / 3, "오른쪽 평균:", sum(y[3:]) / 3)
print("1200은 학습 범위 밖입니다. 트리도 기존 잎 값으로 예측합니다.")
