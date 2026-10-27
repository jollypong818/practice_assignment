"""실습08: 앞서 작성한 실습07 프로젝트의 출력 검증. 새 프로젝트를 만들지 않습니다."""
from pathlib import Path
import sys
import argparse
import json
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[2]
PROJECT=ROOT/'ex07_project'/'03_심화'/'day7_ensemble'
sys.path.insert(0,str(PROJECT))
from course_support import load_data, write_json

def verify_cv_table(scores):
    """모델·task마다 fold1~5,48/12,유한점수, 분류F1[0,1]/회귀RMSE>=0 검사."""
    # TODO D7-08-V1: 위 계약과 README를 읽고 구현하세요.
    raise NotImplementedError("TODO D7-08-V1")

def verify_predictions(predictions,d):
    """각 모델/task당 valid20개 순서, 실제 정답 일치, test ID 미포함 검사."""
    # TODO D7-08-V2: 위 계약과 README를 읽고 구현하세요.
    raise NotImplementedError("TODO D7-08-V2")

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--project',type=Path,default=PROJECT)
    args=p.parse_args(); out=args.project/'outputs'
    d=load_data(args.project/'data')
    summary=json.loads((out/'run_summary.json').read_text(encoding='utf-8'))
    if summary['test_evaluated'] is not False: raise ValueError('test 평가 금지')
    scores=pd.read_csv(out/'cv_scores.csv',encoding='utf-8-sig')
    predictions=pd.read_csv(out/'validation_predictions.csv',encoding='utf-8-sig')
    result={'cv_table':verify_cv_table(scores),'predictions':verify_predictions(predictions,d),
            'test_not_evaluated':True}
    write_json(out/'submission_check.json',result)
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
