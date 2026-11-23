"""실습 06 Advanced · 공개 범위와 정수형 Citation Contract."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from coursekit.io import save_json,show_success
from coursekit.processing import stable_chunk_id


def check_meta(row:dict)->None:
    # BEGIN D24-06-A01
    # TODO D24-06-A01 : doc_id·version·category·Span·locator와 page_number 자료형을 검증합니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-06-A01 TODO 미완성")
    # END D24-06-A01
def stable_id(row:dict)->str:
    # BEGIN D24-06-A02
    # TODO D24-06-A02 : doc_id·원문 판·처리 판·unit_id·Span으로 안정적인 chunk_id를 만듭니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-06-A02 TODO 미완성")
    # END D24-06-A02
def restrict_allowed(rows:list[dict],allowed_doc_ids:set[str])->list[dict]:
    # BEGIN D24-06-A03
    # TODO D24-06-A03 : 서버가 확인한 allowed_doc_ids 목록으로만 후보를 제한합니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-06-A03 TODO 미완성")
    # END D24-06-A03
def select_published(rows:list[dict],pointers:dict,category:str)->list[dict]:
    # BEGIN D24-06-A04
    # TODO D24-06-A04 : 문서별 current source_version·pipeline_version 쌍과 category가 맞는 후보를 선택합니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-06-A04 TODO 미완성")
    # END D24-06-A04
def citation_map(rows:list[dict])->dict:
    # BEGIN D24-06-A05
    # TODO D24-06-A05 : 양의 정수 citation_id와 문자열 chunk_id 사이의 중복 없는 매핑을 만듭니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-06-A05 TODO 미완성")
    # END D24-06-A05
def audit(rows:list[dict],pointers:dict,allowed:set[str],category:str)->dict:
    # BEGIN D24-06-A06
    # TODO D24-06-A06 : 정상·차단·미공개·Metadata 오류 상태를 구분해 감사 결과를 출력합니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-06-A06 TODO 미완성")
    # END D24-06-A06
def main():
    def make(docid,ver,category,citation):
        r={'doc_id':docid,'source_version':ver,'pipeline_version':'ingest-e5-v1',
           'unit_id':'sec-1','source_locator':f'{docid}.md#sec-1',
           'category':category,'char_start':0,'char_end':12,'page_number':None,
           'citation_id':citation}
        return {**r,'chunk_id':stable_id(r)}
    items=[make('DOC-ATTEND','v1','학사',201),make('DOC-ATTEND','v2','학사',202),
           make('DOC-FACILITY','v1','시설',203)]
    report=audit(items,{'DOC-ATTEND':('v2','ingest-e5-v1')},
                 {'DOC-ATTEND'},'학사')
    out=save_json(HERE,'metadata_audit.json',report)
    show_success('06 Advanced',out)
