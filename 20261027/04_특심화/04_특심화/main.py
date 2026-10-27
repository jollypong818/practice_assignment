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

def importance_bias_demo(seed=42):
    """공통100건을 변경하지 않는 별도 합성320건 실험. raw4 대신 3개 수치열.
    반환: 학습 MDI / holdout 순열 F1감소 표. 순위 방향을 강제로 만들지 않는다.
    """
    # TODO D7-04-H1: 위 함수 설명과 README 계약에 맞게 구현하세요.
    raise NotImplementedError("TODO D7-04-H1")

def run():
    return {'separate_bias_experiment':importance_bias_demo(),
        'not_main_dataset':True,
        'warning':'복제열은 중요도를 나눠 가질 수 있다. 잡음열의 특정 순위를 보장하지 않는다. 이 결과로 공통 데이터의 열을 삭제하지 않는다.'}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path(__file__).resolve().parent/'outputs')
    args = parser.parse_args()
    emit(run(), args.output)

if __name__ == '__main__':
    main()
