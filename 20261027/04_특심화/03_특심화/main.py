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

def average_tree_probabilities(pipe, X):
    """전체 전처리 후 각 estimator의 확률을 stack하여 (행, 클래스) 평균 반환."""
    # TODO D7-03-H1: 위 함수 설명과 README 계약에 맞게 구현하세요.
    raise NotImplementedError("TODO D7-03-H1")

def run():
    d=load_data(); pipe=build(new_classifier('Forest')).fit(d.X_train,d.yc_train)
    averaged=average_tree_probabilities(pipe,d.X_valid)
    direct=pipe.predict_proba(d.X_valid)
    fake=np.array([0.51,0.51,0.01])
    return {'max_difference':float(np.max(np.abs(averaged-direct))),
        'probabilities_equal':bool(np.allclose(averaged,direct)),
        'fake_votes':int(np.sum(fake>=0.5)>1),'fake_probability_mean':float(fake.mean()),
        'fake_probability_class':int(fake.mean()>=0.5),
        'probability_check':pd.DataFrame({'request_id':d.X_valid.index,
            'tree_mean_p1':averaged[:,1],'forest_p1':direct[:,1]})}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path(__file__).resolve().parent/'outputs')
    args = parser.parse_args()
    emit(run(), args.output)

if __name__ == '__main__':
    main()
