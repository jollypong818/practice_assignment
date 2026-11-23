"""실습 06 Basic · 본문과 설명 정보를 나눕니다."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from coursekit.io import save_json, show_success


def attach_metadata(chunk:dict,doc:dict)->dict:
    # BEGIN D24-06-B01
    # TODO D24-06-B01 : 원문 문서 ID·버전·원문 위치를 Chunk에 복사합니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-06-B01 TODO 미완성")
    # doc에서 복사할 메타데이터의 Key를 any 네 곳에 채우세요.
    return {**chunk,'doc_id':doc[any], 'source_version':doc[any],
            'category':doc[any], 'source_locator':doc[any]}
    # END D24-06-B01
def select_category(chunks:list[dict],category:str)->list[dict]:
    # BEGIN D24-06-B02
    # TODO D24-06-B02 : 주어진 category에 속하는 Chunk만 원래 순서를 보존해서 반환합니다.
    # 요구: 입력 변수·반환값의 자료형을 유지하고, 완료 기준은 README/expected를 참조하세요.
    # 힌트: 이 함수의 docstring과 상위 실행 함수에 전달되는 값을 확인합니다.
    # TODO를 완성한 뒤 아래 NotImplementedError 줄을 삭제합니다.
    raise NotImplementedError("D24-06-B02 TODO 미완성")
    # category와 비교할 Chunk의 메타데이터 Key를 any로 표시했습니다.
    return [chunk for chunk in chunks if chunk[any]==category]
    # END D24-06-B02
def main():
    a=attach_metadata({'chunk_id':'C1','body':'출석 안내'},
                     {'doc_id':'DOC-ATTEND','source_version':'v1','category':'학사',
                      'source_locator':'attendance.md#sec-1'})
    b=attach_metadata({'chunk_id':'C2','body':'시설 안내'},
                     {'doc_id':'DOC-FACILITY','source_version':'v1','category':'시설',
                      'source_locator':'facility.html#main'})
    selected=select_category([a,b],'학사')
    assert [r['chunk_id'] for r in selected]==['C1']
    out=save_json(HERE,'metadata.json',{'total':2,'selected':selected})
    show_success('06 Basic',out)

if __name__=='__main__':main()
