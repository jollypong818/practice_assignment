"""실습 07~08: 분류 후보 2개를 비교하고 같은 파일을 다시 실행합니다."""
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split

# 제공: 이 파일 옆의 정상 CSV 20건을 읽습니다. 현재 터미널 위치와 무관합니다.
HERE = Path(__file__).resolve().parent
raw = pd.read_csv(HERE / "requests.csv")
develop, test = train_test_split(raw, test_size=0.2, stratify=raw["failed"], random_state=42)
train, valid = train_test_split(develop, test_size=0.25, stratify=develop["failed"], random_state=42)
# test 4건은 보관만 합니다. 입력은 실행 전에 아는 글자 수입니다.
X_train = train[["input_chars"]]
X_valid = valid[["input_chars"]]
y_train = train["failed"]
y_valid = valid["failed"]

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.base import clone
from sklearn.metrics import f1_score

# 제공: 전날과 같은 입력 2열입니다. 실행시간과 failed는 입력에 넣지 않습니다.
features = ["input_chars", "task_type"]
X_train, X_valid = train[features], valid[features]
pre = ColumnTransformer([
    ("num", "passthrough", ["input_chars"]),
    ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), ["task_type"]),
])
folds = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
candidates = [("Tree", DecisionTreeClassifier(max_depth=3, random_state=42)),
              ("Forest", RandomForestClassifier(n_estimators=20, max_depth=3, random_state=42, n_jobs=1))]
rows, cv_rows = [], []
predictions = valid[["request_id", "failed"]].copy()
for name, estimator in candidates:
    # 제공: 전처리까지 Pipeline에 포함하여 fold 학습 부분에서만 fit하게 합니다.
    model = Pipeline([("pre", clone(pre)), ("model", estimator)])
    # TODO B07a: 전처리까지 연결한 model을 train에서 교차검증하세요.
    scores = None
    # TODO 끝
    # TODO B07b: 전체 train으로 학습하고 valid를 예측하세요.
    pass
    prediction = None
    # TODO 끝
    rows.append({"model": name, "CV_F1": scores.mean(),
                 "CV_std": scores.std(), "valid_F1": f1_score(y_valid, prediction, zero_division=0)})
    for number, value in enumerate(scores, start=1):
        cv_rows.append({"model": name, "fold": number, "F1": value})
    predictions[name] = prediction
    if name == "Forest":
        importance = pd.DataFrame({"feature": model["pre"].get_feature_names_out(),
                                   "importance": model["model"].feature_importances_})

# 제공: 입력 파일을 덮어쓰지 않고 결과 4개를 같은 폴더에 만듭니다.
comparison = pd.DataFrame(rows)
comparison.to_csv(HERE / "classification_comparison.csv", index=False, encoding="utf-8-sig")
pd.DataFrame(cv_rows).to_csv(HERE / "cv_scores.csv", index=False, encoding="utf-8-sig")
predictions.to_csv(HERE / "validation_predictions.csv", index=False, encoding="utf-8-sig")
importance.to_csv(HERE / "feature_importance.csv", index=False, encoding="utf-8-sig")
print("분할:", len(train), len(valid), len(test))
print(comparison.round(3).to_string(index=False))
print("중요도")
print(importance.round(3).to_string(index=False))
print("저장: classification_comparison.csv, cv_scores.csv, validation_predictions.csv, feature_importance.csv")
print("test는 학습·변환·예측·평가하지 않았습니다.")
