from __future__ import annotations
import json
from pathlib import Path

def save_result(exercise_dir,name,result):
    out=Path(exercise_dir)/'outputs'
    out.mkdir(parents=True,exist_ok=True)
    path=out/name
    path.write_text(json.dumps(result,ensure_ascii=False,indent=2,default=str)+'\n',encoding='utf-8')
    return path
