"""실습 04 Advanced · 구조 우선, 긴 부분 재분할; --live-e5는 모델 길이 측정."""
from pathlib import Path
import hashlib,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from coursekit.io import save_json,show_success
from coursekit.documents import by_doc,parse_one
from coursekit.processing import clean_prose,char_windows,build_chunk,token_len


def paragraph_spans(text:str)->list[dict]:
    # BEGIN D24-04-A01
    # 개념·실무 해설: Chunk Span은 본문의 Python 문자 Offset입니다. 바이트 위치나 Token ID가 아닙니다. 원문 구간을 그대로 슬라이스해야 역추적할 수 있습니다.
    # 해설 D24-04-A01 : 문단 경계 후보를 찾아 원문 구간을 정확히 추출합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    result=[];cursor=0
    for para in text.split('\n'):
        if not para.strip():cursor+=len(para)+1;continue
        index=text.find(para,cursor)
        if index<0:raise ValueError('paragraph position mismatch')
        result.append({'char_start':index,'char_end':index+len(para),'text':para})
        cursor=index+len(para)+1
    return result
    # END D24-04-A01


def split_long(text:str,spans:list[dict],size=90,overlap=15)->list[dict]:
    # BEGIN D24-04-A02
    # 개념·실무 해설: Chunk Size·Overlap은 0≤overlap<size를 만족해야 합니다. 창이 끝에 닿은 순간 종료해야 중복 꼬리 Chunk가 생기지 않습니다.
    # 해설 D24-04-A02 : 긴 문단만 문자 창으로 재분할하며 짧은 문단은 그대로 유지합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    out=[]
    for s in spans:
        if len(s['text'])<=size:
            out.append(s)
        else:
            for w in char_windows(s['text'],size,overlap):
                a=s['char_start']+w['char_start'];b=s['char_start']+w['char_end']
                out.append({'char_start':a,'char_end':b,'text':text[a:b]})
    return out
    # END D24-04-A02


def make_records(doc:dict,unit:dict,clean:str,spans:list[dict])->list[dict]:
    # BEGIN D24-04-A03
    # 개념·실무 해설: 문서·unit의 경계를 넘어 데이터를 합치지 않습니다. 같은 메타데이터를 Chunk로 정확히 상속시켜 출처가 뒤섞이지 않도록 합니다.
    # 해설 D24-04-A03 : 각 Span을 doc_id·unit_id·source_locator에 연결해 Chunk를 만듭니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    return [build_chunk(doc,unit,clean,s) for s in spans]
    # END D24-04-A03


def embedding_input(chunk:dict,include_title:bool)->str:
    # BEGIN D24-04-A04
    # 개념·실무 해설: E5 본문은 반드시 `passage: ` 접두어를 포함하고, title 추가 여부는 입력 계약으로 고정합니다. Offset에는 title 접두어를 섞지 않습니다.
    # 해설 D24-04-A04 : 본문과 선택적 제목을 합쳐 `passage: ` 입력을 만들고 Offset과 분리합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    title=chunk.get('section_title','').strip()
    body=(title+'\n'+chunk['body']) if include_title and title else chunk['body']
    return 'passage: '+body
    # END D24-04-A04


def check_model_lengths(chunks:list[dict],model=None)->dict:
    # BEGIN D24-04-A05
    # 개념·실무 해설: Token 길이는 실제 E5 Tokenizer로 `add_special_tokens=True`, `truncation=False` 상태에서 재야 합니다. 384차원은 384 Token 허용을 의미하지 않습니다.
    # 해설 D24-04-A05 : 모델이 제공되면 Tokenizer로 길이를 측정하고 초과 결과를 격리합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    if model is None:return {'status':'not_run','checked':0,'oversize_ids':[]}
    overs=[]
    for chunk in chunks:
        t=embedding_input(chunk,True)
        if token_len(model,t)>model.max_seq_length:overs.append(chunk['chunk_id'])
    return {'status':'pass' if not overs else 'quarantine',
            'checked':len(chunks),'oversize_ids':overs}
    # END D24-04-A05


def check_repeat(doc:dict,unit:dict)->dict:
    # BEGIN D24-04-A06
    # 개념·실무 해설: 분할의 재실행에서 Chunk ID·Span·본문이 같아야 합니다. 모델/분할 조건이 바뀌면 pipeline_version도 변경해야 합니다.
    # 해설 D24-04-A06 : 동일 원문·설정의 재실행에서 Chunk ID·본문·문자 범위가 동일한지 검사합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    clean=clean_prose(unit['raw_text'])
    def make():
        return make_records(doc,unit,clean,split_long(clean,paragraph_spans(clean)))
    first=make();second=make()
    a=[(r['chunk_id'],r['char_start'],r['char_end'],r['body']) for r in first]
    b=[(r['chunk_id'],r['char_start'],r['char_end'],r['body']) for r in second]
    if a!=b:raise ValueError('unstable chunking')
    return {'chunks':first,'stable':True}
    # END D24-04-A06


def main():
    doc=by_doc('DOC-ATTEND');unit=parse_one(doc)['units'][0]
    result=check_repeat(doc,unit)
    model=None
    if '--live-e5' in sys.argv:
        from coursekit.live import load_encoder
        model=load_encoder()
    result['token_check']=check_model_lengths(result['chunks'],model)
    result['embedding_input_contract']='passage: [optional title] + body'
    out=save_json(HERE,'structure_chunks.json',result)
    show_success('04 Advanced',out)
