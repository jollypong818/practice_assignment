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
    # TODO D24-08-B01 : DOC-ASSIGN의 Parsing 결과를 읽어 정제하고 110자/15자 설정으로 청크를 만듭니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-08-B01 TODO 미완성")
    doc=by_doc(doc_id)
    result=parse_one(doc)
    if result['status']!='parsed':
        raise ValueError('parse not ready')
    unit=result['units'][0]
    # ParsedUnit에서 원문 텍스트를 꺼낼 Key를 any 대신 작성하세요.
    clean=clean_prose(unit[any])
    chunks=[build_chunk(doc,unit,clean,span)
            for span in char_windows(clean,110,15)]
    return doc,clean,chunks
    # END D24-08-B01
def check_report(doc:dict,clean:str,chunks:list[dict])->dict:
    # BEGIN D24-08-B02
    # TODO D24-08-B02 : 원문 ID·Chunk 수·Span 일치 여부를 기록하고 문제가 있으면 성공으로 처리하지 않습니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-08-B02 TODO 미완성")
    if not chunks:
        raise ValueError('empty chunk list')
    for c in chunks:
        if c['doc_id']!=doc['doc_id']:
            raise ValueError('doc_id mismatch')
        # Chunk의 본문 필드가 어떤 이름인지 확인하세요.
        validate_span({'char_start':c['char_start'],'char_end':c['char_end'],
                       'text':any},clean)
    # 상태는 실제 Embedding·DB 적재가 아니라 준비가 끝났음을 의미해야 합니다.
    return {'doc_id':doc['doc_id'],'status':any,
            'chunk_count':len(chunks),'source_versions':[doc['source_version']],
            'chunk_ids':[c['chunk_id'] for c in chunks]}
    # END D24-08-B02
def main():
    doc,clean,chunks=run_pipeline('DOC-ASSIGN')
    report=check_report(doc,clean,chunks)
    out=save_json(HERE,'daily_project.json',{'report':report,'chunks':chunks})
    show_success('08 Basic',out)

if __name__=='__main__':main()
