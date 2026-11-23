"""실습 05 Advanced · 검증 Gate와 Regression."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from coursekit.io import save_json,show_success
from coursekit.processing import covered_positions


def schema_check(chunk:dict)->None:
    # BEGIN D24-05-A01
    # 개념·실무 해설: Schema 검증은 필수 필드, 올바른 타입, 양의 위치 등을 확인하는 최소 Gate입니다. 누락을 정상 데이터로 바꾸지 않습니다.
    # 해설 D24-05-A01 : 필수 필드·자료형·문자 범위를 검증합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    for name in ('chunk_id','doc_id','source_version','unit_id','body'):
        if not isinstance(chunk.get(name),str) or not chunk[name].strip():
            raise ValueError(f'missing_{name}')
    if type(chunk.get('char_start')) is not int or type(chunk.get('char_end')) is not int:
        raise ValueError('invalid_span_type')
    # END D24-05-A01


def text_match(chunk:dict,clean:str)->None:
    # BEGIN D24-05-A02
    # 개념·실무 해설: clean_text[start:end]와 저장된 Chunk 본문이 완전히 일치하는지 확인해야 Citation이 다시 원문 구간을 가리킬 수 있습니다.
    # 해설 D24-05-A02 : 청크 본문이 기준 clean_text 슬라이스와 일치하는지 확인합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    schema_check(chunk)
    a,b=chunk['char_start'],chunk['char_end']
    if not 0<=a<b<=len(clean):raise ValueError('invalid_span')
    if chunk['body']!=clean[a:b]:raise ValueError('text_mismatch')
    # END D24-05-A02


def duplicated_ids(chunks:list[dict])->list[str]:
    # BEGIN D24-05-A03
    # 개념·실무 해설: Overlap으로 일부 문자가 반복되는 것은 의도적일 수 있지만 동일 Chunk ID를 두 번 생성하는 것은 별도 오류입니다.
    # 해설 D24-05-A03 : 같은 chunk_id 중복과 의도한 overlap을 구분합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    seen=set();duplicates=set()
    for c in chunks:
        cid=c.get('chunk_id')
        if cid in seen:duplicates.add(cid)
        seen.add(cid)
    return sorted(duplicates)
    # END D24-05-A03


def coverage_stats(chunks:list[dict],clean:str)->dict:
    # BEGIN D24-05-A04
    # 개념·실무 해설: Coverage의 분모는 해당 clean_text 문자 수입니다. 중복 위치를 여러 번 더하지 않으며 원본 PDF 전체가 보존됐다는 뜻도 아닙니다.
    # 해설 D24-05-A04 : 고유 문자 위치 Coverage와 Gap·Repeat 양을 계산합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    if not clean:return {'coverage':None,'gaps':[],'repeat_extra':0}
    spans=[(c['char_start'],c['char_end']) for c in chunks]
    n,missing=covered_positions(spans,len(clean))
    return {'coverage':n/len(clean),'gaps':missing,
            'repeat_extra':sum(b-a for a,b in spans)-n}
    # END D24-05-A04


def gate(chunks:list[dict],clean:str)->dict:
    # BEGIN D24-05-A05
    # 개념·실무 해설: 격리한 입력은 사유·위치·ID를 남깁니다. 실패한 Chunk를 버리면 공개 전 검수에서 무엇이 누락됐는지 알 수 없습니다.
    # 해설 D24-05-A05 : 입력 오류별 reason code를 기록하고 통과 청크·격리 청크를 분리합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    good=[];quarantine=[];seen=set()
    for c in chunks:
        try:
            text_match(c,clean)
            if c['chunk_id'] in seen:raise ValueError('duplicate_id')
            seen.add(c['chunk_id'])
        except (ValueError,KeyError,TypeError) as exc:
            quarantine.append({'chunk_id':c.get('chunk_id'),'reason':str(exc)})
        else:good.append(c)
    return {'passed':good,'quarantine':quarantine,
            'stats':coverage_stats(good,clean)}
    # END D24-05-A05


def regression()->dict:
    # BEGIN D24-05-A06
    # 개념·실무 해설: 실패 사례 수정 후 정상 입력까지 다시 실행해야 합니다. 예외 검사를 강화하느라 정상 입력을 전부 차단하면 품질이 악화됩니다.
    # 해설 D24-05-A06 : 오류 수정 후 정상 회귀 사례를 다시 확인합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    clean='01234567890123456789'
    good=[{'chunk_id':'C1','doc_id':'DOC-TEST','source_version':'v1','unit_id':'t1',
           'char_start':0,'char_end':10,'body':clean[:10]},
          {'chunk_id':'C2','doc_id':'DOC-TEST','source_version':'v1','unit_id':'t1',
           'char_start':10,'char_end':20,'body':clean[10:]}]
    broken=[*good,{**good[0],'body':'corrupted'},good[1]]
    result=gate(broken,clean)
    if len(result['quarantine'])!=2:raise AssertionError('error cases not isolated')
    fixed=gate(good,clean)
    if len(fixed['passed'])!=2 or fixed['stats']['coverage']!=1.0:
        raise AssertionError('normal regression failed')
    return {'failure_reasons':result['quarantine'],'fixed_passed':len(fixed['passed'])}
    # END D24-05-A06


def main():
    out=save_json(HERE,'validation_gate.json',regression())
    show_success('05 Advanced',out)
