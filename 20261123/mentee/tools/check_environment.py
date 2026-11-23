"""패키지 버전만 확인합니다. API·DB·모델 다운로드는 실행하지 않습니다."""
from importlib.metadata import version, PackageNotFoundError
from pathlib import Path
import argparse
import sys

GROUPS={
    "base":["langchain-core","pydantic","fastapi","httpx","python-dotenv","uvicorn"],
    "llm":["langchain-core","pydantic","langchain-openai","openai","python-dotenv"],
    "live":["sentence-transformers","torch","numpy","psycopg","pgvector","python-dotenv"],
    "test":["pytest"],
}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--group",choices=[*GROUPS,"all"],default="base")
    args=parser.parse_args()
    print("Python:",sys.version.split()[0])
    print("실행 파일:",sys.executable)
    print("현재 역할 폴더:",Path(__file__).resolve().parents[1])
    packages=list(dict.fromkeys(sum(GROUPS.values(),[]))) if args.group=="all" else GROUPS[args.group]
    missing=[]
    for package in packages:
        try:
            print(package,version(package))
        except PackageNotFoundError:
            missing.append(package)
            print(package,"미설치")
    if sys.version_info < (3,11):
        raise SystemExit("이 패키지는 Python 3.11 이상을 기준으로 작성했습니다.")
    if missing:
        print("현재 인터프리터에서 찾지 못한 패키지:",", ".join(missing))
        print("docs/SETUP_WINDOWS.md에서 해당 requirements 파일을 확인하세요.")
        raise SystemExit(1)
    print("패키지 확인 완료. 실제 인증·DB 접속·모델 추론 성공을 뜻하지 않습니다.")

if __name__=="__main__":
    main()
