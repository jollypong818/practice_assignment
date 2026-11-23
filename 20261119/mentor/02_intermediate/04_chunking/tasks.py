"""실습 04 Intermediate · --live-e5 시 실제 토크나이저 사용."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from coursekit.io import save_json,show_success
from coursekit.documents import by_doc,parse_one
from coursekit.processing import clean_prose,char_windows,build_chunk,token_len


def split_one(doc:dict,unit:dict,size=70,overlap=10)->tuple[str,list[dict]]:
    # BEGIN D24-04-I01
    # 개념·실무 해설: Chunk Span은 본문의 Python 문자 Offset입니다. 바이트 위치나 Token ID가 아닙니다. 원문 구간을 그대로 슬라이스해야 역추적할 수 있습니다.
    # 해설 D24-04-I01 : 하나의 ParsedUnit을 clean_text에서 문자 창으로 분할합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    text=clean_prose(unit['raw_text'])
    return text,list(char_windows(text,size,overlap))
    # END D24-04-I01


def attach_chunks(doc:dict,unit:dict,text:str,spans:list[dict])->list[dict]:
    # BEGIN D24-04-I02
    # 개념·실무 해설: Chunk Size·Overlap은 0≤overlap<size를 만족해야 합니다. 창이 끝에 닿은 순간 종료해야 중복 꼬리 Chunk가 생기지 않습니다.
    # 해설 D24-04-I02 : 각 창에 doc_id·unit_id·버전·Locator와 passage: 접두어를 전달합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    return [build_chunk(doc,unit,text,s) for s in spans]
    # END D24-04-I02


def measure(chunks:list[dict],model=None)->list[dict]:
    # BEGIN D24-04-I03
    # 개념·실무 해설: 문서·unit의 경계를 넘어 데이터를 합치지 않습니다. 같은 메타데이터를 Chunk로 정확히 상속시켜 출처가 뒤섞이지 않도록 합니다.
    # 해설 D24-04-I03 : SentenceTransformer 모델이 주어졌을 때 특수 토큰 포함 길이를 측정합니다. 모델이 없으면 not_run으로 기록합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    if model is None:return [{**c,'token_count':None,'token_status':'not_run'} for c in chunks]
    return [{**c,'token_count':token_len(model,c['embedding_text']),'token_status':'measured'}
            for c in chunks]
    # END D24-04-I03


def enforce_limit(chunks:list[dict],model=None)->dict:
    # BEGIN D24-04-I04
    # 개념·실무 해설: E5 본문은 반드시 `passage: ` 접두어를 포함하고, title 추가 여부는 입력 계약으로 고정합니다. Offset에는 title 접두어를 섞지 않습니다.
    # 해설 D24-04-I04 : 최대 입력 길이를 초과한 청크를 통과시키지 않고 개수와 ID를 기록합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    if model is None:return {'status':'not_run','too_long_ids':[], 'checked':0}
    overs=[c['chunk_id'] for c in chunks if c['token_count'] is not None
          and c['token_count']>model.max_seq_length]
    return {'status':'failed' if overs else 'pass','too_long_ids':overs,'checked':len(chunks)}
    # END D24-04-I04


def main():
    model=None
    if '--live-e5' in sys.argv:
        from coursekit.live import load_encoder
        model=load_encoder()
    all_chunks=[]
    for doc_id in ('DOC-ATTEND','DOC-ASSIGN'):
        doc=by_doc(doc_id)
        for unit in parse_one(doc)['units']:
            text,spans=split_one(doc,unit)
            all_chunks.extend(attach_chunks(doc,unit,text,spans))
    measured=measure(all_chunks,model)
    report=enforce_limit(measured,model)
    out=save_json(HERE,'chunking_report.json',{'chunks':measured,'token_validation':report})
    show_success('04 Intermediate',out)
