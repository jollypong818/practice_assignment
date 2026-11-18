"""Day23 실습 07 · 검색 결과 정성평가 (기본필수, mentee).

실행: python main.py --mode fixture
실제 E5/DB: python main.py --mode live  (필요한 선행 설치 후)
수강생 TODO: 3개 / 상세 요구사항은 각 함수의 주석 및 README.md.
fixture는 모의 시연이지 모델·PostgreSQL 실측 결과가 아닙니다.
"""
import argparse
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2] / 'common'))
from day23kit.fixtures import fixture_search
from day23kit.embedding import get_encoder, encode_question
from day23kit.db import connect_db, exact_topk, check_data_ready
from day23kit.io import save_result


# BEGIN D23-07-B01
def make_casebook():
    """
    TODO D23-07-B01 · make_casebook
        강의의 질문 3종과 확인할 지식 ID를 구성하세요.
        server(102), retention(101: 보관 기간 없음), error(103/108).
        자동 생성한 정답이 아니라 사람이 평가할 고정 기준 샘플임을 표시합니다.
    """
    # TODO D23-07-B01: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-07-B01: 직접 구현하세요")
    return [{'case_id': '', 'question': '', 'reference_ids': []}]
# END D23-07-B01

# BEGIN D23-07-B02
def judge_training_reference(case_id,doc_id):
    """
    TODO D23-07-B02 · judge_training_reference
        교안에 미리 주어진 원문 근거로 관련/부분 관련/무관을 수동 기준표로 판정하세요.
        server:102 관련,106 부분 관련. retention:101 부분 관련(기간 없음).
        error:103,108 관련. 그 밖에는 무관.
        *이 표는 사람이 만든 교육용 기준이며 모델 검색 평가점수가 아닙니다.*
    """
    # TODO D23-07-B02: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-07-B02: 직접 구현하세요")
    gold = {'server': {}, 'retention': {}, 'error': {}}
    return gold[case_id].get(doc_id, '')
# END D23-07-B02

# BEGIN D23-07-B03
def make_review_row(case,hit):
    """
    TODO D23-07-B03 · make_review_row
        질문 ID·검색된 ID·본문·거리·교재 기준 라벨을 한 행으로 만드세요.
        distance는 정답 확률로 표현하지 않습니다.
        human_reviewed는 False로 두어 실제 수강생의 근거 검토 전임을 표시합니다.
    """
    # TODO D23-07-B03: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-07-B03: 직접 구현하세요")
    return dict(case_id=case[''], retrieved_id=hit[''], human_reviewed=False)
# END D23-07-B03


def run(mode,level,args):
    cases=make_casebook()
    reviews=[]; search_state=[]
    for case in cases:
        # 검색 자체는 fixture의 수학 예시 또는 실제 E5/pgvector.
        if mode=='fixture':hits=fixture_search(case['question'],k=3)
        else:
            if '_live_cache' not in locals():
                encoder=get_encoder('live')
                conn=connect_db(Path(__file__).with_name('.env'))
                check_data_ready(conn)
                _live_cache=True
            qvec=encode_question(encoder,case['question'])
            hits=exact_topk(conn,qvec,3)
        search_state.append({'case_id':case['case_id'],'state':classify_search_state(hits) if level>=2 else ('candidates' if hits else 'empty')})
        for hit in hits:
            row=make_review_row(case,hit)
            row['source_version']=hit['source_version']
            reviews.append(row)
    result=dict(exercise=7,level=level,source_mode='simulated' if mode=='fixture' else 'pgvector_exact',
                review_rows=reviews,search_states=search_state,
                human_evidence_ok=None)
    if level>=2:
        if mode=='live':
            qvec=encode_question(encoder,'서버는 어디에서 실행하나요?')
            baseline=[h['id'] for h in exact_topk(conn,qvec,k=3)]
            filtered=[h['id'] for h in exact_topk(conn,qvec,k=3,category='development')]
        else:
            baseline=[h['id'] for h in fixture_search('서버는 어디에서 실행하나요?',k=3)]
            filtered=[h['id'] for h in fixture_search('서버는 어디에서 실행하나요?',k=3,category='development')]
        result['filter_effect']=review_filter_effect(baseline,filtered)
        result['empty_is_not_error']=classify_search_state([])=='empty' and classify_search_state([],error='DB 연결 오류')=='error'
    if level>=3:result['evaluation_integrity']=check_evaluation_integrity(reviews)
    if mode=='live':conn.close()
    return result


def main():
    parser=argparse.ArgumentParser(description='Day23 실습 07 · 검색 결과 정성평가')
    parser.add_argument('--mode',choices=['fixture','live'],default='fixture',
        help='fixture=모의 벡터/오프라인, live=실제 E5/DB가 필요한 단계')
    args=parser.parse_args()
    result=run(args.mode,1,args)
    path=save_result(Path(__file__).resolve().parent,'exercise_07.json',result)
    import json
    print(json.dumps(result,ensure_ascii=False,indent=2,default=str))
    print('결과 저장:',path)

if __name__=='__main__':
    main()
