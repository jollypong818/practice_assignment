"""완성한 전체 실습의 실행·수치·프로젝트 계약을 재검사합니다. 약1~3분/PC에 따라 다름.
미완성 수강생코드는 실패가 정상입니다. 먼저 check_exercise.py로 개별 단계를 검사하세요.
"""
from pathlib import Path
import argparse,subprocess,sys,os,tempfile,json,time
ROOT=Path(__file__).resolve().parents[1]

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--include-bonus',action='store_true')
    args=p.parse_args();records=[]
    env={**os.environ,'PYTHONUTF8':'1','PYTHONIOENCODING':'utf-8','OMP_NUM_THREADS':'1',
         'OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'1'}
    def run(label,command,cwd=ROOT):
        start=time.time()
        r=subprocess.run([sys.executable,*map(str,command)],cwd=cwd,env=env,capture_output=True,text=True)
        records.append({'label':label,'returncode':r.returncode,'seconds':round(time.time()-start,3),
                        'stdout':r.stdout,'stderr':r.stderr})
        print(('PASS ' if r.returncode==0 else 'FAIL ')+label,flush=True)
        if r.returncode: print(r.stderr[-2500:],r.stdout[-2500:],flush=True)
    run('데이터/입력/CV 계약25개',['tools/test_contracts.py'])
    for ex in range(1,7):
        for level in ['basic','applied','advanced']:
            run(f'실습{ex:02d}/{level}',['tools/check_exercise.py','--exercise',ex,'--level',level])
    for lev in ['01_기본필수','02_응용','03_심화']:
        project=ROOT/'ex07_project'/lev/'day7_ensemble'
        run(f'프로젝트/{lev}',[project/'main.py'])
        run(f'프로젝트 계약12개/{lev}',['-m','unittest','-v','test_project.py'],project)
        run(f'제출검증/{lev}',[ROOT/'ex08_verify'/lev/'verify.py'])
        if lev!='01_기본필수':run(f'새 프로세스 복원/{lev}',[project/'restore_check.py','--trust-local-models'])
    if args.include_bonus:run('선택심화 조기종료',[ROOT/'bonus_early_stopping'/'main.py'])
    out=ROOT/'검수_실행결과.json';out.write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
    failed=sum(r['returncode']!=0 for r in records)
    print(f'검사 실행 {len(records)}건 / 실패 {failed}건 / 기록 {out.name}')
    sys.exit(1 if failed else 0)
if __name__=='__main__': main()
