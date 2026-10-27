"""실습 03: 여러 트리를 결합하는 Random Forest를 실행합니다."""
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

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score

# 제공: 작은 숲 20개, 깊이 3. 오늘은 설정을 더 늘리지 않습니다.
model = RandomForestClassifier(n_estimators=20, max_depth=3, random_state=42, n_jobs=1)
# TODO B03: train으로 학습하고 valid를 예측하세요.
pass
prediction = None
# TODO 끝
print("트리 수:", len(model.estimators_))
print("valid 예측:", prediction.tolist())
print("valid F1:", round(f1_score(y_valid, prediction, zero_division=0), 3))
