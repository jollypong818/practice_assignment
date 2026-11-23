"""실습 06 Intermediate · 버전 쌍과 분류 조건."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from coursekit.io import save_json,show_success


def require_metadata(row:dict)->None:
    # BEGIN D24-06-I01
    # TODO D24-06-I01 : 필수 Metadata 필드의 존재와 비어 있지 않음을 검사합니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-06-I01 TODO 미완성")
    # END D24-06-I01
def validate_locator(row:dict)->None:
    # BEGIN D24-06-I02
    # TODO D24-06-I02 : 문자 범위와 PDF page_number 등 자료형·조건을 확인합니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-06-I02 TODO 미완성")
    # END D24-06-I02
def select_current(rows:list[dict],pointers:dict)->list[dict]:
    # BEGIN D24-06-I03
    # TODO D24-06-I03 : 현재 공개 중인 source_version·pipeline_version 쌍만 선택합니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-06-I03 TODO 미완성")
    # END D24-06-I03
def filter_and_report(rows:list[dict],pointers:dict,category:str)->dict:
    # BEGIN D24-06-I04
    # TODO D24-06-I04 : category 필터 후 반환 건수와 제외 이유를 기록합니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-06-I04 TODO 미완성")
    # END D24-06-I04
def main():
    base={'doc_id':'DOC-ATTEND','source_locator':'attendance.md#sec-1','category':'학사',
          'pipeline_version':'ingest-e5-v1','char_start':0,'char_end':20,'page_number':None}
    items=[{**base,'chunk_id':'C1','source_version':'v1'},
           {**base,'chunk_id':'C2','source_version':'v2'},
           {**base,'chunk_id':'C3','source_version':'v2','category':'시설'}]
    report=filter_and_report(items,{'DOC-ATTEND':('v2','ingest-e5-v1')},'학사')
    out=save_json(HERE,'metadata_filter.json',report)
    show_success('06 Intermediate',out)
