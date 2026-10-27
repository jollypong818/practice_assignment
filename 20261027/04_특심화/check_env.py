"""실습 환경 점검. 시스템·전역 설정이나 파일은 수정하지 않습니다."""
import sys,platform,importlib.metadata as md
from pathlib import Path
names=['numpy','pandas','scikit-learn','scipy','joblib','threadpoolctl','xgboost']
print('Python:',platform.python_version());print('실행기:',sys.executable)
print('CPU 실습입니다. CUDA/GPU는 필요하지 않습니다.')
missing=[]
for name in names:
    try: print(f'{name}: {md.version(name)}')
    except md.PackageNotFoundError: missing.append(name)
if missing:
    print('미설치:',', '.join(missing));print('python -m pip install -r requirements.txt');sys.exit(1)
try:
    import numpy,pandas,sklearn,xgboost
    from xgboost import XGBClassifier
    import numpy as np
    X=np.array([[0],[1],[2],[3]]);y=np.array([0,0,1,1])
    m=XGBClassifier(n_estimators=2,max_depth=1,n_jobs=1,tree_method='hist',device='cpu').fit(X,y)
    print('XGBoost CPU fit/predict:',m.predict([[1]]).tolist())
except Exception as e:
    print('패키지 import/실행 실패:',type(e).__name__,str(e));sys.exit(1)
print('환경 확인 완료. 검증 조합은 requirements-lock.txt를 확인하세요.')
