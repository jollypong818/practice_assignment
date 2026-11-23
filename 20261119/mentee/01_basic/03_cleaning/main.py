"""실습 03 Basic · 일반 prose 전용 cleaning."""
from pathlib import Path
import re,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from coursekit.io import DATA, save_json, show_success


def unify_newlines(text:str)->str:
    # BEGIN D24-03-B01
    # TODO D24-03-B01 : CRLF·CR 줄바꿈을 LF로 바꿉니다. 문단의 줄을 하나로 합치지 않습니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-03-B01 TODO 미완성")
    # CRLF와 CR을 차례로 LF로 바꾸도록 any 두 곳을 채우세요.
    return text.replace(any,'\n').replace(any,'\n')
    # END D24-03-B01
def reduce_horizontal_spaces(text:str)->str:
    """줄 단위 변환이므로 빈 줄이 사라지지 않습니다."""
    # BEGIN D24-03-B02
    # TODO D24-03-B02 : 연속된 공백·탭을 한 칸으로 줄이고 좌우 공백을 제거합니다. 빈 줄은 보존합니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-03-B02 TODO 미완성")
    # 줄 단위로 처리할 목록을 any 대신 작성하세요. 빈 줄은 보존해야 합니다.
    return '\n'.join(re.sub(r'[ \t]+',' ',line).strip()
                     for line in any).strip()
    # END D24-03-B02
def main():
    text='출석   안내\r\n\r\n10분  초과는 결석.\r\n단,  사전 승인 시 예외.'
    cleaned=reduce_horizontal_spaces(unify_newlines(text))
    assert '10분 초과는 결석.' in cleaned
    assert '\n\n' in cleaned
    out=save_json(HERE,'cleaning.json',{'before':repr(text),'after':cleaned})
    show_success('03 Basic',out)

if __name__=='__main__':main()
