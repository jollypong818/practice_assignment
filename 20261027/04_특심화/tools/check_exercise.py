"""완성한 실습01~06을 임시 폴더에서 실행하고 기대 결과와 대조합니다.
실행 예: python tools/check_exercise.py --exercise 1 --level basic
"""
from pathlib import Path
import sys,argparse,subprocess,tempfile,json,math,os
ROOT=Path(__file__).resolve().parents[1]
NAMES={1:'tree',2:'overfitting',3:'forest',4:'importance',5:'xgboost',6:'cv'}
LEVELS={'basic':'01_기본필수','applied':'02_응용','advanced':'03_심화'}

def differences(a,b,path='root',atol=0.001):
    result=[]
    if isinstance(a,dict) and isinstance(b,dict):
        if set(a)!=set(b): return [f'{path}: 키 불일치']
        for k in a: result+=differences(a[k],b[k],path+'.'+k,atol)
    elif isinstance(a,list) and isinstance(b,list):
        if len(a)!=len(b): return [f'{path}: 길이 {len(a)} != {len(b)}']
        for i,(x,y) in enumerate(zip(a,b)): result+=differences(x,y,f'{path}[{i}]',atol)
    elif isinstance(a,(int,float)) and isinstance(b,(int,float)) and not isinstance(a,bool) and not isinstance(b,bool):
        if not math.isclose(a,b,rel_tol=1e-6,abs_tol=atol): result.append(f'{path}: {a} != {b}')
    elif a!=b: result.append(f'{path}: {a!r} != {b!r}')
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--exercise',type=int,choices=range(1,7),required=True)
    p.add_argument('--level',choices=LEVELS,default='basic')
    args=p.parse_args()
    folder=ROOT/f'ex{args.exercise:02d}_{NAMES[args.exercise]}'/LEVELS[args.level]
    env={**os.environ,'PYTHONUTF8':'1','PYTHONIOENCODING':'utf-8','OMP_NUM_THREADS':'1'}
    with tempfile.TemporaryDirectory(prefix='day7_check_') as temp:
        done=subprocess.run([sys.executable,str(folder/'main.py'),'--output',temp],capture_output=True,text=True,env=env)
        if done.returncode:
            print(done.stderr);print('미완성 TODO 또는 실행 오류를 먼저 수정하세요.');sys.exit(1)
        actual=json.loads((Path(temp)/'result.json').read_text(encoding='utf-8'))
        expected=json.loads((folder/'expected_outputs'/'result.json').read_text(encoding='utf-8'))
        errors=differences(actual,expected)
        if errors:
            print('불일치:',*errors[:15],sep='\n');print('환경 버전·자료/순서·설정을 확인하세요.');sys.exit(1)
    print(f'통과: 실습{args.exercise:02d}/{args.level} — 표시된 기준 결과와 일치')
    print('이 검사는 정답 하드코딩을 판별하는 채점기가 아닙니다. 다른 입력과 구현 과정도 설명하세요.')
if __name__=='__main__': main()
