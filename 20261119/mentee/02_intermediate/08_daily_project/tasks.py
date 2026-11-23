"""실습 08 Intermediate · DB 없이 전체 자료 준비 단계 검증."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from coursekit.io import DATA,load_json,save_json,show_success
from coursekit.documents import parse_one
from coursekit.processing import make_chunks,clean_prose,validate_span


def read_all()->list[dict]:
    # BEGIN D24-08-I01
    # TODO D24-08-I01 : 6개 Manifest 문서를 순회하고 각 파일의 Parsing 상태를 보존합니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-08-I01 TODO 미완성")
    # END D24-08-I01
def build_chunks(results:list[dict])->list[dict]:
    # BEGIN D24-08-I02
    # TODO D24-08-I02 : parsed 문서만 Cleaning·Chunking 하며 DOC-SCAN을 정상으로 허위 처리하지 않습니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-08-I02 TODO 미완성")
    # END D24-08-I02
def count_states(results:list[dict])->dict:
    # BEGIN D24-08-I03
    # TODO D24-08-I03 : 수집 수와 parsed·needs_ocr·unsupported·error 수를 일관되게 집계합니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-08-I03 TODO 미완성")
    # END D24-08-I03
def validate_all(results:list[dict],chunks:list[dict])->dict:
    # BEGIN D24-08-I04
    # TODO D24-08-I04 : 모든 청크의 ID·원문 위치·출처·본문 일치 여부를 확인하고 Report로 출력합니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-08-I04 TODO 미완성")
    # END D24-08-I04
def main():
    results=read_all();chunks=build_chunks(results)
    report={'documents':count_states(results),'chunks':validate_all(results,chunks),
            'list':[{'doc_id':c['doc_id'],'chunk_id':c['chunk_id'],
                     'source_locator':c['source_locator']} for c in chunks]}
    out=save_json(HERE,'daily_project.json',report)
    show_success('08 Intermediate',out)
