"""실습 08 Basic · Checkpoint를 연결합니다. LLM 답변 생성은 하지 않습니다."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from coursekit.io import save_json,show_success
from coursekit.documents import by_doc,parse_one
from coursekit.processing import clean_prose,char_windows,build_chunk,validate_span


def run_pipeline(doc_id:str)->tuple[dict,str,list[dict]]:
    # BEGIN D24-08-B01
    # 개념·실무 해설: 원본 목록에서 입력 1건이 사라지면 성공률 해석이 왜곡됩니다. 모든 doc_id의 최종 상태를 추적합니다.
    # 해설 D24-08-B01 : DOC-ASSIGN의 Parsing 결과를 읽어 정제하고 110자/15자 설정으로 청크를 만듭니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    doc=by_doc(doc_id);result=parse_one(doc)
    if result['status']!='parsed':raise ValueError('parse not ready')
    unit=result['units'][0]
    clean=clean_prose(unit['raw_text'])
    chunks=[build_chunk(doc,unit,clean,span)
            for span in char_windows(clean,110,15)]
    return doc,clean,chunks
    # END D24-08-B01


def check_report(doc:dict,clean:str,chunks:list[dict])->dict:
    # BEGIN D24-08-B02
    # 개념·실무 해설: 단계별로 ParsedUnit → CleanUnit → Chunk가 같은 문서/버전/원문 위치를 유지해야 합니다. clean_text 기반 Span을 검증합니다.
    # 해설 D24-08-B02 : 원문 ID·Chunk 수·Span 일치 여부를 기록하고 문제가 있으면 성공으로 처리하지 않습니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    if not chunks:raise ValueError('empty chunk list')
    for c in chunks:
        if c['doc_id']!=doc['doc_id']:raise ValueError('doc_id mismatch')
        validate_span({'char_start':c['char_start'],'char_end':c['char_end'],'text':c['body']},clean)
    return {'doc_id':doc['doc_id'],'status':'prepared_not_embedded',
            'chunk_count':len(chunks),'source_versions':[doc['source_version']],
            'chunk_ids':[c['chunk_id'] for c in chunks]}
    # END D24-08-B02


def main():
    doc,clean,chunks=run_pipeline('DOC-ASSIGN')
    report=check_report(doc,clean,chunks)
    out=save_json(HERE,'daily_project.json',{'report':report,'chunks':chunks})
    show_success('08 Basic',out)

if __name__=='__main__':main()
