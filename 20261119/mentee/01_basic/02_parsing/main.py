"""실습 02 Basic · TXT parsing의 기본."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from coursekit.io import DATA, save_json, show_success


def decode_text(raw:bytes)->str:
    """errors='ignore'를 쓰면 누락을 탐지하기 어렵습니다."""
    # BEGIN D24-02-B01
    # TODO D24-02-B01 : 원문 바이트를 UTF-8로 디코딩해 str을 반환합니다. 잘못된 입력은 무시하지 않습니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-02-B01 TODO 미완성")
    # any를 UTF-8 디코딩에 사용할 Encoding 이름으로 교체하세요.
    return raw.decode(any)
    # END D24-02-B01
def make_unit(doc_id:str,source_version:str,text:str)->dict:
    """TXT에는 페이지 번호가 없으므로 None. 가짜 page 1을 만들지 않습니다."""
    # BEGIN D24-02-B02
    # TODO D24-02-B02 : 추출된 문자열을 doc_id·버전·unit_id·source_locator와 함께 한 건의 ParsedUnit으로 묶습니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-02-B02 TODO 미완성")
    # any는 수강생이 직접 채울 자리 표시자입니다.
    return {'doc_id':any,'source_version':any,
            'unit_id':'text-1','source_locator':'assignment.txt',
            'page_number':None,'raw_text':any}
    # END D24-02-B02
def main():
    raw=(DATA/'raw'/'assignment.txt').read_bytes()
    text=decode_text(raw)
    if not text.strip():raise ValueError('empty text')
    unit=make_unit('DOC-ASSIGN','v1',text)
    out=save_json(HERE,'parsed_unit.json',unit)
    show_success('02 Basic',out)

if __name__=='__main__':main()
