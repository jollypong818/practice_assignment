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
    # 개념·실무 해설: 원본 목록에서 입력 1건이 사라지면 성공률 해석이 왜곡됩니다. 모든 doc_id의 최종 상태를 추적합니다.
    # 해설 D24-08-A01 : Manifest의 빈 목록·중복 doc_id를 검사하고, unsupported 문서도 포함해 ID순 목록을 반환합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    rows=load_json(DATA/'manifest.json')
    ids=[r['doc_id'] for r in rows]
    if len(ids)!=len(set(ids)):raise ValueError('duplicate doc_id')
    if len(rows)==0:raise ValueError('empty manifest')
    return sorted(rows,key=lambda r:r['doc_id'])
    # END D24-08-A01


def prepare_all(rows:list[dict])->tuple[list[dict],list[dict]]:
    # BEGIN D24-08-A02
    # 개념·실무 해설: 단계별로 ParsedUnit → CleanUnit → Chunk가 같은 문서/버전/원문 위치를 유지해야 합니다. clean_text 기반 Span을 검증합니다.
    # 해설 D24-08-A02 : Parsing·Cleaning·Chunking·Span 검사 후 정상 청크만 준비합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    prepared=[];statuses=[]
    for doc in rows:
        result=parse_one(doc)
        state=result['status']
        statuses.append({'doc_id':doc['doc_id'],'status':state,'reason':result.get('reason')})
        if state!='parsed':continue
        chunks=[]
        for unit in result['units']:
            clean=clean_prose(unit['raw_text'])
            for c in make_chunks(doc,unit,110,15):
                validate_span({'char_start':c['char_start'],'char_end':c['char_end'],
                               'text':c['body']},clean)
                chunks.append(c)
        if not chunks:raise ValueError(f'empty chunks: {doc["doc_id"]}')
        prepared.append({'doc':doc,'chunks':chunks})
    return prepared,statuses
    # END D24-08-A02


def embed_batches(prepared:list[dict],model)->list[dict]:
    # BEGIN D24-08-A03
    # 개념·실무 해설: 임베딩은 실제 E5 passage 입력 전체의 길이를 확인한 뒤 계산합니다. 수강생 PC에서 실행하지 않았다면 not_run으로 남깁니다.
    # 해설 D24-08-A03 : main()이 한 번 로드한 E5 모델을 재사용해 문서별 passage 입력 길이·벡터 정규화를 검증합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    from coursekit.live import encode_passages
    result=[]
    for item in prepared:
        vecs=encode_passages(model,item['chunks'])
        result.append({**item,'vectors':vecs})
    return result
    # END D24-08-A03


def save_and_publish(conn,embedded:list[dict])->list[dict]:
    # BEGIN D24-08-A04
    # 개념·실무 해설: DB 저장·공개는 문서별로 분리하면 한 문서 실패가 전체 버전 공개를 오염시키는 일을 줄일 수 있습니다.
    # 해설 D24-08-A04 : 각 문서를 분리된 Transaction에서 Stage하고 완성본만 Publish합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    from coursekit.db import stage_version,publish_version
    committed=[]
    for item in embedded:
        doc,chunks=item['doc'],item['chunks']
        with conn.transaction():
            stage_version(conn,doc,doc['file'],chunks,item['vectors'])
            publish_version(conn,doc['doc_id'],doc['source_version'],chunks[0]['pipeline_version'])
        committed.append({'doc_id':doc['doc_id'],'published_version':doc['source_version']})
    return committed
    # END D24-08-A04


def regression_v2(conn,model)->dict:
    # BEGIN D24-08-A05
    # 개념·실무 해설: v2 정상 처리 실패 시 원래 v1 공개 포인터를 보존하고, 오류 제거 후 v2로 전환되는지 회귀 검사합니다.
    # 해설 D24-08-A05 : v2에도 동일한 Markdown Parser를 적용하고, 실패·Rollback·정상 Publish 전후의 공개 포인터를 비교합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    from coursekit.db import stage_version,publish_version
    from coursekit.documents import by_doc
    from coursekit.processing import make_chunks
    from coursekit.live import encode_passages
    src=(DATA/'versions'/'attendance_v2.md').read_text(encoding='utf-8')
    doc={**by_doc('DOC-ATTEND'),'source_version':'v2'}
    # v1과 같은 제목·절별 Parser를 통과시켜 동일한 Pipeline 계약을 유지합니다.
    units=parse_markdown_units(src,'attendance_v2.md')
    chunks=[chunk for unit in units for chunk in make_chunks(doc,unit,110,15)]
    if not chunks:raise ValueError('empty v2 chunks')
    vectors=encode_passages(model,chunks)
    pointer=lambda:conn.execute('SELECT current_version FROM ingest_documents WHERE doc_id=%s',
                                (doc['doc_id'],)).fetchone()[0]
    before=pointer()
    try:
        with conn.transaction():
            stage_version(conn,doc,'versions/attendance_v2.md',chunks,vectors)
            publish_version(conn,doc['doc_id'],'v2',chunks[0]['pipeline_version'])
            raise RuntimeError('injected_failure_before_commit')
    except RuntimeError as exc:
        if str(exc)!='injected_failure_before_commit':raise
    after_failure=pointer()
    if before!=after_failure:raise ValueError('failed transaction changed public pointer')
    with conn.transaction():
        stage_version(conn,doc,'versions/attendance_v2.md',chunks,vectors)
        publish_version(conn,doc['doc_id'],'v2',chunks[0]['pipeline_version'])
    return {'before':before,'after_failure':after_failure,'after_retry':pointer()}
    # END D24-08-A05


def make_final_report(rows:list[dict],statuses:list[dict],prepared:list[dict],live:dict|None=None)->dict:
    # BEGIN D24-08-A06
    # 개념·실무 해설: 최종 Report에는 입력 수·상태 수·Chunk ID·출처·정수 Citation ID를 담습니다. 생성형 답변 API 연결은 11/20일 범위입니다.
    # 해설 D24-08-A06 : 문서별 상태·청크 수를 기록하고, Live 실행 시에만 검색 결과·Citation ID·원문 Locator를 포함합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    counts={s:sum(r['status']==s for r in statuses)
            for s in sorted({r['status'] for r in statuses})}
    if sum(counts.values())!=len(rows):raise ValueError('input count inconsistent')
    chunks=sum(len(r['chunks']) for r in prepared)
    return {'source_mode':'e5_pgvector_live' if live is not None else 'prepared_only_not_embedded',
            'document_count':len(rows),'by_status':counts,'prepared_chunk_count':chunks,
            'prepared_doc_ids':[p['doc']['doc_id'] for p in prepared],
            'live':live if live is not None else 'not_run'}
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
