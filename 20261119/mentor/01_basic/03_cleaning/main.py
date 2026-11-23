"""실습 03 Basic · 일반 prose 전용 cleaning."""
from pathlib import Path
import re,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from coursekit.io import DATA, save_json, show_success


def unify_newlines(text:str)->str:
    # BEGIN D24-03-B01
    # 개념·실무 해설: CRLF와 CR을 LF로 통일하되, 줄바꿈이 나타낸 문단 경계는 그대로 남깁니다. NFC는 응용 단계에서 별도 정규화합니다.
    # 해설 D24-03-B01 : CRLF·CR 줄바꿈을 LF로 바꿉니다. 문단의 줄을 하나로 합치지 않습니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    return text.replace('\r\n','\n').replace('\r','\n')
    # END D24-03-B01


def reduce_horizontal_spaces(text:str)->str:
    """줄 단위 변환이므로 빈 줄이 사라지지 않습니다."""
    # BEGIN D24-03-B02
    # 개념·실무 해설: 일반 prose의 연속된 가로 공백만 축약하고 줄바꿈 경계는 유지합니다. 코드 들여쓰기와 표의 탭 구분에는 같은 규칙을 적용하지 않습니다.
    # 해설 D24-03-B02 : 연속된 공백·탭을 한 칸으로 줄이고 좌우 공백을 제거합니다. 빈 줄은 보존합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    return '\n'.join(re.sub(r'[ \t]+',' ',line).strip()
                     for line in text.split('\n')).strip()
    # END D24-03-B02


def main():
    text='출석   안내\r\n\r\n10분  초과는 결석.\r\n단,  사전 승인 시 예외.'
    cleaned=reduce_horizontal_spaces(unify_newlines(text))
    assert '10분 초과는 결석.' in cleaned
    assert '\n\n' in cleaned
    out=save_json(HERE,'cleaning.json',{'before':repr(text),'after':cleaned})
    show_success('03 Basic',out)

if __name__=='__main__':main()
