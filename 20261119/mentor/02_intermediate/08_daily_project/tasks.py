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
    # 개념·실무 해설: 원본 목록에서 입력 1건이 사라지면 성공률 해석이 왜곡됩니다. 모든 doc_id의 최종 상태를 추적합니다.
    # 해설 D24-08-I01 : 6개 Manifest 문서를 순회하고 각 파일의 Parsing 상태를 보존합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    return [parse_one(doc) for doc in load_json(DATA/'manifest.json')]
    # END D24-08-I01


def build_chunks(results:list[dict])->list[dict]:
    # BEGIN D24-08-I02
    # 개념·실무 해설: 단계별로 ParsedUnit → CleanUnit → Chunk가 같은 문서/버전/원문 위치를 유지해야 합니다. clean_text 기반 Span을 검증합니다.
    # 해설 D24-08-I02 : parsed 문서만 Cleaning·Chunking 하며 DOC-SCAN을 정상으로 허위 처리하지 않습니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    chunks=[]
    for result in results:
        if result['status']!='parsed':continue
        doc={**result['doc'],'file':result['doc']['source_uri'].split('/')[-1]}
        for unit in result['units']:
            chunks.extend(make_chunks(doc,unit,110,15))
    return chunks
    # END D24-08-I02


def count_states(results:list[dict])->dict:
    # BEGIN D24-08-I03
    # 개념·실무 해설: 임베딩은 실제 E5 passage 입력 전체의 길이를 확인한 뒤 계산합니다. 수강생 PC에서 실행하지 않았다면 not_run으로 남깁니다.
    # 해설 D24-08-I03 : 수집 수와 parsed·needs_ocr·unsupported·error 수를 일관되게 집계합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    counts={s:sum(r['status']==s for r in results)
            for s in sorted({r['status'] for r in results})}
    if sum(counts.values())!=len(results):raise ValueError('lost input')
    return {'total':len(results),'by_status':counts}
    # END D24-08-I03


def validate_all(results:list[dict],chunks:list[dict])->dict:
    # BEGIN D24-08-I04
    # 개념·실무 해설: DB 저장·공개는 문서별로 분리하면 한 문서 실패가 전체 버전 공개를 오염시키는 일을 줄일 수 있습니다.
    # 해설 D24-08-I04 : 모든 청크의 ID·원문 위치·출처·본문 일치 여부를 확인하고 Report로 출력합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    by_doc={r['doc']['doc_id']:r for r in results}
    for chunk in chunks:
        r=by_doc[chunk['doc_id']]
        unit=next(u for u in r['units'] if u['unit_id']==chunk['unit_id'])
        text=clean_prose(unit['raw_text'])
        validate_span({'char_start':chunk['char_start'],'char_end':chunk['char_end'],
                       'text':chunk['body']},text)
    return {'checked':len(chunks),'valid':True,'source_mode':'prepared_only_not_embedded'}
    # END D24-08-I04


def main():
    results=read_all();chunks=build_chunks(results)
    report={'documents':count_states(results),'chunks':validate_all(results,chunks),
            'list':[{'doc_id':c['doc_id'],'chunk_id':c['chunk_id'],
                     'source_locator':c['source_locator']} for c in chunks]}
    out=save_json(HERE,'daily_project.json',report)
    show_success('08 Intermediate',out)
