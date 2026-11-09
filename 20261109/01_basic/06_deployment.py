"""실습 06: 배포 흐름의 설계 기록입니다. ONNX·TensorRT 엔진을 실행하지 않습니다."""
from pathlib import Path
import json

base = Path(__file__).resolve().parent
# TODO B07
stages = []
# TODO 끝 B07
plan = {'stages': stages, 'status': 'DESIGN_ONLY', 'target_device': None, 'tensorrt_version': None, 'engine_sha256': None, 'latency_ms': None, 'checked_on_hardware': False}
(base / 'p06_deployment_plan.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding='utf-8')
print(' -> '.join(stages))
print('DESIGN_ONLY: 오늘은 설계 기록. Tesseract 자체를 ONNX로 변환하는 예제가 아닙니다.')
