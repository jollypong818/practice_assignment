"""새 프로세스 복원 확인. 반드시 본인이 생성한 출력에만 --trust-local-models 사용."""
from pathlib import Path
import argparse
import json
import numpy as np
from course_support import load_data, write_json
ROOT=Path(__file__).resolve().parent

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--trust-local-models',action='store_true')
    p.add_argument('--data-dir',type=Path,default=ROOT/'data')
    p.add_argument('--output',type=Path,default=ROOT/'outputs')
    args=p.parse_args()
    if not args.trust_local_models: p.error('본인이 생성한 모델일 때만 --trust-local-models를 지정하세요.')
    import joblib
    import pandas as pd
    d=load_data(args.data_dir)
    summary=json.loads((args.output/'run_summary.json').read_text(encoding='utf-8'))
    saved=pd.read_csv(args.output/'validation_predictions.csv',encoding='utf-8-sig')
    checks={}
    for task,name in summary['choices_by_CV'].items():
        model=joblib.load(args.output/f'{task}_pipeline.joblib')
        rows=saved[(saved['task']==task)&(saved['model']==name)].set_index('request_id')
        before=rows.loc[d.X_valid.index,'predicted'].to_numpy()
        checks[task]=bool(np.allclose(model.predict(d.X_valid),before))
        if not checks[task]: raise AssertionError(f'{task}: 새 프로세스 복원 예측 불일치')
    write_json(args.output/'fresh_process_restore.json',checks)
    print(json.dumps(checks,ensure_ascii=False))
if __name__=='__main__': main()
