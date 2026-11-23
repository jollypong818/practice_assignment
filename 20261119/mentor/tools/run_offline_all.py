"""각 수준·8개 실습을 새 Python 프로세스로 검증합니다.
멘티 파일이 TODO 미완성일 때 실패하는 것이 정상입니다.
"""
import subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
failed=[]
for level in ('01_basic','02_intermediate','03_advanced'):
    for exercise in sorted((ROOT/level).glob('[0-9][0-9]_*')):
        status=subprocess.run([sys.executable,'main.py'],cwd=exercise,capture_output=True,text=True)
        print(('OK' if status.returncode==0 else 'TODO / FAIL'),exercise.relative_to(ROOT))
        if status.returncode:failed.append(str(exercise.relative_to(ROOT)))
print('Success:',24-len(failed),'/ 24')
if failed:print('Not completed:',*failed,sep='\n - ')
raise SystemExit(1 if failed else 0)
