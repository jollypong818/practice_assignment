"""실습 02 Intermediate · format dispatch와 공통 ParsedUnit."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from coursekit.io import DATA,load_json,save_json,show_success
from coursekit.documents import parse_one,raw_path


def kind_of(doc:dict)->str:
    # BEGIN D24-02-I01
    # TODO D24-02-I01 : 파일 확장자로 파서 경로를 결정합니다. 미지원 확장자를 정상 취급하지 않습니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-02-I01 TODO 미완성")
    # END D24-02-I01
def parse_txt(doc:dict)->dict:
    # BEGIN D24-02-I02
    # TODO D24-02-I02 : TXT를 UTF-8로 읽고 오류와 빈 결과를 구분합니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-02-I02 TODO 미완성")
    # END D24-02-I02
def parse_markup(doc:dict)->dict:
    # BEGIN D24-02-I03
    # TODO D24-02-I03 : Markdown·HTML에서 제목·본문·표의 구조를 가진 ParsedUnit을 추출합니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-02-I03 TODO 미완성")
    # END D24-02-I03
def parse_dispatch(doc:dict)->dict:
    # BEGIN D24-02-I04
    # TODO D24-02-I04 : PDF는 페이지별 위치를 기록하고 이미지 PDF는 별도 needs_ocr로 분류합니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-02-I04 TODO 미완성")
    # END D24-02-I04
def main():
    rows=load_json(DATA/'manifest.json')
    results=[parse_dispatch(r) for r in rows]
    out=save_json(HERE,'parsing_report.json',{'items':results,
             'status_counts':{s:sum(r['status']==s for r in results)
                for s in sorted({r['status'] for r in results})}})
    show_success('02 Intermediate',out)
