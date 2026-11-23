"""실습 05 Basic · 유효한 위치인지 먼저 판단."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from coursekit.io import save_json, show_success


def check_bounds(chunk:dict,text:str)->None:
    # BEGIN D24-05-B01
    # TODO D24-05-B01 : 범위 0 <= start < end <= len(clean_text)를 검사합니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-05-B01 TODO 미완성")
    # 아래 any 두 곳에 Chunk의 시작·끝 필드 이름을 넣으세요.
    start,end=chunk[any],chunk[any]
    if type(start) is not int or type(end) is not int or not (0<=start<end<=len(text)):
        raise ValueError('invalid span')
    # END D24-05-B01
def check_content(chunk:dict,text:str)->None:
    # BEGIN D24-05-B02
    # TODO D24-05-B02 : chunk.text와 clean_text[start:end]가 같고 공백만 있는 청크가 아닌지 검사합니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-05-B02 TODO 미완성")
    check_bounds(chunk,text)
    # 아래 any 두 곳에 검증된 문자 범위의 시작·끝 위치를 넣으세요.
    if chunk['text'] != text[any:any]:
        raise ValueError('span text mismatch')
    if not chunk['text'].strip():
        raise ValueError('empty content')
    # END D24-05-B02
def main():
    text='10분 초과 시 결석으로 기록합니다.'
    good={'char_start':0,'char_end':len(text),'text':text}
    bad={'char_start':0,'char_end':len(text),'text':'잘못된 내용'}
    check_content(good,text)
    try:check_content(bad,text)
    except ValueError:result='expected failure'
    else:raise AssertionError('a corrupted chunk must fail')
    out=save_json(HERE,'span_check.json',{'good':'pass','bad':result})
    show_success('05 Basic',out)

if __name__=='__main__':main()
