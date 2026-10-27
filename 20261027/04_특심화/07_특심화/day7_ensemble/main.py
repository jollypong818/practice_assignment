"""Day7 앙상블 비교 프로젝트. 모든 상대경로는 이 파일 위치를 기준으로 합니다."""
from pathlib import Path
import argparse
import json
import numpy as np
import pandas as pd
from course_support import load_data, write_json, environment, sha256
from model_config import make_folds, fold_table
from preprocessing import candidates
from evaluate import run_candidate, importance_table, choose_by_cv
from checks import verify_development_data, boundary_checks
ROOT=Path(__file__).resolve().parent
DEFAULT_LEVEL=3

def run_project(data_dir=ROOT/'data', output=ROOT/'outputs', level=DEFAULT_LEVEL):
    if level not in (1,2,3): raise ValueError('level은 1~3')
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    d=load_data(data_dir); integrity=verify_development_data(d)
    cls_folds=make_folds(d.X_train,d.yc_train)
    tasks=['classification'] if level==1 else ['classification','regression']
    comparisons={}; models={}; all_scores=[]; all_pred=[]; all_folds=[]; choices={}
    # TODO D7-07-M1: 위 계약과 README를 읽고 구현하세요.
    raise NotImplementedError("TODO D7-07-M1")
    for task,table in comparisons.items():
        table.to_csv(output/f'{task}_comparison.csv',index=False,encoding='utf-8-sig')
    pd.concat(all_scores,ignore_index=True).to_csv(output/'cv_scores.csv',index=False,encoding='utf-8-sig')
    pd.concat(all_pred,ignore_index=True).to_csv(output/'validation_predictions.csv',index=False,encoding='utf-8-sig')
    pd.concat(all_folds,ignore_index=True).to_csv(output/'fold_manifest.csv',index=False,encoding='utf-8-sig')
    importance=importance_table(models[('classification','Forest')],d,include_permutation=level>=2)
    importance.to_csv(output/'feature_importance.csv',index=False,encoding='utf-8-sig')
    check=boundary_checks(models[('classification',choices['classification'])],d)
    if level>=2:
        import joblib
        # 직접 생성한 파일만 같은 환경에서 복원합니다. 외부 pickle/joblib은 로드하지 않습니다.
        for task,name in choices.items():
            filename=output/f'{task}_pipeline.joblib'
            joblib.dump(models[(task,name)],filename)
            restored=joblib.load(filename)
            a=models[(task,name)].predict(d.X_valid); b=restored.predict(d.X_valid)
            if not np.allclose(a,b): raise AssertionError('저장·복원 예측 불일치')
        write_json(output/'persistence_check.json',{'same_predictions':True,'trusted_local_files_only':True})
    if level>=3:
        # 별도 탐색 실험은 기본 비교표를 변경하지 않습니다.
        from search_extension import run_search
        run_search(d,cls_folds,output)
    summary={'level':level,'choices_by_CV':choices,'tie_rule':'候補宣言順 (完全同点時)',
        'integrity':integrity,'boundary_checks':check,'test_evaluated':False,
        'selection_metric':{'classification':'mean fold F1','regression':'mean fold RMSE'},
        'data_sha256':d.source_hashes,'versions':environment(),
        'warnings':['CVは選択用。validも前日から反復診断され独立最終評価ではない。',
                    '重要度は因果関係ではない。validの重要度で特性を自動削除しない。']}
    write_json(output/'run_summary.json',summary)
    print(json.dumps(summary,ensure_ascii=False,indent=2))
    return summary

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--data-dir',type=Path,default=ROOT/'data')
    p.add_argument('--output',type=Path,default=ROOT/'outputs')
    p.add_argument('--level',type=int,choices=[1,2,3],default=DEFAULT_LEVEL)
    args=p.parse_args()
    run_project(args.data_dir,args.output,args.level)
if __name__=='__main__': main()
