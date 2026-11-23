"""실습 03 Intermediate · 정제 계약과 보고서."""
from pathlib import Path
import sys, re,unicodedata,hashlib
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from coursekit.io import DATA,save_json,show_success
from coursekit.documents import by_doc,parse_one


def apply_nfc(text:str)->str:
    # BEGIN D24-03-I01
    # 개념·실무 해설: NFC는 Unicode 정준 정규화이며, NFKC는 ① 등의 호환 문자까지 바꿀 수 있습니다. 손실 범위가 더 큰 NFKC를 무조건 적용하지 않습니다.
    # 해설 D24-03-I01 : 원문을 Unicode NFC로 정규화합니다. NFKC로 동그라미 번호를 무조건 지우지 않습니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    return unicodedata.normalize('NFC',text)
    # END D24-03-I01


def normalize_prose(text:str)->str:
    # BEGIN D24-03-I02
    # 개념·실무 해설: 일반 prose의 연속된 가로 공백만 축약하고 줄바꿈 경계는 유지합니다. 코드 들여쓰기와 표의 탭 구분에는 같은 규칙을 적용하지 않습니다.
    # 해설 D24-03-I02 : CRLF·CR·가로 공백만 정리하며 문단 경계를 보존합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    text=apply_nfc(text.replace('\r\n','\n').replace('\r','\n'))
    return '\n'.join(re.sub(r'[ \t]+',' ',line).strip() for line in text.split('\n')).strip()
    # END D24-03-I02


def check_phrases(text:str,phrases:list[str])->dict:
    # BEGIN D24-03-I03
    # 개념·실무 해설: 정제 중 부정어, 숫자, 단위, 조건, 예외가 사라지면 업무 규정이 뒤집힐 수 있습니다. 핵심 문자열은 원문에서 추출해 비교합니다.
    # 해설 D24-03-I03 : 핵심 구절 목록을 받아 부정어·숫자·예외의 존재 여부를 검사합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    return {'present':[p for p in phrases if p in text],
            'missing':[p for p in phrases if p not in text]}
    # END D24-03-I03


def make_audit(original:str,cleaned:str,phrases:list[str])->dict:
    # BEGIN D24-03-I04
    # 개념·실무 해설: 동일 입력을 다시 정제했을 때 결과가 같아야 합니다. 멱등성은 일관성 검사일 뿐 의미 보존의 충분조건이 아닙니다.
    # 해설 D24-03-I04 : 정제 규칙 버전·전후 길이·해시·검사 결과를 출력합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    return {'cleaner_version':'nfc-prose-v1','chars_before':len(original),
            'chars_after':len(cleaned),'clean_hash':hashlib.sha256(cleaned.encode('utf-8')).hexdigest(),
            'phrase_check':check_phrases(cleaned,phrases),
            'idempotent':normalize_prose(cleaned)==cleaned}
    # END D24-03-I04


def main():
    doc=by_doc('DOC-ATTEND');unit=parse_one(doc)['units'][0]
    original=unit['raw_text'];cleaned=normalize_prose(original)
    audit=make_audit(original,cleaned,['10분','결석','사전 승인'])
    out=save_json(HERE,'clean_report.json',{'doc_id':doc['doc_id'],
        'unit_id':unit['unit_id'],'clean_text':cleaned,'audit':audit})
    show_success('03 Intermediate',out)
