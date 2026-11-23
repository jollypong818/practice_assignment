"""실습 02 Advanced · PDF/Text/HTML parsing QA."""
from pathlib import Path
import json,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from coursekit.io import DATA,load_json,save_json,show_success
from coursekit.documents import parse_one


def dispatch(row:dict)->dict:
    # BEGIN D24-02-A01
    # 개념·실무 해설: Parsing은 Byte를 해석하여 텍스트뿐 아니라 제목·문단·페이지·표의 관계를 얻는 작업입니다. UTF-8 디코딩과 PDF Parser는 별도 구현입니다.
    # 해설 D24-02-A01 : 문서 ID별 형식을 검사하고 TXT/Markdown/HTML/PDF/Unsupported 경로를 선택합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    suffix=Path(row['file']).suffix.lower()
    if suffix not in {'.txt','.md','.html','.pdf'}:
        return {'doc':{'doc_id':row['doc_id']},'status':'unsupported','units':[],
                'reason':'unknown_extension'}
    return parse_one(row)
    # END D24-02-A01


def check_pdf(doc:dict,result:dict)->None:
    # BEGIN D24-02-A02
    # 개념·실무 해설: ParsedUnit에는 raw_text만이 아니라 원문 문서 ID·source_version·unit_id·Locator가 함께 있어야 문제의 위치를 다시 찾을 수 있습니다.
    # 해설 D24-02-A02 : PDF의 페이지 번호와 source_locator를 검증하고 원문 텍스트를 유지합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    if not doc['file'].endswith('.pdf'):return
    for page_i,unit in enumerate(result['units'],1):
        if unit['page_number']!=page_i or unit['unit_id']!=f'page-{page_i}':
            raise ValueError('page numbering mismatch')
        if not unit['source_locator'].endswith(f'#page={page_i}'):
            raise ValueError('bad page locator')
    # END D24-02-A02


def check_html(doc:dict,result:dict)->None:
    # BEGIN D24-02-A03
    # 개념·실무 해설: HTML의 nav·script는 본문이 아닙니다. 표는 시설 이름과 안내 값의 열·행 관계가 유지되는지 확인합니다.
    # 해설 D24-02-A03 : HTML에서 nav·script가 본문에 섞이지 않고 표의 헤더·값 관계가 남았는지 검사합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    if not doc['file'].endswith('.html') or result['status']!='parsed':return
    joined='\n'.join(u['raw_text'] for u in result['units'])
    if 'login' in joined.lower() or 'console.log' in joined:
        raise ValueError('navigation/script entered body')
    for required in ('시설: 실습실','안내: 담당자 안내에 따라 운영'):
        if required not in joined:raise ValueError('table columns lost: '+required)
    # END D24-02-A03


def empty_policy(doc:dict,result:dict)->str:
    # BEGIN D24-02-A04
    # 개념·실무 해설: pypdf의 extract_text()는 이미지 OCR이 아닙니다. `scan.pdf`는 자료 제작 시 이미지 전용임을 알고 분리한 샘플이며 다른 빈 PDF는 원문 확인이 필요합니다.
    # 해설 D24-02-A04 : 본문이 없는 페이지를 무조건 OCR 성공으로 처리하지 않고 상태를 분류합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    if result['status']=='needs_ocr':return 'needs_ocr'
    if result['status']=='empty_text_review':return 'needs_original_review'
    if result['status']=='parse_error':return 'parse_error'
    if result['status']=='unsupported':return 'unsupported'
    if result['status']=='parsed' and result['units']:return 'parsed'
    return 'quarantine'
    # END D24-02-A04


def inspect_one(doc:dict)->dict:
    # BEGIN D24-02-A05
    # 개념·실무 해설: 빈 추출·지원 밖 확장자·파일 손상은 오류 원인이 다릅니다. 모두 빈 문자열로 치환하면 오류를 추적하지 못합니다.
    # 해설 D24-02-A05 : 파일별 실패·격리·성공 상태를 가진 Result를 작성합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    result=dispatch(doc)
    check_pdf(doc,result);check_html(doc,result)
    status=empty_policy(doc,result)
    return {'doc_id':doc['doc_id'],'status':status,
            'unit_count':len(result['units']),
            'source_locators':[u['source_locator'] for u in result['units']],
            'reason':result.get('reason')}
    # END D24-02-A05


def run_audit(rows:list[dict])->dict:
    # BEGIN D24-02-A06
    # 개념·실무 해설: 같은 원문과 Parser 설정에서 동일한 ParsedUnit·위치가 나오는지 회귀 검사합니다. 결과가 출력됐어도 원문 의미 보존은 별도 검증입니다.
    # 해설 D24-02-A06 : 원문 목록 건수와 처리 결과가 일치하며 동일 입력 재실행의 결과도 같은지 확인합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    items=[inspect_one(doc) for doc in rows]
    if len(items)!=len(rows):raise ValueError('unprocessed input')
    repeat=[inspect_one(doc) for doc in rows]
    if items!=repeat:raise ValueError('non deterministic parsing')
    counts={s:sum(r['status']==s for r in items) for s in sorted({r['status'] for r in items})}
    return {'total':len(items),'status_counts':counts,'items':items,'repeat_equal':True}
    # END D24-02-A06


def main():
    report=run_audit(load_json(DATA/'manifest.json'))
    out=save_json(HERE,'parsing_audit.json',report)
    show_success('02 Advanced',out)
