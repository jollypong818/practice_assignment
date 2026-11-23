"""실습 06 Basic · 본문과 설명 정보를 나눕니다."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from coursekit.io import save_json, show_success


def attach_metadata(chunk:dict,doc:dict)->dict:
    # BEGIN D24-06-B01
    # 개념·실무 해설: Metadata는 본문이 아닌 관리 정보입니다. 문서 ID·원문 판·처리 판·위치를 함께 가져야 검색 결과의 근거를 설명할 수 있습니다.
    # 해설 D24-06-B01 : 원문 문서 ID·버전·원문 위치를 Chunk에 복사합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    return {**chunk,'doc_id':doc['doc_id'], 'source_version':doc['source_version'],
            'category':doc['category'], 'source_locator':doc['source_locator']}
    # END D24-06-B01


def select_category(chunks:list[dict],category:str)->list[dict]:
    # BEGIN D24-06-B02
    # 개념·실무 해설: Category 필터는 목록에서 해당 분류에 속한 행만 선택하는 처리입니다. 다른 분류의 청크를 삭제하거나 변경하지 않습니다.
    # 해설 D24-06-B02 : 주어진 category에 속하는 Chunk만 원래 순서를 보존해서 반환합니다.
    # 입력·출력은 함수 시그니처와 docstring에 따릅니다.
    # 이 블록은 예제를 따라 실행하며 검증 가능한 결과를 반환합니다.
    # 오류를 정상 성공으로 포장하지 않고 해당 원인에서 중단합니다.
    return [chunk for chunk in chunks if chunk['category']==category]
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
