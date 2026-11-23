"""공통 체크포인트: 문서별 파싱을 테스트 가능한 단위로 제공합니다.

이 파일은 이전 실습 미완료자가 다음 교시에 참여하도록 지원합니다.
강사가 과제로 지정한 tasks.py/main.py의 TODO를 대신한 것은 아닙니다.
"""
from __future__ import annotations
import hashlib
import re
from pathlib import Path
from .io import DATA, load_json


def raw_manifest() -> list[dict]:
    return load_json(DATA / 'manifest.json')


def by_doc(doc_id: str) -> dict:
    rows = [r for r in raw_manifest() if r['doc_id'] == doc_id]
    if len(rows) != 1:
        raise ValueError(f"doc_id not found/unique: {doc_id}")
    return rows[0]


def raw_path(doc: dict) -> Path:
    # 파일명에는 수강생 제공의 고정 manifest 값만 사용합니다.
    p = (DATA / 'raw' / doc['file']).resolve()
    p.relative_to((DATA / 'raw').resolve())
    return p


def sha_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def parse_markdown_units(text: str, source_name: str) -> list[dict]:
    """수업의 Markdown 제목(#) 구간을 ParsedUnit으로 추출합니다.

    v1과 개정 v2에 같은 구현을 사용합니다. 복잡한 Markdown 전체
    (fenced code 안의 # 등)를 완벽히 파싱하는 범용 Parser는 아닙니다.
    """
    sections=[]; title=''; lines=[]
    for line in text.splitlines():
        if line.startswith('#') and re.match(r'^#{1,6}\s+',line):
            if lines and '\n'.join(lines).strip():
                sections.append((title,'\n'.join(lines).strip()))
            title=line.lstrip('#').strip(); lines=[]
        else:
            lines.append(line)
    if lines and '\n'.join(lines).strip():
        sections.append((title,'\n'.join(lines).strip()))
    return [{'unit_id':f'sec-{i}', 'page_number':None,
             'section_title':section_title,'source_locator':f"{source_name}#sec-{i}",
             'raw_text':body} for i,(section_title,body) in enumerate(sections,1)]


def parse_one(doc: dict) -> dict:
    """문서 1개를 파싱하고 출처 단위와 상태를 반환합니다.

    PDF의 빈 추출이 곧 OCR 대상임을 단정하지 않습니다. 여기서 scan.pdf는
    제작 시 이미지 PDF임을 알고 있으므로 해당 예제에 한해 needs_ocr 상태를 줍니다.
    """
    path = raw_path(doc)
    common = {k: doc[k] for k in ('doc_id','category','source_version')}
    common['source_uri'] = str(path.relative_to(DATA)).replace('\\','/')
    if not path.exists():
        return {'doc':common,'status':'not_found','units':[],'reason':'file_not_found'}
    kind = path.suffix.lower()
    try:
        if kind == '.txt':
            text=path.read_bytes().decode('utf-8-sig')
            units=[{'unit_id':'text-1','page_number':None,'section_title':'',
                    'source_locator':doc['file'], 'raw_text':text}]
        elif kind == '.md':
            text=path.read_bytes().decode('utf-8-sig')
            units=parse_markdown_units(text,doc['file'])
        elif kind == '.html':
            from bs4 import BeautifulSoup
            soup=BeautifulSoup(path.read_text(encoding='utf-8-sig'), 'html.parser')
            main=soup.select_one('main')
            if main is None:
                return {'doc':common,'status':'parse_error','units':[], 'reason':'main_not_found'}
            for tag in main.select('script, style'):tag.decompose()
            segments=[]
            for child in main.find_all(recursive=False):
                if child.name == 'table':
                    trs=child.find_all('tr')
                    headers=[cell.get_text(' ',strip=True) for cell in (trs[0].find_all(['th','td']) if trs else [])]
                    for tr in trs[1:]:
                        values=[cell.get_text(' ',strip=True) for cell in tr.find_all(['th','td'])]
                        segments.append(' | '.join(f'{h}: {v}' for h,v in zip(headers,values)))
                else:
                    t=child.get_text(' ',strip=True)
                    if t:segments.append(t)
            units=[{'unit_id':'main-1','page_number':None,'section_title':'시설 안내',
                    'source_locator':f"{doc['file']}#main", 'raw_text':'\n'.join(segments)}]
        elif kind == '.pdf':
            from pypdf import PdfReader
            reader=PdfReader(str(path))
            units=[{'unit_id':f'page-{i}','page_number':i,'section_title':'',
                    'source_locator':f"{doc['file']}#page={i}",
                    'raw_text':page.extract_text() or ''} for i,page in enumerate(reader.pages,1)]
        else:
            return {'doc':common,'status':'unsupported','units':[], 'reason':f'unsupported:{kind}'}
    except (OSError,UnicodeError,ValueError,ImportError) as exc:
        return {'doc':common,'status':'parse_error','units':[], 'reason':type(exc).__name__}
    if not any(unit['raw_text'].strip() for unit in units):
        state='needs_ocr' if doc['file']=='scan.pdf' else 'empty_text_review'
        return {'doc':common,'status':state,'units':units,'reason':'image_only_known_fixture' if state=='needs_ocr' else 'inspect_original'}
    return {'doc':common,'status':'parsed','units':units,'reason':None}
