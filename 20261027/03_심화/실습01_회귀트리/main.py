"""실습 01 심화: 회귀 트리의 잎별 평균을 표로 확인합니다."""
from pathlib import Path
import pandas as pd
from sklearn.tree import DecisionTreeRegressor

X = [[100], [200], [300], [700], [800], [900]]
y = [100, 120, 140, 700, 720, 740]
# TODO C01: 깊이 1인 회귀 트리를 만들고 학습하세요.
model = DecisionTreeRegressor(max_depth=1, random_state=42)
pass
# TODO 끝
# 제공: apply는 각 학습 행이 도착한 잎 번호를 돌려줍니다. 번호 자체는 크기 순위가 아닙니다.
rows = pd.DataFrame({"leaf": model.apply(X), "actual": y})
means = rows.groupby("leaf", as_index=False).agg(count=("actual", "size"), mean_ms=("actual", "mean"))
OUT = Path(__file__).resolve().parent / "outputs"
OUT.mkdir(exist_ok=True)
means.to_csv(OUT / "leaf_means.csv", index=False, encoding="utf-8-sig")
print("분기 기준:", model.tree_.threshold[0])
print(means.to_string(index=False))
print("250·850·1200 예측:", model.predict([[250], [850], [1200]]).tolist())
