"""실습 02 심화: 깊이는 고정하고 최소 잎 표본 수만 비교합니다."""
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

from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import f1_score
from preprocessing import build_model

rows = []
for leaf in [1, 3, 5]:
    # TODO C02: 깊이 3을 고정하고 leaf를 최소 잎 표본 수로 연결하세요.
    model = build_model(DecisionTreeClassifier(max_depth=3, min_samples_leaf=1, random_state=42))
    # TODO 끝
    model.fit(X_train, y_train)
    rows.append({"min_samples_leaf": leaf, "leaves": model["model"].get_n_leaves(),
                 "train_F1": f1_score(y_train, model.predict(X_train), zero_division=0),
                 "valid_F1": f1_score(y_valid, model.predict(X_valid), zero_division=0)})
result = pd.DataFrame(rows)
result.to_csv(OUT / "leaf_comparison.csv", index=False, encoding="utf-8-sig")
print(result.round(4).to_string(index=False))
