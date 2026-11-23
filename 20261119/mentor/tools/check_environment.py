"""실습 실행 인터프리터/데이터/선택 패키지를 확인합니다. 설치나 DB 변경을 하지 않습니다."""
from pathlib import Path
import importlib.util
import sys
ROOT=Path(__file__).resolve().parents[1]
print('Python:',sys.version.split()[0]);print('Interpreter:',sys.executable)
print('Data files:',[p.name for p in sorted((ROOT/'data'/'raw').iterdir())])
for name in ('pypdf','bs4','pytest','psycopg','pgvector','sentence_transformers','dotenv'):
    print(name, 'installed' if importlib.util.find_spec(name) else 'missing')
print('PostgreSQL server:', 'not_checked (requires connection)')
print('E5 model:', 'not_checked (requires actual load)')
