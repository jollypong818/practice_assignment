"""실습 04 Advanced · 구조 우선, 긴 부분 재분할; --live-e5는 모델 길이 측정."""
from pathlib import Path
import hashlib,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from coursekit.io import save_json,show_success
from coursekit.documents import by_doc,parse_one
from coursekit.processing import clean_prose,char_windows,build_chunk,token_len


def paragraph_spans(text:str)->list[dict]:
    # BEGIN D24-04-A01
    # TODO D24-04-A01 : 문단 경계 후보를 찾아 원문 구간을 정확히 추출합니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-04-A01 TODO 미완성")
    # END D24-04-A01
def split_long(text:str,spans:list[dict],size=90,overlap=15)->list[dict]:
    # BEGIN D24-04-A02
    # TODO D24-04-A02 : 긴 문단만 문자 창으로 재분할하며 짧은 문단은 그대로 유지합니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-04-A02 TODO 미완성")
    # END D24-04-A02
def make_records(doc:dict,unit:dict,clean:str,spans:list[dict])->list[dict]:
    # BEGIN D24-04-A03
    # TODO D24-04-A03 : 각 Span을 doc_id·unit_id·source_locator에 연결해 Chunk를 만듭니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-04-A03 TODO 미완성")
    # END D24-04-A03
def embedding_input(chunk:dict,include_title:bool)->str:
    # BEGIN D24-04-A04
    # TODO D24-04-A04 : 본문과 선택적 제목을 합쳐 `passage: ` 입력을 만들고 Offset과 분리합니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-04-A04 TODO 미완성")
    # END D24-04-A04
def check_model_lengths(chunks:list[dict],model=None)->dict:
    # BEGIN D24-04-A05
    # TODO D24-04-A05 : 모델이 제공되면 Tokenizer로 길이를 측정하고 초과 결과를 격리합니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-04-A05 TODO 미완성")
    # END D24-04-A05
def check_repeat(doc:dict,unit:dict)->dict:
    # BEGIN D24-04-A06
    # TODO D24-04-A06 : 동일 원문·설정의 재실행에서 Chunk ID·본문·문자 범위가 동일한지 검사합니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-04-A06 TODO 미완성")
    # END D24-04-A06
def main():
    doc=by_doc('DOC-ATTEND');unit=parse_one(doc)['units'][0]
    result=check_repeat(doc,unit)
    model=None
    if '--live-e5' in sys.argv:
        from coursekit.live import load_encoder
        model=load_encoder()
    result['token_check']=check_model_lengths(result['chunks'],model)
    result['embedding_input_contract']='passage: [optional title] + body'
    out=save_json(HERE,'structure_chunks.json',result)
    show_success('04 Advanced',out)
