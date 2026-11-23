"""실습 08 Advanced · 오프라인 준비 + --live-db 실제 통합 실행."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from coursekit.io import DATA,load_json,save_json,show_success
from coursekit.documents import parse_one,parse_markdown_units
from coursekit.processing import make_chunks,clean_prose,validate_span


def read_manifest()->list[dict]:
    # BEGIN D24-08-A01
    # TODO D24-08-A01 : Manifest의 빈 목록·중복 doc_id를 검사하고, unsupported 문서도 포함해 ID순 목록을 반환합니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-08-A01 TODO 미완성")
    # END D24-08-A01
def prepare_all(rows:list[dict])->tuple[list[dict],list[dict]]:
    # BEGIN D24-08-A02
    # TODO D24-08-A02 : Parsing·Cleaning·Chunking·Span 검사 후 정상 청크만 준비합니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-08-A02 TODO 미완성")
    # END D24-08-A02
def embed_batches(prepared:list[dict],model)->list[dict]:
    # BEGIN D24-08-A03
    # TODO D24-08-A03 : main()이 한 번 로드한 E5 모델을 재사용해 문서별 passage 입력 길이·벡터 정규화를 검증합니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-08-A03 TODO 미완성")
    # END D24-08-A03
def save_and_publish(conn,embedded:list[dict])->list[dict]:
    # BEGIN D24-08-A04
    # TODO D24-08-A04 : 각 문서를 분리된 Transaction에서 Stage하고 완성본만 Publish합니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-08-A04 TODO 미완성")
    # END D24-08-A04
def regression_v2(conn,model)->dict:
    # BEGIN D24-08-A05
    # TODO D24-08-A05 : v2에도 동일한 Markdown Parser를 적용하고, 실패·Rollback·정상 Publish 전후의 공개 포인터를 비교합니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-08-A05 TODO 미완성")
    # END D24-08-A05
def make_final_report(rows:list[dict],statuses:list[dict],prepared:list[dict],live:dict|None=None)->dict:
    # BEGIN D24-08-A06
    # TODO D24-08-A06 : 문서별 상태·청크 수를 기록하고, Live 실행 시에만 검색 결과·Citation ID·원문 Locator를 포함합니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-08-A06 TODO 미완성")
    # END D24-08-A06
def main():
    rows=read_manifest();prepared,statuses=prepare_all(rows)
    live=None
    if '--live-db' in sys.argv:
        from coursekit.live import connect_db,load_encoder,encode_query
        from coursekit.db import initialize,search_current,use_schema
        model=load_encoder();embedded=embed_batches(prepared,model)
        with connect_db() as conn:
            use_schema(conn,'d24_adv08')
            initialize(conn)
            committed=save_and_publish(conn,embedded)
            revision=regression_v2(conn,model)
            q=encode_query(model,'출석 기준을 알려 주세요')
            hits=search_current(conn,q,'학사',3)
            live={'published':committed,'revision':revision,
                  'hits':[{'citation_id':h[0],'chunk_id':h[1],
                           'body':h[2],'source_locator':h[3],'doc_id':h[4],
                           'source_version':h[5],'cosine_distance':h[6]} for h in hits]}
    out=save_json(HERE,'ingestion_report.json',make_final_report(rows,statuses,prepared,live))
    show_success('08 Advanced',out)
