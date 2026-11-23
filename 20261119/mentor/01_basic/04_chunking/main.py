"""실습 04 Basic · 종료 조건이 중요한 문자 창."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from coursekit.io import DATA, save_json, show_success


def check_params(size:int,overlap:int)->None:
    # BEGIN D24-04-B01
    # 개념·실무 해설: 0 이상인 Overlap이 Chunk Size보다 작아야 다음 시작 위치가 앞으로 진행합니다. bool은 int의 하위 타입이라 type()으로 따로 거부합니다.
    # 해설 D24-04-B01 : size와 overlap을 정수로 검사하고 0 <= overlap < size를 보장합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    if type(size) is not int or type(overlap) is not int or not 0<=overlap<size:
        raise ValueError('invalid chunk size or overlap')
    # END D24-04-B01


def make_windows(text:str,size:int,overlap:int)->list[dict]:
    """본문 끝에서 반복문을 종료하지 않으면 겹친 꼬리 청크가 생깁니다."""
    # BEGIN D24-04-B02
    # 개념·실무 해설: Chunk Size·Overlap은 0≤overlap<size를 만족해야 합니다. 창이 끝에 닿은 순간 종료해야 중복 꼬리 Chunk가 생기지 않습니다.
    # 해설 D24-04-B02 : start·end·text가 있는 Chunk 목록을 만들고 본문 끝에 닿으면 종료합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    check_params(size,overlap)
    spans=[];start=0
    while start<len(text):
        end=min(start+size,len(text))
        spans.append({'char_start':start,'char_end':end,'text':text[start:end]})
        if end==len(text):break
        start=end-overlap
    return spans
    # END D24-04-B02


def main():
    text='가'*71
    chunks=make_windows(text,size=40,overlap=10)
    assert [(c['char_start'],c['char_end']) for c in chunks]==[(0,40),(30,70),(60,71)]
    out=save_json(HERE,'chunks.json',{'source':'71-character teaching fixture','chunks':chunks})
    show_success('04 Basic',out)

if __name__=='__main__':main()
