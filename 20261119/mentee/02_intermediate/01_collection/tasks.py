"""실습 01 Intermediate · run via python main.py"""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from coursekit.io import DATA,save_json,show_success,load_json
from coursekit.documents import raw_path,sha_bytes


def sort_rows(rows:list[dict])->list[dict]:
    # BEGIN D24-01-I01
    # TODO D24-01-I01 : 문서 목록을 doc_id 순으로 정렬합니다. 동일 ID가 있으면 오류로 분류합니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-01-I01 TODO 미완성")
    # END D24-01-I01
def classify(path:Path)->str:
    # BEGIN D24-01-I02
    # TODO D24-01-I02 : 확장자와 허용 집합을 비교하여 supported/unsupported를 반환합니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-01-I02 TODO 미완성")
    # END D24-01-I02
def collect_one(doc:dict)->dict:
    # BEGIN D24-01-I03
    # TODO D24-01-I03 : 파일별 원문 크기·해시 또는 읽기 실패 이유를 안전하게 기록합니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-01-I03 TODO 미완성")
    # END D24-01-I03
def collect_all(rows:list[dict])->dict:
    # BEGIN D24-01-I04
    # TODO D24-01-I04 : 모든 입력을 제외 없이 기록하고 상태별 건수 합이 입력 수와 일치하는지 검사합니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-01-I04 TODO 미완성")
    # END D24-01-I04
def main():
    result=collect_all(load_json(DATA/'manifest.json'))
    out=save_json(HERE,'manifest_report.json',result)
    show_success('01 Intermediate',out)
