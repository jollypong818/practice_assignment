"""Day23 실습 08 · AI Agent용 Retriever (기본필수, mentor).

실행: python main.py --mode fixture
실제 E5/DB: python main.py --mode live  (필요한 선행 설치 후)
수강생 TODO: 3개 / 상세 요구사항은 각 함수의 주석 및 README.md.
fixture는 모의 시연이지 모델·PostgreSQL 실측 결과가 아닙니다.
"""
import argparse
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2] / 'common'))
from time import perf_counter
from day23kit.fixtures import fixture_search
from day23kit.embedding import get_encoder, encode_question
from day23kit.db import connect_db, exact_topk, check_data_ready
from day23kit.io import save_result


# BEGIN D23-08-B01
def validate_question(question):
    """
    [강사용 정답] D23-08-B01 · validate_question
        질문은 1자 이상의 문자열이어야 하며 앞뒤 공백을 제거하세요.
        빈 값/공백만 있는 값이면 ValueError. 반환은 정리된 질문.
        API가 연결되어 있지 않아도 검사 가능한 순수 함수입니다.
    """
    # 해설 D23-08-B01: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    if not isinstance(question,str) or not question.strip():raise ValueError('empty_question')
    return question.strip()
# END D23-08-B01

# BEGIN D23-08-B02
def retrieve_candidates(question,mode,k,category,env_file):
    """
    [강사용 정답] D23-08-B02 · retrieve_candidates
        fixture면 교육용 fixture_search, live면 E5 query Embedding → pgvector Exact SQL을 사용하세요.
        실제 live는 exercise05에서 9개 자료를 먼저 저장해야 합니다.
        DB 연결 실패를 빈 결과 []로 바꾸지 말고 예외를 전달하세요.
    """
    # 해설 D23-08-B02: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    if mode=='fixture':return fixture_search(question,k,category)
    encoder=get_encoder('live')
    qvec=encode_question(encoder,question)
    # 실제 연결은 명시적으로 --mode live를 지정한 경우에만 만듭니다.
    with connect_db(env_file) as conn:
        check_data_ready(conn)
        return exact_topk(conn,qvec,k,category)
# END D23-08-B02

# BEGIN D23-08-B03
def format_candidates(hits):
    """
    [강사용 정답] D23-08-B03 · format_candidates
        후보의 id/title/content/category/source_version/distance를 반환하세요.
        검색된 원문을 요약·변조하지 않고, distance는 숫자 그대로 둡니다.
        답변 상태(answered)를 자동으로 부여하지 마세요.
    """
    # 해설 D23-08-B03: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    return [{'id':h['id'],'title':h['title'],'content':h['content'],
             'category':h['category'],'source_version':h['source_version'],
             'distance':round(float(h['distance']),6)} for h in hits]
# END D23-08-B03


def run(mode,level,args):
    question=validate_question(getattr(args,'question','서버는 어디에서 실행하나요?'))
    k=3 if level==1 else args.k
    category=None if level==1 else args.category
    if level>=2:options=validate_options(k,category)
    else:options={'k':k,'category':category}
    t0=perf_counter()
    hits=retrieve_candidates(question,mode,options['k'],options['category'],Path(__file__).with_name('.env'))
    elapsed=(perf_counter()-t0)*1000
    formatted=format_candidates(hits)
    result=dict(exercise=8,level=level,source_mode='simulated' if mode=='fixture' else 'pgvector_exact',question=question,options=options,
                retrieved=formatted,retrieved_count=len(formatted),human_evidence_ok=None,
                next_step='검토 후 Context 후보로 전달; LLM 답변 생성은 Day25 RAG에서 수행')
    if level>=2:result['run_report']=make_run_report(question,hits,mode,elapsed)
    if level>=3:result['contract_check']=check_model_and_versions(hits,mode)
    return result


def main():
    parser=argparse.ArgumentParser(description='Day23 실습 08 · AI Agent용 Retriever')
    parser.add_argument('--mode',choices=['fixture','live'],default='fixture',
        help='fixture=모의 벡터/오프라인, live=실제 E5/DB가 필요한 단계')

    parser.add_argument('--question',default='서버는 어디에서 실행하나요?',help='검색 질문')
    parser.add_argument('--k',type=int,default=3,help='반환할 최대 검색 후보 (1~9)')
    parser.add_argument('--category',default=None,choices=['course','development','support'],help='Metadata 분류 필터')
    args=parser.parse_args()
    result=run(args.mode,1,args)
    path=save_result(Path(__file__).resolve().parent,'exercise_08.json',result)
    import json
    print(json.dumps(result,ensure_ascii=False,indent=2,default=str))
    print('결과 저장:',path)

if __name__=='__main__':
    main()
