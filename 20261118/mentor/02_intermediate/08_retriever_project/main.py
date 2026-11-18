"""Day23 실습 08 · AI Agent용 Retriever (응용, mentor).

실행: python main.py --mode fixture
실제 E5/DB: python main.py --mode live  (필요한 선행 설치 후)
수강생 TODO: 5개 / 상세 요구사항은 각 함수의 주석 및 README.md.
fixture는 모의 시연이지 모델·PostgreSQL 실측 결과가 아닙니다.
"""
import argparse
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2] / 'common'))
from time import perf_counter
from day23kit.io import save_result

from tasks import validate_question, retrieve_candidates, format_candidates, validate_options, make_run_report



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
    result=run(args.mode,2,args)
    path=save_result(Path(__file__).resolve().parent,'exercise_08.json',result)
    import json
    print(json.dumps(result,ensure_ascii=False,indent=2,default=str))
    print('결과 저장:',path)

if __name__=='__main__':
    main()
