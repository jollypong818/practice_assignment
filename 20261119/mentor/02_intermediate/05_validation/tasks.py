"""실습 05 Intermediate · 설명용 20자 경계 세트."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from coursekit.io import save_json,show_success
from coursekit.processing import covered_positions


def validate_ranges(length:int,spans:list[tuple[int,int]])->None:
    # BEGIN D24-05-I01
    # 개념·실무 해설: Schema 검증은 필수 필드, 올바른 타입, 양의 위치 등을 확인하는 최소 Gate입니다. 누락을 정상 데이터로 바꾸지 않습니다.
    # 해설 D24-05-I01 : 청크별 Span이 기준 본문의 범위 안인지 검증합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    for a,b in spans:
        if not 0<=a<b<=length:raise ValueError('invalid range')
    # END D24-05-I01


def coverage(length:int,spans:list[tuple[int,int]])->float|None:
    # BEGIN D24-05-I02
    # 개념·실무 해설: clean_text[start:end]와 저장된 Chunk 본문이 완전히 일치하는지 확인해야 Citation이 다시 원문 구간을 가리킬 수 있습니다.
    # 해설 D24-05-I02 : 합집합으로 덮은 문자 수와 Coverage를 계산합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    if length==0:return None
    validate_ranges(length,spans)
    n,_=covered_positions(spans,length)
    return n/length
    # END D24-05-I02


def detect_gaps_and_duplicates(length:int,spans:list[tuple[int,int]],ids:list[str])->dict:
    # BEGIN D24-05-I03
    # 개념·실무 해설: Overlap으로 일부 문자가 반복되는 것은 의도적일 수 있지만 동일 Chunk ID를 두 번 생성하는 것은 별도 오류입니다.
    # 해설 D24-05-I03 : 빠진 위치의 연속 구간 및 중복 Chunk ID를 구합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    _,missing=covered_positions(spans,length)
    gaps=[]
    for pos in missing:
        if gaps and gaps[-1][1]==pos:gaps[-1]=(gaps[-1][0],pos+1)
        else:gaps.append((pos,pos+1))
    seen=set();dups=[]
    for cid in ids:
        if cid in seen:dups.append(cid)
        seen.add(cid)
    return {'gaps':gaps,'duplicate_ids':sorted(set(dups))}
    # END D24-05-I03


def make_report(length:int,spans:list[tuple[int,int]],ids:list[str])->dict:
    # BEGIN D24-05-I04
    # 개념·실무 해설: Coverage의 분모는 해당 clean_text 문자 수입니다. 중복 위치를 여러 번 더하지 않으며 원본 PDF 전체가 보존됐다는 뜻도 아닙니다.
    # 해설 D24-05-I04 : 통과·오류·반복량·Coverage를 구분한 보고서를 작성합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    validate_ranges(length,spans)
    covered,_=covered_positions(spans,length)
    errors=detect_gaps_and_duplicates(length,spans,ids)
    return {'coverage':coverage(length,spans), 'covered_characters':covered,
            'repeat_extra_chars':sum(b-a for a,b in spans)-covered,
            'errors':errors,'valid':not errors['gaps'] and not errors['duplicate_ids']}
    # END D24-05-I04


def main():
    samples={'overlap':([(0,8),(6,14),(12,20)],['A','B','C']),
             'missing':([(0,8),(10,20)],['A','B']),
             'duplicate':([(0,8),(0,8),(8,20)],['A','A','C'])}
    reports={name:make_report(20,*parts) for name,parts in samples.items()}
    assert [reports[n]['coverage'] for n in samples]==[1.0,.9,1.0]
    out=save_json(HERE,'coverage_report.json',reports)
    show_success('05 Intermediate',out)
