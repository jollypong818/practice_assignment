"""실습 05: 5문서×3필드의 일치율을 구합니다. 정답은 평가할 때만 읽습니다."""
from pathlib import Path
import json
import re
import pandas as pd

base = Path(__file__).resolve().parent
lesson = json.loads((base / 'lesson.json').read_text(encoding='utf-8'))
rows = []
for name, doc in lesson['documents'].items():
    text = doc['ocr']['text']
    predicted = {'issued_at': re.search(r'DATE: (\d{4}-\d{2}-\d{2})', text).group(1), 'supplier': re.search(r'SUPPLIER: (.+)', text).group(1), 'total_amount': int(re.search(r'TOTAL: (\d+)', text).group(1))}
    for field in ['issued_at', 'supplier', 'total_amount']:
# TODO B06
        correct = False
# TODO 끝 B06
        rows.append({'document_id': name, 'field': field, 'predicted': predicted[field], 'correct': correct})
table = pd.DataFrame(rows)
table.to_csv(base / 'p05_field_scores.csv', index=False, encoding='utf-8-sig')
print('문서 수:', len(lesson['documents']), '필드 수:', len(table))
print('필드 일치:', int(table['correct'].sum()), '/', len(table))
print('합성 영어 문서의 기록 비교이며 일반 OCR·한국어 성능이 아닙니다.')
