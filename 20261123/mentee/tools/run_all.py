"""한 수준의 8개 실습을 로컬 모드로 점검합니다. 실제 LLM/DB를 호출하지 않습니다."""
from pathlib import Path
import argparse
import os
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1]
LEVELS=("01_basic","02_intermediate","03_advanced")

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--level",choices=LEVELS,default="01_basic")
    p.add_argument("--all-levels",action="store_true")
    p.add_argument("--tests",action="store_true",help="main 실행 대신 각 폴더의 pytest 실행")
    args=p.parse_args()
    failures=[]
    levels=LEVELS if args.all_levels else [args.level]
    env=os.environ.copy()
    env["PYTHONIOENCODING"]="utf-8"
    env["PYTHONUTF8"]="1"
    env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"]="1"
    for level in levels:
        for folder in sorted((ROOT/level).iterdir()):
            if not (folder/"main.py").is_file():
                continue
            command=[sys.executable,"-m","pytest","-q","tests"] if args.tests else [sys.executable,"main.py"]
            if not args.tests and folder.name[:2] in {"05","06","08"}:
                command.append("--offline")
            print(f"\n[{level}/{folder.name}]",flush=True)
            result=subprocess.run(command,cwd=folder,env=env,check=False)
            if result.returncode:
                failures.append(f"{level}/{folder.name}")
    print("\n미완료/실패:",len(failures))
    for name in failures:
        print(" -",name)
    if failures:
        print("mentee의 미완성 TODO는 실패가 정상입니다. 최초 오류의 D26 ID부터 확인하세요.")
    raise SystemExit(1 if failures else 0)

if __name__=="__main__":
    main()
