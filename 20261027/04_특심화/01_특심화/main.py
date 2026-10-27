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

def compare_label_change(X, y, changed_index):
    """원본 보존. 지정 정답을 1-y로 바꿔 두 깊이1 모델의 조건과 예측을 비교한다."""
    # TODO D7-01-H1: 위 함수 설명과 README 계약에 맞게 구현하세요.
    raise NotImplementedError("TODO D7-01-H1")

def run():
    X=np.array([[100],[200],[300],[700],[800],[900]])
    y=np.array([0,0,0,1,1,1]); before=y.copy()
    result=compare_label_change(X,y,2)
    return {'sensitivity':result,'original_preserved':bool(np.array_equal(y,before)),
        'training_range':[100,900],'extrapolation_query':1200}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path(__file__).resolve().parent/'outputs')
    args = parser.parse_args()
    emit(run(), args.output)

if __name__ == '__main__':
    main()
