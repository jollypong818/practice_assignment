"""실습 02 Intermediate · format dispatch와 공통 ParsedUnit."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from coursekit.io import DATA,load_json,save_json,show_success
from coursekit.documents import parse_one,raw_path


def kind_of(doc:dict)->str:
    # BEGIN D24-02-I01
    # 개념·실무 해설: Parsing은 Byte를 해석하여 텍스트뿐 아니라 제목·문단·페이지·표의 관계를 얻는 작업입니다. UTF-8 디코딩과 PDF Parser는 별도 구현입니다.
    # 해설 D24-02-I01 : 파일 확장자로 파서 경로를 결정합니다. 미지원 확장자를 정상 취급하지 않습니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    suffix=Path(doc['file']).suffix.lower()
    return {'.txt':'txt','.md':'markdown','.html':'html','.pdf':'pdf'}.get(suffix,'unsupported')
    # END D24-02-I01


def parse_txt(doc:dict)->dict:
    # BEGIN D24-02-I02
    # 개념·실무 해설: ParsedUnit에는 raw_text만이 아니라 원문 문서 ID·source_version·unit_id·Locator가 함께 있어야 문제의 위치를 다시 찾을 수 있습니다.
    # 해설 D24-02-I02 : TXT를 UTF-8로 읽고 오류와 빈 결과를 구분합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    if kind_of(doc)!='txt':raise ValueError('wrong parser')
    return parse_one(doc)
    # END D24-02-I02


def parse_markup(doc:dict)->dict:
    # BEGIN D24-02-I03
    # 개념·실무 해설: HTML의 nav·script는 본문이 아닙니다. 표는 시설 이름과 안내 값의 열·행 관계가 유지되는지 확인합니다.
    # 해설 D24-02-I03 : Markdown·HTML에서 제목·본문·표의 구조를 가진 ParsedUnit을 추출합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    if kind_of(doc) not in {'markdown','html'}:raise ValueError('wrong parser')
    return parse_one(doc)
    # END D24-02-I03


def parse_dispatch(doc:dict)->dict:
    # BEGIN D24-02-I04
    # 개념·실무 해설: pypdf의 extract_text()는 이미지 OCR이 아닙니다. `scan.pdf`는 자료 제작 시 이미지 전용임을 알고 분리한 샘플이며 다른 빈 PDF는 원문 확인이 필요합니다.
    # 해설 D24-02-I04 : PDF는 페이지별 위치를 기록하고 이미지 PDF는 별도 needs_ocr로 분류합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    kind=kind_of(doc)
    if kind=='txt':return parse_txt(doc)
    if kind in {'markdown','html'}:return parse_markup(doc)
    if kind=='pdf':return parse_one(doc)
    return {'doc':{'doc_id':doc['doc_id']},'status':'unsupported','units':[],
            'reason':'unsupported_extension'}
    # END D24-02-I04


def main():
    rows=load_json(DATA/'manifest.json')
    results=[parse_dispatch(r) for r in rows]
    out=save_json(HERE,'parsing_report.json',{'items':results,
             'status_counts':{s:sum(r['status']==s for r in results)
                for s in sorted({r['status'] for r in results})}})
    show_success('02 Intermediate',out)
