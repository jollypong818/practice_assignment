"""실제 수동 응답만 등록합니다. API를 호출하지 않습니다."""
from pathlib import Path
import sys
import argparse
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from coursekit.experiments import record_manual
from coursekit.io import run

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--run-dir',type=Path,required=True)
    p.add_argument('--slot',required=True)
    p.add_argument('--raw-file',type=Path)
    p.add_argument('--model-label',default='미확인')
    p.add_argument('--state',choices=['completed','refused','incomplete','failed'],default='completed')
    p.add_argument('--conditions',default='미확인')
    p.add_argument('--reason',default='')
    p.add_argument('--attempt',type=int,choices=[1,2],default=1)
    p.add_argument('--observed-at',help='관찰 시각 예: 2026-11-16T14:35:00+09:00. 모르면 생략')
    a=p.parse_args()
    record_manual(a.run_dir,a.slot,a.raw_file,a.model_label,a.state,a.conditions,a.reason,a.attempt,a.observed_at)
    print('원문과 실행 정보를 보존했습니다. review로 확인하고 사람 평가를 따로 채우세요.')
if __name__=='__main__':
    run(main)
