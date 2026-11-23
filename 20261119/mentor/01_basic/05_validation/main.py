"""실습 05 Basic · 유효한 위치인지 먼저 판단."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from coursekit.io import save_json, show_success


def check_bounds(chunk:dict,text:str)->None:
    # BEGIN D24-05-B01
    # 개념·실무 해설: Schema 검증은 필수 필드, 올바른 타입, 양의 위치 등을 확인하는 최소 Gate입니다. 누락을 정상 데이터로 바꾸지 않습니다.
    # 해설 D24-05-B01 : 범위 0 <= start < end <= len(clean_text)를 검사합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    a,b=chunk['char_start'],chunk['char_end']
    if type(a) is not int or type(b) is not int or not 0<=a<b<=len(text):
        raise ValueError('invalid span')
    # END D24-05-B01


def check_content(chunk:dict,text:str)->None:
    # BEGIN D24-05-B02
    # 개념·실무 해설: clean_text[start:end]와 저장된 Chunk 본문이 완전히 일치하는지 확인해야 Citation이 다시 원문 구간을 가리킬 수 있습니다.
    # 해설 D24-05-B02 : chunk.text와 clean_text[start:end]가 같고 공백만 있는 청크가 아닌지 검사합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    check_bounds(chunk,text)
    if chunk['text']!=text[chunk['char_start']:chunk['char_end']]:
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
