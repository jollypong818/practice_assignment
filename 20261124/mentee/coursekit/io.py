"""실습 실행 위치와 관계없이 공통 데이터와 outputs 경로를 사용합니다."""
from pathlib import Path
import json
ROOT = Path(__file__).resolve().parents[1]

def load_json(name):
    return json.loads((ROOT/'data'/name).read_text(encoding='utf-8'))

def save_report(folder, name, obj):
    path=Path(folder)/'outputs'/name
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False,default=str)+'\n',encoding='utf-8')
    print('결과 기록:',path)
    return path
