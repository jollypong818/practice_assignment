"""실습 04 Basic · 종료 조건이 중요한 문자 창."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from coursekit.io import DATA, save_json, show_success


def check_params(size:int,overlap:int)->None:
    # BEGIN D24-04-B01
    # TODO D24-04-B01 : size와 overlap을 정수로 검사하고 0 <= overlap < size를 보장합니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-04-B01 TODO 미완성")
    # Overlap의 최소 허용값을 any 대신 채우세요.
    if type(size) is not int or type(overlap) is not int or not (any<=overlap<size):
        raise ValueError('invalid chunk size or overlap')
    # END D24-04-B01
def make_windows(text:str,size:int,overlap:int)->list[dict]:
    """본문 끝에서 반복문을 종료하지 않으면 겹친 꼬리 청크가 생깁니다."""
    # BEGIN D24-04-B02
    # TODO D24-04-B02 : start·end·text가 있는 Chunk 목록을 만들고 본문 끝에 닿으면 종료합니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-04-B02 TODO 미완성")
    check_params(size,overlap)
    spans=[]
    start=0
    while start<len(text):
        end=min(start+size,len(text))
        # 두 any는 현재 Chunk가 원문에서 차지하는 시작·끝 위치입니다.
        spans.append({'char_start':start,'char_end':end,'text':text[any:any]})
        if end==len(text):
            break
        # 다음 시작점은 현재 끝점에서 Overlap만큼 되돌아간 위치입니다.
        start=any
    return spans
    # END D24-04-B02
def main():
    text='가'*71
    chunks=make_windows(text,size=40,overlap=10)
    assert [(c['char_start'],c['char_end']) for c in chunks]==[(0,40),(30,70),(60,71)]
    out=save_json(HERE,'chunks.json',{'source':'71-character teaching fixture','chunks':chunks})
    show_success('04 Basic',out)

if __name__=='__main__':main()
