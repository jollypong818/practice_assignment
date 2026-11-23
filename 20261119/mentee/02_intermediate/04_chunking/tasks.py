"""실습 04 Intermediate · --live-e5 시 실제 토크나이저 사용."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from coursekit.io import save_json,show_success
from coursekit.documents import by_doc,parse_one
from coursekit.processing import clean_prose,char_windows,build_chunk,token_len


def split_one(doc:dict,unit:dict,size=70,overlap=10)->tuple[str,list[dict]]:
    # BEGIN D24-04-I01
    # TODO D24-04-I01 : 하나의 ParsedUnit을 clean_text에서 문자 창으로 분할합니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-04-I01 TODO 미완성")
    # END D24-04-I01
def attach_chunks(doc:dict,unit:dict,text:str,spans:list[dict])->list[dict]:
    # BEGIN D24-04-I02
    # TODO D24-04-I02 : 각 창에 doc_id·unit_id·버전·Locator와 passage: 접두어를 전달합니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-04-I02 TODO 미완성")
    # END D24-04-I02
def measure(chunks:list[dict],model=None)->list[dict]:
    # BEGIN D24-04-I03
    # TODO D24-04-I03 : SentenceTransformer 모델이 주어졌을 때 특수 토큰 포함 길이를 측정합니다. 모델이 없으면 not_run으로 기록합니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-04-I03 TODO 미완성")
    # END D24-04-I03
def enforce_limit(chunks:list[dict],model=None)->dict:
    # BEGIN D24-04-I04
    # TODO D24-04-I04 : 최대 입력 길이를 초과한 청크를 통과시키지 않고 개수와 ID를 기록합니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-04-I04 TODO 미완성")
    # END D24-04-I04
def main():
    model=None
    if '--live-e5' in sys.argv:
        from coursekit.live import load_encoder
        model=load_encoder()
    all_chunks=[]
    for doc_id in ('DOC-ATTEND','DOC-ASSIGN'):
        doc=by_doc(doc_id)
        for unit in parse_one(doc)['units']:
            text,spans=split_one(doc,unit)
            all_chunks.extend(attach_chunks(doc,unit,text,spans))
    measured=measure(all_chunks,model)
    report=enforce_limit(measured,model)
    out=save_json(HERE,'chunking_report.json',{'chunks':measured,'token_validation':report})
    show_success('04 Intermediate',out)
