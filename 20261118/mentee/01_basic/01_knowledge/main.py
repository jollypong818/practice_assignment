"""Day23 실습 01 · 검색 대상과 ID (기본필수, mentee).

실행: python main.py --mode fixture
실제 E5/DB: python main.py --mode live  (필요한 선행 설치 후)
수강생 TODO: 3개 / 상세 요구사항은 각 함수의 주석 및 README.md.
fixture는 모의 시연이지 모델·PostgreSQL 실측 결과가 아닙니다.
"""
import argparse
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2] / 'common'))
from day23kit.data import load_knowledge
from day23kit.io import save_result


# BEGIN D23-01-B01
def select_original(rows):
    """
    TODO D23-01-B01 · select_original
        기존 수업에서 사용한 101·102·103만 ID 오름차순으로 선택합니다.
        입력: 전체 지식 목록(list[dict]). 출력: 원래 지식 3개를 담은 list.
        원본 딕셔너리의 id/title/content를 수정하지 마세요.
        개념: 원문 ID 고정·검색할 자료의 범위.
    """
    # TODO D23-01-B01: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-01-B01: 직접 구현하세요")
    return sorted()
# END D23-01-B01

# BEGIN D23-01-B02
def make_passage_input(row):
    """
    TODO D23-01-B02 · make_passage_input
        E5 문서 입력 텍스트를 "passage: 제목 본문" 형식으로 만드세요.
        입력: 지식 한 행. 출력: 문자열. 제목과 본문을 공백 하나로 구분하세요.
        개념: FAQ 질문과 달리 지식 본문을 검색 대상으로 사용합니다.
    """
    # TODO D23-01-B02: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-01-B02: 직접 구현하세요")
    return 'passage: ' + row[''] + ' ' + row['']
# END D23-01-B02

# BEGIN D23-01-B03
def make_mapping(rows):
    """
    TODO D23-01-B03 · make_mapping
        각 지식의 id/title/content/category/source_version 및 passage_input을 기록하세요.
        입력: 선택된 지식 목록. 출력: 딕셔너리 목록.
        개념: 벡터를 생성하기 전에도 원문·ID·버전을 추적해야 합니다.
    """
    # TODO D23-01-B03: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-01-B03: 직접 구현하세요")
    return [dict('') for r in rows]
# END D23-01-B03


def run(mode,level,args):
    rows=load_knowledge()
    selected=select_original(rows)
    passage=make_passage_input(selected[1])
    mapping=make_mapping(selected if level==1 else rows)
    result=dict(exercise=1,level=level,source_mode='local_snapshot',
                selected_ids=[r['id'] for r in selected],example_passage=passage,
                total_mapped=len(mapping),mapping=mapping)
    if level>=2:
        result['unique_ids']=len(reject_duplicate_ids(rows))
        result['all_fields_valid']=reject_missing_fields(rows)
    if level>=3:
        result['versions']=audit_versions(rows)
    return result


def main():
    parser=argparse.ArgumentParser(description='Day23 실습 01 · 검색 대상과 ID')
    parser.add_argument('--mode',choices=['fixture','live'],default='fixture',
        help='fixture=모의 벡터/오프라인, live=실제 E5/DB가 필요한 단계')
    args=parser.parse_args()
    result=run(args.mode,1,args)
    path=save_result(Path(__file__).resolve().parent,'exercise_01.json',result)
    import json
    print(json.dumps(result,ensure_ascii=False,indent=2,default=str))
    print('결과 저장:',path)

if __name__=='__main__':
    main()
