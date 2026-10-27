"""CV·valid·해석. train 내부 CV와 외부 valid의 역할을 분리합니다."""
import json
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.model_selection import cross_validate
from sklearn.inspection import permutation_importance
from course_support import cls_metrics, reg_metrics, snapshot, json_ready

def run_candidate(name, pipe, d, folds, task='classification'):
    """행 dict, fold DataFrame, 검증예측 DataFrame, train60으로 fit한 Pipeline 반환.
    CV는 clone으로 fold 안에서 fit; valid는 train60으로 별도 fit한 모델로만 예측.
    보관 test의 입력·정답은 받지 않습니다.
    """
    is_cls=(task=='classification')
    yt=d.yc_train if is_cls else d.yr_train
    yv=d.yc_valid if is_cls else d.yr_valid
    scorer='f1' if is_cls else 'neg_root_mean_squared_error'
    # TODO D7-07-E1: 위 계약과 README를 읽고 구현하세요.
    raise NotImplementedError("TODO D7-07-E1")
    metric='F1' if is_cls else 'RMSE_ms'
    valid=cls_metrics(yv,pred) if is_cls else reg_metrics(yv,pred)
    train=cls_metrics(yt,fitted.predict(d.X_train)) if is_cls else reg_metrics(yt,fitted.predict(d.X_train))
    row={'model':name,'task':task,'scaling':'none' if name in ['Tree','Forest','XGB'] else 'standard',
         'CV_mean':float(scores.mean()),'CV_std':float(scores.std(ddof=0)),
         'CV_metric':metric,'train_primary':train[metric],
         **{'valid_'+k:v for k,v in valid.items()},
         'params':json.dumps(json_ready(fitted['model'].get_params()),ensure_ascii=False,sort_keys=True)}
    fold_rows=[]
    for i,((a,b),score,tr,fold_model) in enumerate(zip(folds,scores,train_scores,cv['estimator']),1):
        expected=d.X_train.iloc[a][['input_chars','allowed_tools']].median().to_numpy()
        actual=fold_model['pre'].named_transformers_['num']['imputer'].statistics_
        # 이 검사는 모든 단계에 제공합니다. 06의 통계 감사에서도 같은 원리를 구현합니다.
        if not np.allclose(expected,actual): raise AssertionError('fold外の中央値を使用')
        fold_rows.append({'task':task,'model':name,'fold':i,'fit_n':len(a),'eval_n':len(b),
            'metric':metric,'score':float(score),'train_score':float(tr),'median_audit_passed':True})
    predictions=pd.DataFrame({'request_id':d.X_valid.index,'task':task,'model':name,
                              'actual':yv.to_numpy(),'predicted':pred})
    if is_cls:
        pindex=list(fitted.classes_).index(1)
        predictions['failure_probability']=fitted.predict_proba(d.X_valid)[:,pindex]
    else: predictions['residual_ms']=yv.to_numpy()-pred
    return row,pd.DataFrame(fold_rows),predictions,fitted

def importance_table(forest, d, include_permutation=False):
    """train MDI 8행. 응용이면 valid 원본 4열 순열 진단 4행 추가. 인과/특성선택 아님."""
    # TODO D7-07-E2: 위 계약과 README를 읽고 구현하세요.
    raise NotImplementedError("TODO D7-07-E2")

def choose_by_cv(table, task='classification'):
    """F1 평균 최대 / RMSE 평균 최소. 정확히 동점이면 사전 후보 순서 우선.
    valid 점수는 함수에서 참조하지 않습니다. 선택점수는 최종 성능이 아닙니다.
    """
    # TODO D7-07-E3: 위 계약과 README를 읽고 구현하세요.
    raise NotImplementedError("TODO D7-07-E3")
