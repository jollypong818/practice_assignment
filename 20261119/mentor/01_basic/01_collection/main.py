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
    # 개념·실무 해설: 원본 수집 시 경로가 존재하는지 확인하고 read_bytes()를 사용합니다. text decode는 다음 실습에서 수행하므로 이 단계에서 원문 바이트를 바꾸지 않습니다.
    # 해설 D24-01-B01 : 입력 경로의 파일을 bytes로 읽어 반환합니다. 없는 파일은 명확히 실패해야 합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    if not path.is_file():
        raise FileNotFoundError(path)
    return path.read_bytes()
    # END D24-01-B01


def build_record(doc_id:str,path:Path,raw:bytes)->dict:
    """파일명은 식별자가 아닙니다. 문서 ID와 원본 바이트 해시를 별도로 보관합니다."""
    # BEGIN D24-01-B02
    # 개념·실무 해설: len(raw)은 Byte 길이이며 len(text)와 같지 않습니다. SHA-256은 같은 바이트를 다시 확인하기 위한 식별 단서이지 문서의 내용이 진실임을 증명하지 않습니다.
    # 해설 D24-01-B02 : 문서 ID·원문 파일명·바이트 수·SHA-256을 한 딕셔너리에 묶습니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    return {'doc_id':doc_id,'filename':path.name,'size_bytes':len(raw),
            'raw_sha256':sha_bytes(raw)}
    # END D24-01-B02


def main():
    path=DATA/'raw'/'assignment.txt'
    raw=read_raw(path)
    record=build_record('DOC-ASSIGN',path,raw)
    assert record['size_bytes']==len(raw)
    out=save_json(HERE,'collection.json',record)
    show_success('01 Basic',out)

if __name__=='__main__':main()
