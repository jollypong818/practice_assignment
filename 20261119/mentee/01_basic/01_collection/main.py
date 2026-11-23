"""실습 01 Basic · Python 파일 하나로 원문을 수집합니다."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from coursekit.io import DATA, save_json, show_success
from coursekit.documents import sha_bytes


def read_raw(path:Path)->bytes:
    """입력: Path / 출력: bytes. 원본 파일은 수정하지 않습니다."""
    # BEGIN D24-01-B01
    # TODO D24-01-B01 : 입력 경로의 파일을 bytes로 읽어 반환합니다. 없는 파일은 명확히 실패해야 합니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-01-B01 TODO 미완성")
    return path.read_bytes()
    # END D24-01-B01
def build_record(doc_id:str,path:Path,raw:bytes)->dict:
    """파일명은 식별자가 아닙니다. 문서 ID와 원본 바이트 해시를 별도로 보관합니다."""
    # BEGIN D24-01-B02
    # TODO D24-01-B02 : 문서 ID·원문 파일명·바이트 수·SHA-256을 한 딕셔너리에 묶습니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-01-B02 TODO 미완성")
    # any는 수강생이 알맞은 변수·표현식으로 교체할 자리 표시자입니다.
    return {'doc_id':any,'filename':any,'size_bytes':len(any),
                'raw_sha256':sha_bytes(any)}
    # END D24-01-B02
def main():
    path=DATA/'raw'/'assignment.txt'
    raw=read_raw(path)
    record=build_record('DOC-ASSIGN',path,raw)
    assert record['size_bytes']==len(raw)
    out=save_json(HERE,'collection.json',record)
    show_success('01 Basic',out)

if __name__=='__main__':main()
