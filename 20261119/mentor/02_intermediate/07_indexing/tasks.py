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
    # 개념·실무 해설: Indexing 입력은 검증된 Chunk의 내용과 출처입니다. 임의로 만든 384개 숫자를 E5 Embedding이라 부르지 않습니다.
    # 해설 D24-07-I01 : 여러 ParsedUnit을 정제·분할하고 입력 청크의 출처·버전 계약을 통일합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    doc=by_doc(doc_id);parsed=parse_one(doc)
    if parsed['status']!='parsed':raise ValueError(parsed['status'])
    chunks=[]
    for unit in parsed['units']:
        chunks.extend(make_chunks(doc,unit,size=110,overlap=15))
    if not chunks:raise ValueError('empty chunk set')
    return doc,chunks
    # END D24-07-I01


def embed(model,chunks:list[dict]):
    # BEGIN D24-07-I02
    # 개념·실무 해설: E5 모델은 한 번 로드해서 CPU로 추론합니다. passage와 query의 접두어, 모델 ID, 정규화, 차원을 동일 계약으로 유지합니다.
    # 해설 D24-07-I02 : 실제 E5 Encoder로 384차원 passage 벡터를 만들고 개수·길이·유한값을 확인합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    from coursekit.live import encode_passages
    return encode_passages(model,chunks)
    # END D24-07-I02


def stage(conn,doc:dict,chunks:list[dict],vectors)->None:
    # BEGIN D24-07-I03
    # 개념·실무 해설: Stage는 아직 조회에 노출되지 않은 새 버전을 DB에 저장하는 단계입니다. 같은 Chunk ID의 본문 불일치는 조용히 덮어쓰지 않습니다.
    # 해설 D24-07-I03 : 짧은 DB Transaction 안에서 Chunk·벡터를 Staging 합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    from coursekit.db import stage_version
    with conn.transaction():
        stage_version(conn,doc,doc['file'],chunks,vectors)
    # END D24-07-I03


def publish_search(conn,doc:dict,chunks:list[dict],model)->list[tuple]:
    # BEGIN D24-07-I04
    # 개념·실무 해설: Publish는 staging된 대상의 수와 상태를 검증하고 현재 포인터 쌍을 변경하는 짧은 Transaction으로 처리합니다.
    # 해설 D24-07-I04 : 검증된 버전만 Publish하고 동일 계약의 query: 벡터로 Top-k를 조회합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    from coursekit.db import publish_version,search_current
    from coursekit.live import encode_query
    with conn.transaction():
        publish_version(conn,doc['doc_id'],doc['source_version'],chunks[0]['pipeline_version'])
    qvec=encode_query(model,'과제 파일은 어디에 보관하나요?')
    return search_current(conn,qvec,category='학사',k=3)
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
