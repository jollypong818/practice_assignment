"""실습 07 Basic · 기본 실행은 데이터 계약, --live-db는 실제 E5/DB 실행."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from coursekit.io import save_json, show_success
from coursekit.documents import by_doc,parse_one
from coursekit.processing import make_chunks


def select_index_chunk(doc_id:str)->tuple[dict,dict]:
    # BEGIN D24-07-B01
    # 개념·실무 해설: Indexing 입력은 검증된 Chunk의 내용과 출처입니다. 임의로 만든 384개 숫자를 E5 Embedding이라 부르지 않습니다.
    # 해설 D24-07-B01 : 기존 DOC-ASSIGN 텍스트에서 유효한 청크 1건을 선택하고 E5 passage 입력을 확인합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    doc=by_doc(doc_id)
    parsed=parse_one(doc)
    if parsed['status']!='parsed':raise ValueError('not indexable')
    chunks=make_chunks(doc,parsed['units'][0],size=110,overlap=15)
    first=chunks[0]
    if not first['body'].strip() or not first['embedding_text'].startswith('passage: '):
        raise ValueError('bad embedding input')
    return doc,first
    # END D24-07-B01


def format_hit(row:tuple)->dict:
    """DB 행: citation_id,chunk_id,body,locator,doc_id,version,distance."""
    # BEGIN D24-07-B02
    # 개념·실무 해설: 실제 DB가 발급한 citation_id는 양의 정수입니다. 반환 튜플의 필드 순서를 원문·출처·거리와 함께 명시적으로 매핑합니다.
    # 해설 D24-07-B02 : DB 검색 결과 행을 정수 citation_id·chunk_id·본문·출처·거리의 딕셔너리로 변환합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    cid,chunk_id,body,locator,doc_id,source_version,distance=row
    if type(cid) is not int or cid<=0:raise ValueError('invalid citation ID')
    return {'citation_id':cid,'chunk_id':chunk_id,'body':body,
            'source_locator':locator,'doc_id':doc_id,
            'source_version':source_version,'cosine_distance':float(distance)}
    # END D24-07-B02


def main():
    doc,chunk=select_index_chunk('DOC-ASSIGN')
    output={'source_mode':'prepared_only_not_db','chunk':chunk,
            'live_db':'not_run','sample_hit_contract':format_hit((201,chunk['chunk_id'],chunk['body'],chunk['source_locator'],doc['doc_id'],'v1',0.0))}
    if '--live-db' in sys.argv:
        from coursekit.live import connect_db,load_encoder,encode_passages,encode_query
        from coursekit.db import initialize,stage_version,publish_version,search_current,use_schema
        # 실제 모델 추론은 DB 트랜잭션 전에 수행합니다.
        model=load_encoder();vectors=encode_passages(model,[chunk])
        query=encode_query(model,'과제 파일은 어디에 보관하나요?')
        with connect_db() as conn:
            use_schema(conn,'d24_basic07')
            initialize(conn)
            with conn.transaction():
                stage_version(conn,doc,doc['file'],[chunk],vectors)
                publish_version(conn,doc['doc_id'],doc['source_version'],chunk['pipeline_version'])
            result=search_current(conn,query,category='학사',k=3)
            output['source_mode']='e5_pgvector_live'
            output['live_db']=[format_hit(r) for r in result]
    out=save_json(HERE,'indexing.json',output)
    show_success('07 Basic',out)

if __name__=='__main__':main()
