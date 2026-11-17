"""통합본에서 mentee·mentor를 대조하고 임시 복사본에서 전 실습을 실행합니다.
기존 실습 폴더의 outputs와 학생 응답을 수정하지 않습니다.
실제 ChatGPT·LLM API를 실행하거나 성능을 측정하지 않습니다.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
import ast
import json
import re
import shutil
import subprocess
import sys
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

BLOCK=re.compile(r'(?ms)^(?P<indent>[ \t]*)# BEGIN (?P<id>D21-\d{2}-[BIA]\d{2})\n(?P<body>.*?)^(?P=indent)# END (?P=id)[^\n]*')
IGNORE=shutil.ignore_patterns('__pycache__','.pytest_cache','outputs','.venv','*.pyc')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path.cwd()/'verification_result.json')
    args=parser.parse_args()
    root=Path(__file__).resolve().parents[2]
    if not (root/'mentee').is_dir():
        raise SystemExit('mentee+mentor가 모두 있는 통합본에서 실행하세요.')
    compile_count=0
    for p in root.rglob('*.py'):
        if any(x in p.parts for x in ['__pycache__','outputs','.venv']):continue
        compile(p.read_text(encoding='utf-8'),str(p),'exec');compile_count+=1
    results=[]
    ids=[]
    counts=Counter()
    with TemporaryDirectory(prefix='day21_verify_') as tmp:
        work=Path(tmp)/'space path 한글'
        shutil.copytree(root,work,ignore=IGNORE)
        # 교시별 독립 프로세스를 병렬 확인합니다. 한 교시 안의 prepare/review는 순서를 지킵니다.
        def unfinished(script):
            p=subprocess.run([sys.executable,str(script)],cwd=tmp,capture_output=True,text=True,timeout=30)
            assert p.returncode==2 and '[미완성 TODO]' in p.stderr,(script,p.stdout,p.stderr)
            return {'phase':'unfinished_expected_stop','path':str(script.relative_to(work)),'passed':True}
        with ThreadPoolExecutor(max_workers=4) as pool:
            results.extend(pool.map(unfinished,sorted((work/'mentee').glob('0*/0*/main.py'))))
        print('미완성 24개 경로: 예상 TODO 중단 확인',flush=True)
        # 각 TODO의 정답 몸체를 복사하고 Python AST가 같은지 대조합니다.
        for mentee in sorted((work/'mentee').rglob('*.py')):
            relative=mentee.relative_to(work/'mentee')
            mentor=work/'mentor'/relative
            if not mentor.exists():continue
            st=mentee.read_text(encoding='utf-8'); mt=mentor.read_text(encoding='utf-8')
            solutions={m['id']:m.group(0) for m in BLOCK.finditer(mt)}
            current=list(BLOCK.finditer(st))
            if current:
                for m in current:
                    assert m['id'] in solutions
                    ids.append(m['id']);counts[relative.parts[0]]+=1
                    # basic에는 raise만 있는 블록을 허용하지 않습니다.
                    if relative.parts[0]=='01_basic':
                        meaningful=[x.strip() for x in m['body'].splitlines() if x.strip() and not x.strip().startswith(('#','raise NotImplementedError'))]
                        assert meaningful,(relative,m['id'])
                restored=BLOCK.sub(lambda m:solutions[m['id']],st)
                assert ast.dump(ast.parse(restored))==ast.dump(ast.parse(mt)),relative
                mentee.write_text(restored,encoding='utf-8')
        assert len(ids)==len(set(ids))
        assert counts['01_basic']<counts['02_intermediate']<counts['03_advanced']
        # 실제 수동 응답은 입력하지 않습니다. prepare/review는 미실행임을 확인합니다.
        def completed(script):
            commands=[[sys.executable,str(script)]]
            if script.parent.name.startswith(('05','08')):
                commands += [[sys.executable,str(script),'review'],[sys.executable,str(script),'fixtures']]
            entries=[]
            for cmd in commands:
                p=subprocess.run(cmd,cwd=tmp,capture_output=True,text=True,timeout=30)
                assert p.returncode==0,(script,cmd,p.stdout,p.stderr)
                entries.append({'phase':'completed_run','path':str(script.relative_to(work)),'args':cmd[2:],'passed':True})
            print('실행 통과:',str(script.relative_to(work)),flush=True)
            return entries
        scripts=sorted((work/'mentor').glob('0*/0*/main.py'))+sorted((work/'mentee').glob('0*/0*/main.py'))
        with ThreadPoolExecutor(max_workers=4) as pool:
            for entries in pool.map(completed,scripts):
                results.extend(entries)
        def local_test(tests):
            p=subprocess.run([sys.executable,'-m','pytest','-q',str(tests)],cwd=tests.parent,capture_output=True,text=True,timeout=40)
            assert p.returncode==0,(tests,p.stdout,p.stderr)
            return {'phase':'local_pytest','path':str(tests.relative_to(work)),'stdout':p.stdout,'passed':True}
        test_paths=sorted((work/'mentor'/'03_advanced').glob('*/tests'))+sorted((work/'mentee'/'03_advanced').glob('*/tests'))
        with ThreadPoolExecutor(max_workers=4) as pool:
            results.extend(pool.map(local_test,test_paths))
    report={'python':sys.version,'compiled_files':compile_count,'todo_count':len(ids),'todo_by_level':dict(counts),
            'entries':results,'actual_model_runs':0,'actual_api_calls':0,'windows_execution_verified':False,
            'meaning':'임시 복사본에서 코드·샘플·기록 흐름을 검사함. 실제 모델 품질은 미측정.'}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='entries'},ensure_ascii=False,indent=2))
    print('검사 실행 항목:',len(results))

if __name__=='__main__':main()
