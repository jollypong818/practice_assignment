"""실습 02 Basic · TXT parsing의 기본."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from coursekit.io import DATA, save_json, show_success


def decode_text(raw:bytes)->str:
    """errors='ignore'를 쓰면 누락을 탐지하기 어렵습니다."""
    # BEGIN D24-02-B01
    # 개념·실무 해설: Parsing은 Byte를 해석하여 텍스트뿐 아니라 제목·문단·페이지·표의 관계를 얻는 작업입니다. UTF-8 디코딩과 PDF Parser는 별도 구현입니다.
    # 해설 D24-02-B01 : 원문 바이트를 UTF-8로 디코딩해 str을 반환합니다. 잘못된 입력은 무시하지 않습니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    return raw.decode('utf-8-sig')
    # END D24-02-B01


def make_unit(doc_id:str,source_version:str,text:str)->dict:
    """TXT에는 페이지 번호가 없으므로 None. 가짜 page 1을 만들지 않습니다."""
    # BEGIN D24-02-B02
    # 개념·실무 해설: ParsedUnit에는 raw_text만이 아니라 원문 문서 ID·source_version·unit_id·Locator가 함께 있어야 문제의 위치를 다시 찾을 수 있습니다.
    # 해설 D24-02-B02 : 추출된 문자열을 doc_id·버전·unit_id·source_locator와 함께 한 건의 ParsedUnit으로 묶습니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    return {'doc_id':doc_id,'source_version':source_version,
            'unit_id':'text-1','source_locator':'assignment.txt',
            'page_number':None,'raw_text':text}
    # END D24-02-B02


def main():
    raw=(DATA/'raw'/'assignment.txt').read_bytes()
    text=decode_text(raw)
    if not text.strip():raise ValueError('empty text')
    unit=make_unit('DOC-ASSIGN','v1',text)
    out=save_json(HERE,'parsed_unit.json',unit)
    show_success('02 Basic',out)

if __name__=='__main__':main()
