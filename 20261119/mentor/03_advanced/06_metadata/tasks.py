"""실습 06 Advanced · 공개 범위와 정수형 Citation Contract."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from coursekit.io import save_json,show_success
from coursekit.processing import stable_chunk_id


def check_meta(row:dict)->None:
    # BEGIN D24-06-A01
    # 개념·실무 해설: Metadata는 본문이 아닌 관리 정보입니다. 문서 ID·원문 판·처리 판·위치를 함께 가져야 검색 결과의 근거를 설명할 수 있습니다.
    # 해설 D24-06-A01 : doc_id·version·category·Span·locator와 page_number 자료형을 검증합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    for name in ('doc_id','source_version','pipeline_version','unit_id','source_locator','category','chunk_id'):
        if not isinstance(row.get(name),str) or not row[name].strip():
            raise ValueError('missing '+name)
    a,b=row.get('char_start'),row.get('char_end')
    if type(a) is not int or type(b) is not int or not 0<=a<b:raise ValueError('bad span')
    page=row.get('page_number')
    if page is not None and (type(page) is not int or page<1):raise ValueError('bad page')
    # END D24-06-A01


def stable_id(row:dict)->str:
    # BEGIN D24-06-A02
    # 개념·실무 해설: 문자 Span과 PDF page_number는 서로 다른 위치 단위입니다. TXT/Markdown에 존재하지 않는 페이지 번호를 만들어 넣지 않습니다.
    # 해설 D24-06-A02 : doc_id·원문 판·처리 판·unit_id·Span으로 안정적인 chunk_id를 만듭니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    return stable_chunk_id(row,row['unit_id'],row['pipeline_version'],row['char_start'],row['char_end'])
    # END D24-06-A02


def restrict_allowed(rows:list[dict],allowed_doc_ids:set[str])->list[dict]:
    # BEGIN D24-06-A03
    # 개념·실무 해설: category는 검색 편의 필터이지 사용자 접근 권한이 아닙니다. 실제 허용 문서 ID는 서버 측 인증/정책 확인 결과를 사용해야 합니다.
    # 해설 D24-06-A03 : 서버가 확인한 allowed_doc_ids 목록으로만 후보를 제한합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    if not isinstance(allowed_doc_ids,set):raise ValueError('server-verified set required')
    return [r for r in rows if r.get('doc_id') in allowed_doc_ids]
    # END D24-06-A03


def select_published(rows:list[dict],pointers:dict,category:str)->list[dict]:
    # BEGIN D24-06-A04
    # 개념·실무 해설: 현재 공개 포인터는 (source_version,pipeline_version) 쌍입니다. 둘 중 하나만 검사하면 다른 정제·모델 계약의 청크가 섞입니다.
    # 해설 D24-06-A04 : 문서별 current source_version·pipeline_version 쌍과 category가 맞는 후보를 선택합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    return [r for r in rows if r['category']==category and
            pointers.get(r['doc_id'])==(r['source_version'],r['pipeline_version'])]
    # END D24-06-A04


def citation_map(rows:list[dict])->dict:
    # BEGIN D24-06-A05
    # 개념·실무 해설: 기존 KnowledgeAnswer.source_ids는 list[int]입니다. Chunk ID는 text이므로 DB에서 얻은 양의 정수 citation_id를 명시적으로 매핑합니다.
    # 해설 D24-06-A05 : 양의 정수 citation_id와 문자열 chunk_id 사이의 중복 없는 매핑을 만듭니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    ids=[r['citation_id'] for r in rows]
    if any(type(n) is not int or n<=0 for n in ids) or len(ids)!=len(set(ids)):
        raise ValueError('invalid citation_id')
    chunks=[r['chunk_id'] for r in rows]
    if len(chunks)!=len(set(chunks)):raise ValueError('duplicate chunk_id')
    return {r['citation_id']:{'chunk_id':r['chunk_id'],
           'source_locator':r['source_locator'],'doc_id':r['doc_id']} for r in rows}
    # END D24-06-A05


def audit(rows:list[dict],pointers:dict,allowed:set[str],category:str)->dict:
    # BEGIN D24-06-A06
    # 개념·실무 해설: 문서 권한·공개 버전·필터·오류 여부를 순서대로 검사한 후 대상과 제외 사유를 분리해 보고합니다.
    # 해설 D24-06-A06 : 정상·차단·미공개·Metadata 오류 상태를 구분해 감사 결과를 출력합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    good=[];invalid=[]
    for r in rows:
        try:check_meta(r)
        except ValueError as exc:invalid.append({'chunk_id':r.get('chunk_id'),'reason':str(exc)})
        else:
            if stable_id(r)!=r['chunk_id']:invalid.append({'chunk_id':r['chunk_id'],'reason':'unstable_identity'})
            else:good.append(r)
    accessible=restrict_allowed(good,allowed)
    selected=select_published(accessible,pointers,category)
    return {'citations':citation_map(selected),'invalid':invalid,
            'excluded_permission':len(good)-len(accessible),
            'excluded_version_or_category':len(accessible)-len(selected)}
    # END D24-06-A06


def main():
    def make(docid,ver,category,citation):
        r={'doc_id':docid,'source_version':ver,'pipeline_version':'ingest-e5-v1',
           'unit_id':'sec-1','source_locator':f'{docid}.md#sec-1',
           'category':category,'char_start':0,'char_end':12,'page_number':None,
           'citation_id':citation}
        return {**r,'chunk_id':stable_id(r)}
    items=[make('DOC-ATTEND','v1','학사',201),make('DOC-ATTEND','v2','학사',202),
           make('DOC-FACILITY','v1','시설',203)]
    report=audit(items,{'DOC-ATTEND':('v2','ingest-e5-v1')},
                 {'DOC-ATTEND'},'학사')
    out=save_json(HERE,'metadata_audit.json',report)
    show_success('06 Advanced',out)
