"""강사용 검수 도구. 작성되지 않은 수강생 TODO를 자동으로 풀지 않습니다."""
from pathlib import Path
import subprocess,sys,argparse
ROOT=Path(__file__).resolve().parents[1]
LEVELS=['01_basic','02_intermediate','03_advanced']

def main():
 p=argparse.ArgumentParser();p.add_argument('--level',choices=LEVELS,default='01_basic');p.add_argument('--offline',action='store_true');a=p.parse_args()
 for exercise in sorted((ROOT/a.level).glob('[0-9][0-9]_*')):
    script=exercise/'main.py'
    if not script.exists():continue
    argv=[sys.executable,str(script)]
    if a.offline:argv+=['--offline']
    print('\n====',exercise.name,'====',flush=True)
    result=subprocess.run(argv,cwd=ROOT)
    if result.returncode:raise SystemExit(result.returncode)
if __name__=='__main__':main()
