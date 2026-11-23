"""검증된 체크포인트: 정제·청킹·위치·Coverage 기본 함수."""
from __future__ import annotations
import hashlib
import json
import re
import unicodedata


def clean_prose(text: str) -> str:
    """일반 본문 전용. 코드·TSV·표에는 구조에 맞는 별도 규칙을 사용하세요."""
    text=unicodedata.normalize('NFC',text.replace('\r\n','\n').replace('\r','\n'))
    return '\n'.join(re.sub(r'[ \t]+',' ',line).strip() for line in text.split('\n')).strip()


def char_windows(text: str, size: int, overlap: int):
    if type(size) is not int or type(overlap) is not int or not (0 <= overlap < size):
        raise ValueError('invalid chunk size or overlap')
    start=0
    while start < len(text):
        end=min(start+size,len(text))
        yield {'char_start':start,'char_end':end,'text':text[start:end]}
        if end==len(text):break
        start=end-overlap


def validate_span(chunk: dict, clean_text: str) -> None:
    a,b=chunk['char_start'],chunk['char_end']
    if type(a) is not int or type(b) is not int or not 0 <= a < b <= len(clean_text):
        raise ValueError('invalid span')
    if chunk['text'] != clean_text[a:b]:
        raise ValueError('span mismatch')
    if not chunk['text'].strip():
        raise ValueError('empty chunk')


def covered_positions(spans: list[tuple[int,int]], length: int) -> tuple[int,list[int]]:
    if length < 0:raise ValueError('invalid length')
    covered=bytearray(length)
    for a,b in spans:
        if not 0<=a<b<=length:raise ValueError('span out of range')
        covered[a:b]=b'\x01'*(b-a)
    return sum(covered),[i for i,v in enumerate(covered) if not v]


def stable_chunk_id(doc: dict, unit_id: str, pipeline_version: str, start: int, end: int) -> str:
    identity={'doc_id':doc['doc_id'],'source_version':doc['source_version'],
              'pipeline_version':pipeline_version,'unit_id':unit_id,'span':[start,end]}
    raw=json.dumps(identity,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')
    return hashlib.sha256(raw).hexdigest()


def build_chunk(doc: dict, unit: dict, clean_text: str, span: dict, pipeline_version='ingest-e5-v1') -> dict:
    validate_span(span,clean_text)
    a,b=span['char_start'],span['char_end']
    result={**{k:doc[k] for k in ('doc_id','source_version','category')},
            'pipeline_version':pipeline_version,
            'chunk_id':stable_chunk_id(doc,unit['unit_id'],pipeline_version,a,b),
            'unit_id':unit['unit_id'],'source_locator':unit['source_locator'],
            'section_title':unit.get('section_title',''), 'page_number':unit.get('page_number'),
            'char_start':a,'char_end':b,'body':span['text']}
    result['embedding_text']='passage: '+result['body']
    return result


def make_chunks(doc:dict, unit:dict, size=110, overlap=20, pipeline_version='ingest-e5-v1') -> list[dict]:
    clean=clean_prose(unit['raw_text'])
    return [build_chunk(doc,unit,clean,s,pipeline_version) for s in char_windows(clean,size,overlap)]


def e5_query(question:str) -> str:
    if not question.strip():raise ValueError('empty question')
    return 'query: '+question.strip()


def token_len(model, text: str) -> int:
    """반드시 실제 encoder에 넣을 전체 문자열과 같은 모델 tokenizer를 사용합니다."""
    return len(model.tokenizer(text,add_special_tokens=True,truncation=False)['input_ids'])
