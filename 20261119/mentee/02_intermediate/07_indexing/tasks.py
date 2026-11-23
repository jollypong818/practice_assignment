"""실습 07 Intermediate · --live-db 필수: 실제 DB 결과를 확인할 때."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from coursekit.io import save_json,show_success
from coursekit.documents import by_doc,parse_one
from coursekit.processing import make_chunks


def prepare(doc_id:str)->tuple[dict,list[dict]]:
    # BEGIN D24-07-I01
    # TODO D24-07-I01 : 여러 ParsedUnit을 정제·분할하고 입력 청크의 출처·버전 계약을 통일합니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-07-I01 TODO 미완성")
    # END D24-07-I01
def embed(model,chunks:list[dict]):
    # BEGIN D24-07-I02
    # TODO D24-07-I02 : 실제 E5 Encoder로 384차원 passage 벡터를 만들고 개수·길이·유한값을 확인합니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-07-I02 TODO 미완성")
    # END D24-07-I02
def stage(conn,doc:dict,chunks:list[dict],vectors)->None:
    # BEGIN D24-07-I03
    # TODO D24-07-I03 : 짧은 DB Transaction 안에서 Chunk·벡터를 Staging 합니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-07-I03 TODO 미완성")
    # END D24-07-I03
def publish_search(conn,doc:dict,chunks:list[dict],model)->list[tuple]:
    # BEGIN D24-07-I04
    # TODO D24-07-I04 : 검증된 버전만 Publish하고 동일 계약의 query: 벡터로 Top-k를 조회합니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-07-I04 TODO 미완성")
    # END D24-07-I04
def main():
    doc,chunks=prepare('DOC-ASSIGN')
    result={'source_mode':'prepared_only_not_db','doc_id':doc['doc_id'],
            'chunk_count':len(chunks),'stored':'not_run','retrieved':'not_run'}
    if '--live-db' in sys.argv:
        from coursekit.live import load_encoder,connect_db
        from coursekit.db import initialize,use_schema
        model=load_encoder(); vectors=embed(model,chunks)
        with connect_db() as conn:
            use_schema(conn,'d24_inter07')
            initialize(conn);stage(conn,doc,chunks,vectors)
            hits=publish_search(conn,doc,chunks,model)
            result.update(source_mode='e5_pgvector_live',stored=len(chunks),
                          retrieved=[{'citation_id':r[0],'chunk_id':r[1],
                                      'body':r[2],'source_locator':r[3],'distance':r[6]} for r in hits])
    out=save_json(HERE,'indexing_result.json',result)
    show_success('07 Intermediate',out)
