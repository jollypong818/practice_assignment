"""선택: 이미 실행 중인 지식 API를 GET으로 읽어 새 스냅샷을 만듭니다. 기본 실습은 고정 JSON 사용."""
from pathlib import Path
import argparse
import sys
import json
from urllib.request import urlopen
from urllib.error import URLError
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from coursekit.prompting import build_context
from coursekit.io import write_json, run

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--url',default='http://127.0.0.1:8000/api/knowledge')
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args()
    if a.out.exists():
        raise ValueError('기존 스냅샷은 덮어쓰지 않습니다. 새 이름을 사용하세요.')
    if not a.url.startswith(('http://127.0.0.1:','http://localhost:')):
        raise ValueError('이 수업 도구는 개인 PC의 localhost 지식 API만 조회합니다.')
    try:
        with urlopen(a.url,timeout=5) as response:
            raw=response.read(1_000_001)
    except (URLError,TimeoutError):
        raise ValueError('기존 지식 API 연결 실패. 고정 knowledge_v1.json으로 계속할 수 있습니다.') from None
    if len(raw)>1_000_000:
        raise ValueError('스냅샷 크기 제한을 넘었습니다.')
    rows=json.loads(raw.decode('utf-8'))
    build_context(rows,[r['id'] for r in rows])
    write_json(a.out,rows)
    print('실제 id를 보존했습니다. 새 스냅샷에는 별도 질문·선택 ID·버전이 필요합니다.')
if __name__=='__main__':run(main)
