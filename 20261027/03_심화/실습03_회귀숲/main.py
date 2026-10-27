"""실습 03 심화: 회귀 숲의 트리 수 20·100을 비교합니다."""
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

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, root_mean_squared_error
from preprocessing import build_model

rows = []
for count in [20, 100]:
    model = build_model(RandomForestRegressor(n_estimators=count, max_depth=4,
                        min_samples_leaf=2, max_features=1.0, random_state=42, n_jobs=1))
    # TODO C03: 실행시간을 정답으로 학습하고 valid 실행시간을 예측하세요.
    pass
    prediction = None
    # TODO 끝
    rows.append({"trees": count, "MAE_ms": mean_absolute_error(valid["elapsed_ms"], prediction),
                 "RMSE_ms": root_mean_squared_error(valid["elapsed_ms"], prediction)})
result = pd.DataFrame(rows)
result.to_csv(OUT / "forest_regression.csv", index=False, encoding="utf-8-sig")
print(result.round(3).to_string(index=False))
print("트리 수만 바꾸었습니다. MAE·RMSE는 작을수록 좋고 단위는 ms입니다.")
