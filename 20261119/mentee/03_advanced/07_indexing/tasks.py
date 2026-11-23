"""실습 07 Advanced · --live-db에서 PostgreSQL 실제 버전 전환/회귀."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from coursekit.io import DATA,save_json,show_success
from coursekit.documents import by_doc,parse_one,parse_markdown_units
from coursekit.processing import make_chunks


def prepare_revision(doc_id:str,version:str)->tuple[dict,list[dict]]:
    # BEGIN D24-07-A01
    # TODO D24-07-A01 : DOC-ATTEND v1·v2를 동일한 Markdown Parser로 처리하고, 문서 ID·원문 버전·처리 설정을 보존합니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-07-A01 TODO 미완성")
    # END D24-07-A01
def embeddings_before_db(model,chunks:list[dict]):
    # BEGIN D24-07-A02
    # TODO D24-07-A02 : E5 passage Embedding을 DB Transaction 전에 계산·검증합니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-07-A02 TODO 미완성")
    # END D24-07-A02
def stage_revision(conn,doc:dict,chunks:list[dict],vectors)->None:
    # BEGIN D24-07-A03
    # TODO D24-07-A03 : 벡터·원문·출처를 새 버전으로 Stage하고 ID 충돌을 검사합니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-07-A03 TODO 미완성")
    # END D24-07-A03
def current_pointer(conn,doc_id:str)->tuple|None:
    # BEGIN D24-07-A04
    # TODO D24-07-A04 : 현재 문서의 공개 포인터(source_version, pipeline_version)를 조회합니다. Publish는 A06에서 처리합니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-07-A04 TODO 미완성")
    # END D24-07-A04
def test_rollback(conn,doc:dict,chunks:list[dict])->dict:
    # BEGIN D24-07-A05
    # TODO D24-07-A05 : 강제로 예외를 발생시킨 Transaction에서 Rollback 후 현재 포인터가 유지되는지 확인합니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-07-A05 TODO 미완성")
    # END D24-07-A05
def publish_and_verify(conn,doc:dict,chunks:list[dict],model)->dict:
    # BEGIN D24-07-A06
    # TODO D24-07-A06 : v2를 짧은 Transaction에서 Publish하고, 정확 검색에서 이전 v1 청크가 제외되는지 확인합니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-07-A06 TODO 미완성")
    # END D24-07-A06
def main():
    v1,c1=prepare_revision('DOC-ATTEND','v1')
    v2,c2=prepare_revision('DOC-ATTEND','v2')
    report={'source_mode':'prepared_only_not_db','v1_chunks':len(c1),'v2_chunks':len(c2),
            'db_status':'not_run'}
    if '--live-db' in sys.argv:
        from coursekit.live import connect_db,load_encoder
        from coursekit.db import initialize,publish_version,use_schema
        model=load_encoder();vec1=embeddings_before_db(model,c1);vec2=embeddings_before_db(model,c2)
        with connect_db() as conn:
            use_schema(conn,'d24_adv07')
            initialize(conn)
            stage_revision(conn,v1,c1,vec1)
            # 처음 실행에서는 v1을 정상 공개해 비교 기준을 준비합니다.
            with conn.transaction():publish_version(conn,v1['doc_id'],'v1',c1[0]['pipeline_version'])
            stage_revision(conn,v2,c2,vec2)
            report['injected_failure']=test_rollback(conn,v2,c2)
            report['after_retry']=publish_and_verify(conn,v2,c2,model)
            report['source_mode']='e5_pgvector_live'
            report['db_status']='verified'
    out=save_json(HERE,'version_regression.json',report)
    show_success('07 Advanced',out)
