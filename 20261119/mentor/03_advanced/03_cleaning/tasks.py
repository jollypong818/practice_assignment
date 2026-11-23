"""실습 03 Advanced · 구조별 정제 정책과 실패 회귀."""
from pathlib import Path
import hashlib,re,sys,unicodedata
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from coursekit.io import save_json,show_success
from coursekit.processing import clean_prose
from coursekit.documents import by_doc,parse_one


def choose_policy(block_type:str)->str:
    # BEGIN D24-03-A01
    # 개념·실무 해설: NFC는 Unicode 정준 정규화이며, NFKC는 ① 등의 호환 문자까지 바꿀 수 있습니다. 손실 범위가 더 큰 NFKC를 무조건 적용하지 않습니다.
    # 해설 D24-03-A01 : 본문 유형 prose/code/table을 구분해 정제 정책을 선택합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    if block_type not in ('prose','code','table'):raise ValueError('unknown block')
    return 'nfc_prose' if block_type=='prose' else 'preserve_structure'
    # END D24-03-A01


def clean_block(text:str,block_type:str)->str:
    # BEGIN D24-03-A02
    # 개념·실무 해설: 일반 prose의 연속된 가로 공백만 축약하고 줄바꿈 경계는 유지합니다. 코드 들여쓰기와 표의 탭 구분에는 같은 규칙을 적용하지 않습니다.
    # 해설 D24-03-A02 : 일반 본문에만 NFC·LF·가로 공백 축약을 수행하고 코드·표 구조를 보존합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    policy=choose_policy(block_type)
    if policy=='nfc_prose':return clean_prose(text)
    # 정렬된 표·Python 들여쓰기를 공백으로 뭉개지 않습니다.
    return text.replace('\r\n','\n').replace('\r','\n')
    # END D24-03-A02


def check_critical(source:str,cleaned:str,required:list[str])->dict:
    # BEGIN D24-03-A03
    # 개념·실무 해설: 정제 중 부정어, 숫자, 단위, 조건, 예외가 사라지면 업무 규정이 뒤집힐 수 있습니다. 핵심 문자열은 원문에서 추출해 비교합니다.
    # 해설 D24-03-A03 : 숫자·조건·부정 표현의 삭제를 발견해 실패로 표시합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    missing=[p for p in required if p in source and p not in cleaned]
    return {'passed':not missing,'lost_phrases':missing}
    # END D24-03-A03


def check_idempotent(cleaned:str,block_type:str)->bool:
    # BEGIN D24-03-A04
    # 개념·실무 해설: 동일 입력을 다시 정제했을 때 결과가 같아야 합니다. 멱등성은 일관성 검사일 뿐 의미 보존의 충분조건이 아닙니다.
    # 해설 D24-03-A04 : 같은 Cleaner를 반복 적용했을 때 결과가 동일한지 검사합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    return clean_block(cleaned,block_type)==cleaned
    # END D24-03-A04


def clean_fingerprint(text:str)->str:
    # BEGIN D24-03-A05
    # 개념·실무 해설: clean_hash는 정제한 문자열을 UTF-8로 인코딩한 뒤 계산합니다. raw_sha256은 정제 전 원본 바이트의 해시이므로 둘을 혼동하지 않습니다.
    # 해설 D24-03-A05 : 원본 bytes 해시와 별도로 clean_text UTF-8 해시를 기록합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    return hashlib.sha256(text.encode('utf-8')).hexdigest()
    # END D24-03-A05


def audit_unit(doc_id:str,unit:dict,source_version:str)->dict:
    # BEGIN D24-03-A06
    # 개념·실무 해설: Cleaner 버전·문서 ID·unit ID·정제 전후 차이를 함께 남겨야 검색 결과 문제를 앞단 Cleaning 단계까지 추적할 수 있습니다.
    # 해설 D24-03-A06 : 문서 ID·단위 ID·버전·정제 규칙과 실패 이유를 감사 보고서로 남깁니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    raw=unit['raw_text'];clean=clean_block(raw,'prose')
    check=check_critical(raw,clean,['10분','결석','사전 승인'])
    if not check['passed']:raise ValueError('critical text removed')
    return {'doc_id':doc_id,'source_version':source_version,'unit_id':unit['unit_id'],
            'cleaner_version':'nfc-prose-v1','clean_text':clean,
            'clean_hash':clean_fingerprint(clean),'meaning_check':check,
            'idempotent':check_idempotent(clean,'prose')}
    # END D24-03-A06


def main():
    doc=by_doc('DOC-ATTEND');result=parse_one(doc)
    units=[audit_unit(doc['doc_id'],u,doc['source_version']) for u in result['units']]
    corrupt='10분 초과는 결석.'.replace('10분','')
    bad=check_critical('10분 초과는 결석.',corrupt,['10분'])
    if bad['passed']:raise AssertionError('must detect lost number')
    out=save_json(HERE,'cleaning_audit.json',{'units':units,'bad_rule':bad})
    show_success('03 Advanced',out)
