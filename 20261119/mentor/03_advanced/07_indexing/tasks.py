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
    # 개념·실무 해설: Indexing 입력은 검증된 Chunk의 내용과 출처입니다. 임의로 만든 384개 숫자를 E5 Embedding이라 부르지 않습니다.
    # 해설 D24-07-A01 : DOC-ATTEND v1·v2를 동일한 Markdown Parser로 처리하고, 문서 ID·원문 버전·처리 설정을 보존합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    doc=by_doc(doc_id).copy()
    if version not in {'v1','v2'}:raise ValueError('unsupported source version')
    if version=='v1':
        parsed=parse_one(doc)
    else:
        src=(DATA/'versions'/'attendance_v2.md').read_text(encoding='utf-8')
        # 개정 v2도 v1과 동일한 Markdown Parser를 사용합니다.
        # 문서 구조(# 제목/## 절)가 바뀌지 않았으므로 원문 버전만 구분합니다.
        doc['source_version']='v2'
        parsed={'status':'parsed','units':parse_markdown_units(src,'attendance_v2.md')}
    if parsed['status']!='parsed':raise ValueError(parsed['status'])
    chunks=[]
    for u in parsed['units']:chunks.extend(make_chunks(doc,u,110,15))
    return doc,chunks
    # END D24-07-A01


def embeddings_before_db(model,chunks:list[dict]):
    # BEGIN D24-07-A02
    # 개념·실무 해설: E5 모델은 한 번 로드해서 CPU로 추론합니다. passage와 query의 접두어, 모델 ID, 정규화, 차원을 동일 계약으로 유지합니다.
    # 해설 D24-07-A02 : E5 passage Embedding을 DB Transaction 전에 계산·검증합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    from coursekit.live import encode_passages
    vectors=encode_passages(model,chunks)
    if len(chunks)!=len(vectors):raise ValueError('vector count mismatch')
    return vectors
    # END D24-07-A02


def stage_revision(conn,doc:dict,chunks:list[dict],vectors)->None:
    # BEGIN D24-07-A03
    # 개념·실무 해설: Stage는 아직 조회에 노출되지 않은 새 버전을 DB에 저장하는 단계입니다. 같은 Chunk ID의 본문 불일치는 조용히 덮어쓰지 않습니다.
    # 해설 D24-07-A03 : 벡터·원문·출처를 새 버전으로 Stage하고 ID 충돌을 검사합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    from coursekit.db import stage_version
    with conn.transaction():
        stage_version(conn,doc,doc['file'],chunks,vectors)
    # END D24-07-A03


def current_pointer(conn,doc_id:str)->tuple|None:
    # BEGIN D24-07-A04
    # 개념·실무 해설: 현재 포인터를 읽는 SELECT는 데이터를 변경하지 않습니다. 실제 Ready 검증·Publish는 A06의 Transaction에서 수행합니다.
    # 해설 D24-07-A04 : 현재 문서의 공개 포인터(source_version, pipeline_version)를 조회합니다. Publish는 A06에서 처리합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    return conn.execute('SELECT current_version,current_pipeline_version FROM ingest_documents '
                        'WHERE doc_id=%s',(doc_id,)).fetchone()
    # END D24-07-A04


def test_rollback(conn,doc:dict,chunks:list[dict])->dict:
    # BEGIN D24-07-A05
    # 개념·실무 해설: 의도적 오류는 학생 개인의 ingest_ 전용 Schema 안에서만 실행합니다. Rollback 이후 current pointer가 바뀌지 않은지 확인합니다.
    # 해설 D24-07-A05 : 강제로 예외를 발생시킨 Transaction에서 Rollback 후 현재 포인터가 유지되는지 확인합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    from coursekit.db import publish_version
    before=current_pointer(conn,doc['doc_id'])
    try:
        with conn.transaction():
            publish_version(conn,doc['doc_id'],doc['source_version'],chunks[0]['pipeline_version'])
            raise RuntimeError('injected_rollback_before_commit')
    except RuntimeError as exc:
        if str(exc)!='injected_rollback_before_commit':raise
    after=current_pointer(conn,doc['doc_id'])
    if before!=after:raise ValueError('rollback failed: pointer changed')
    return {'rollback_ok':True,'pointer_before':before,'pointer_after':after}
    # END D24-07-A05


def publish_and_verify(conn,doc:dict,chunks:list[dict],model)->dict:
    # BEGIN D24-07-A06
    # 개념·실무 해설: v2 공개 후에는 이전 v1 청크가 현재 검색 결과에 섞이지 않아야 합니다. 반환된 원문·ID·버전을 확인합니다. 이 예제는 청크 수 감소를 검증하지 않습니다.
    # 해설 D24-07-A06 : v2를 짧은 Transaction에서 Publish하고, 정확 검색에서 이전 v1 청크가 제외되는지 확인합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    from coursekit.db import publish_version,search_current
    from coursekit.live import encode_query
    with conn.transaction():
        publish_version(conn,doc['doc_id'],doc['source_version'],chunks[0]['pipeline_version'])
    pointer=current_pointer(conn,doc['doc_id'])
    if pointer!=(doc['source_version'],chunks[0]['pipeline_version']):
        raise ValueError('publish pointer mismatch')
    query=encode_query(model,'15분 늦으면 어떻게 기록되나요?')
    hits=search_current(conn,query,'학사',k=10)
    mine=[h for h in hits if h[4]==doc['doc_id']]
    if any(h[5]!=doc['source_version'] for h in mine):raise ValueError('stale version in current search')
    return {'pointer':pointer,'hits_for_this_document':len(mine),
            'source_versions':[h[5] for h in mine]}
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
