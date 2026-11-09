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

rows = []
for name, doc in lesson['documents'].items():
    for item in doc['mock_vlm']['responses']:
# TODO A05
        exact = False
# TODO 끝 A05
        grounded = item['evidence'] in doc['ocr']['text']
        rows.append({'document_id':name, 'field':item['field'], 'backend':'mock', 'exact':exact, 'evidence_found':grounded, 'review':not grounded})
table = pd.DataFrame(rows)
table.to_csv(out / 'p05_scores.csv', index=False, encoding='utf-8-sig')
print('값 일치:', int(table['exact'].sum()), '/', len(table))
print('값과 문자열 근거:', int((table['exact'] & table['evidence_found']).sum()), '/', len(table))
print('추론 지연시간: N/A (mock)')
