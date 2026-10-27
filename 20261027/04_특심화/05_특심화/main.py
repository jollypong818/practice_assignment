"""Day7 실습. 실행: python main.py. 결과: 이 폴더의 outputs/."""
from pathlib import Path
import sys
import argparse
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, export_text
from sklearn.model_selection import cross_validate, GridSearchCV
from sklearn.metrics import f1_score, log_loss
from sklearn.inspection import permutation_importance
from course_support import (load_data, build, make_pre, snapshot, emit, write_json,
    cls_metrics, reg_metrics, check_features, NUM, CAT, FEATURES)
from model_config import new_classifier, new_regressor, make_folds, fold_table

def compare_schedules(d, schedules):
    """learning_rate, n_estimators, train_F1, valid_F1, valid_logloss의 표 반환."""
    # TODO D7-05-H1: 위 함수 설명과 README 계약에 맞게 구현하세요.
    raise NotImplementedError("TODO D7-05-H1")

def run():
    schedules=[(0.05,80),(0.1,40)]
    return {'schedule_diagnostics':compare_schedules(load_data(),schedules),
        'predeclared_schedules':schedules,'fixed_max_depth':2,
        'warning':'학습률×회차가 같아도 같은 모델이 아니다. 기본XGB80을 자동 교체하지 않는 별도 진단이다.'}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path(__file__).resolve().parent/'outputs')
    args = parser.parse_args()
    emit(run(), args.output)

if __name__ == '__main__':
    main()
