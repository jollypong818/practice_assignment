"""실습 04 심화: 변환 8열 MDI와 원본 4열 순열 중요도를 구분합니다."""
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

from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from preprocessing import build_model

model = build_model(RandomForestClassifier(n_estimators=100, max_depth=4, min_samples_leaf=2,
                                    max_features="sqrt", random_state=42, n_jobs=1))
model.fit(X_train, y_train)
mdi = pd.DataFrame({"feature": model["pre"].get_feature_names_out(),
                    "importance": model["model"].feature_importances_})
# TODO C04: 학습한 Pipeline의 valid 순열 중요도를 F1 기준으로 구하세요.
result = None
# TODO 끝
# 제공: 원본 열을 하나씩 섞은 뒤 F1 감소량을 봅니다. 모델을 다시 학습하지 않습니다.
permutation = pd.DataFrame({"feature": FEATURES,
                            "mean_F1_drop": result.importances_mean,
                            "repeat_std": result.importances_std})
mdi.to_csv(OUT / "mdi_importance.csv", index=False, encoding="utf-8-sig")
permutation.to_csv(OUT / "permutation_importance.csv", index=False, encoding="utf-8-sig")
print("MDI: 변환 후", len(mdi), "열 / 순열: 원본", len(permutation), "열")
print(permutation.round(4).to_string(index=False))
print("음수는 이 valid 표본에서 섞었을 때 점수가 높아졌다는 뜻입니다. 인과관계는 아닙니다.")
