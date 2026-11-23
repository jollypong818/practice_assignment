"""실습 06 Intermediate · 버전 쌍과 분류 조건."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from coursekit.io import save_json,show_success


def require_metadata(row:dict)->None:
    # BEGIN D24-06-I01
    # 개념·실무 해설: Metadata는 본문이 아닌 관리 정보입니다. 문서 ID·원문 판·처리 판·위치를 함께 가져야 검색 결과의 근거를 설명할 수 있습니다.
    # 해설 D24-06-I01 : 필수 Metadata 필드의 존재와 비어 있지 않음을 검사합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    for key in ('doc_id','source_version','pipeline_version','source_locator','category','chunk_id'):
        if not isinstance(row.get(key),str) or not row[key].strip():
            raise ValueError(f'missing {key}')
    # END D24-06-I01


def validate_locator(row:dict)->None:
    # BEGIN D24-06-I02
    # 개념·실무 해설: 문자 Span과 PDF page_number는 서로 다른 위치 단위입니다. TXT/Markdown에 존재하지 않는 페이지 번호를 만들어 넣지 않습니다.
    # 해설 D24-06-I02 : 문자 범위와 PDF page_number 등 자료형·조건을 확인합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    require_metadata(row)
    a,b=row.get('char_start'),row.get('char_end')
    if type(a) is not int or type(b) is not int or not 0<=a<b:
        raise ValueError('invalid span')
    page=row.get('page_number')
    if page is not None and (type(page) is not int or page<1):
        raise ValueError('invalid page')
    # END D24-06-I02


def select_current(rows:list[dict],pointers:dict)->list[dict]:
    # BEGIN D24-06-I03
    # 개념·실무 해설: category는 검색 편의 필터이지 사용자 접근 권한이 아닙니다. 실제 허용 문서 ID는 서버 측 인증/정책 확인 결과를 사용해야 합니다.
    # 해설 D24-06-I03 : 현재 공개 중인 source_version·pipeline_version 쌍만 선택합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    chosen=[]
    for row in rows:
        match=pointers.get(row['doc_id'])
        if match==(row['source_version'],row['pipeline_version']):
            chosen.append(row)
    return chosen
    # END D24-06-I03


def filter_and_report(rows:list[dict],pointers:dict,category:str)->dict:
    # BEGIN D24-06-I04
    # 개념·실무 해설: 현재 공개 포인터는 (source_version,pipeline_version) 쌍입니다. 둘 중 하나만 검사하면 다른 정제·모델 계약의 청크가 섞입니다.
    # 해설 D24-06-I04 : category 필터 후 반환 건수와 제외 이유를 기록합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    valid=[];invalid=[]
    for row in rows:
        try:validate_locator(row)
        except ValueError as exc:invalid.append({'chunk_id':row.get('chunk_id'),'reason':str(exc)})
        else:valid.append(row)
    current=select_current(valid,pointers)
    selected=[r for r in current if r['category']==category]
    return {'total':len(rows),'selected':selected,'invalid':invalid,
            'excluded_other_version':len(valid)-len(current),
            'excluded_other_category':len(current)-len(selected)}
    # END D24-06-I04


def main():
    base={'doc_id':'DOC-ATTEND','source_locator':'attendance.md#sec-1','category':'학사',
          'pipeline_version':'ingest-e5-v1','char_start':0,'char_end':20,'page_number':None}
    items=[{**base,'chunk_id':'C1','source_version':'v1'},
           {**base,'chunk_id':'C2','source_version':'v2'},
           {**base,'chunk_id':'C3','source_version':'v2','category':'시설'}]
    report=filter_and_report(items,{'DOC-ATTEND':('v2','ingest-e5-v1')},'학사')
    out=save_json(HERE,'metadata_filter.json',report)
    show_success('06 Intermediate',out)
