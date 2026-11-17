"""선택한 Python과 로컬 검사 패키지를 확인합니다. API 키를 읽지 않습니다."""
import sys
from importlib.metadata import version, PackageNotFoundError
print('Python:',sys.version)
print('Interpreter:',sys.executable)
if sys.version_info < (3,10):
    raise SystemExit('Python 3.10 이상이 필요합니다.')
try:
    v=version('pydantic'); print('pydantic:',v)
except PackageNotFoundError:
    raise SystemExit('python -m pip install -r requirements.txt 를 실행하세요.')
if not v.startswith('2.'):
    raise SystemExit('Pydantic v2 환경을 선택하세요.')
try: print('pytest (선택):',version('pytest'))
except PackageNotFoundError: print('pytest: 미설치 — 기본필수 수동 확인에는 불필요')
print('로컬 검사는 CPU·Python으로 실행합니다. 실제 A/B 관찰은 별도의 모델 화면에서 수행합니다.')
