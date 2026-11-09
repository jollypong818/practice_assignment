from pathlib import Path
import json
import re
import numpy as np
import pandas as pd
import cv2
base = Path(__file__).resolve().parent
data = base / 'data'
out = base / 'outputs'
out.mkdir(exist_ok=True)
lesson = json.loads((data / 'lesson.json').read_text(encoding='utf-8'))

# TensorRT 10.x와 11.x의 정밀도 옵션은 다릅니다. 명령 문자열만 기록합니다.
manifest = {'status':'DESIGN_ONLY', 'tensorrt_major':10, 'input_name':'images', 'dtype':'float32', 'min':[1,3,224,224], 'opt':[4,3,224,224], 'max':[8,3,224,224], 'hardware_verified':False, 'engine_sha256':None}
# TODO A06
command = []
# TODO 끝 A06
manifest['example_for_trt10_only'] = command
manifest['trt11_note'] = '11.x는 --fp16 제거. ONNX 정밀도 변환을 사전에 하고 설치 버전의 help를 확인.'
(out / 'p06_engine_manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
print('설계만:', ' '.join(command))
print(manifest['trt11_note'])
