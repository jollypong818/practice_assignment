"""선택 심화: 기본 비교와 분리된 TreeGrid 실험. 결과는 선택 편향을 포함합니다."""
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from preprocessing import make_preprocessor
from course_support import write_json

def run_search(d,folds,output):
    """4후보×5fold + train60 refit. 반환: fit된 grid. test/valid로 탐색하지 않는다."""
    # TODO D7-07-H1: 위 계약과 README를 읽고 구현하세요.
    raise NotImplementedError("TODO D7-07-H1")
    cols=['param_model__max_depth','param_model__min_samples_leaf',
          'mean_test_score','std_test_score','rank_test_score']
    pd.DataFrame(grid.cv_results_)[cols].to_csv(output/'separate_tree_grid.csv',index=False,encoding='utf-8-sig')
    write_json(output/'separate_tree_grid.json',{'name':'TreeGrid','best_params':grid.best_params_,
        'best_CV_F1':float(grid.best_score_),'basic_table_replaced':False,'test_evaluated':False})
    return grid
