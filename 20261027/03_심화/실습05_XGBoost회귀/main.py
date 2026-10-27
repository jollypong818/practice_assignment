"""실습 05 심화: XGBoost의 회귀 목적과 오차를 연결합니다."""
from pathlib import Path
import pandas as pd

# 제공: 전날의 분할 소속뿐 아니라 position 순서까지 그대로 읽습니다.
HERE = Path(__file__).resolve().parent
raw = pd.read_csv(HERE / "data/requests.csv").set_index("request_id")
manifest = pd.read_csv(HERE / "data/split_manifest.csv")
train_ids = manifest.loc[manifest["split"] == "train"].sort_values("position")["request_id"]
valid_ids = manifest.loc[manifest["split"] == "valid"].sort_values("position")["request_id"]
train = raw.loc[train_ids]
valid = raw.loc[valid_ids]
FEATURES = ["input_chars", "allowed_tools", "task_type", "priority"]
X_train, X_valid = train[FEATURES], valid[FEATURES]
y_train, y_valid = train["failed"], valid["failed"]
OUT = HERE / "outputs"
OUT.mkdir(exist_ok=True)
# test 20건의 입력·정답은 아래 모델에 전달하지 않습니다.

from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, root_mean_squared_error
from preprocessing import build_model

# 제공: 목적함수는 회귀용 squared error, 진단 지표는 rmse입니다.
estimator = XGBRegressor(n_estimators=80, max_depth=2, learning_rate=0.05,
                  subsample=0.8, colsample_bytree=1.0, reg_lambda=1.0,
                  objective="reg:squarederror", eval_metric="rmse",
                  tree_method="hist", device="cpu", random_state=42, n_jobs=1)
model = build_model(estimator)
# TODO C05: 회귀 정답 elapsed_ms로 학습하고 valid를 예측하세요.
pass
prediction = None
# TODO 끝
result = pd.DataFrame([{"model": "XGB", "MAE_ms": mean_absolute_error(valid["elapsed_ms"], prediction),
                       "RMSE_ms": root_mean_squared_error(valid["elapsed_ms"], prediction)}])
result.to_csv(OUT / "xgb_regression.csv", index=False, encoding="utf-8-sig")
print(result.round(3).to_string(index=False))
print("고정 80회차·깊이2입니다. valid를 조기 종료에 사용하지 않았습니다.")
