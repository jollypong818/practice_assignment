"""Day23 실습 03 · E5 문장 Embedding (기본필수, mentor).

실행: python main.py --mode fixture
실제 E5/DB: python main.py --mode live  (필요한 선행 설치 후)
수강생 TODO: 3개 / 상세 요구사항은 각 함수의 주석 및 README.md.
fixture는 모의 시연이지 모델·PostgreSQL 실측 결과가 아닙니다.
"""
import argparse
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2] / 'common'))
import numpy as np
from day23kit.data import load_knowledge, passage_text, E5_MODEL_ID
from day23kit.embedding import get_encoder
from day23kit.io import save_result


# BEGIN D23-03-B01
def make_passages(rows):
    """
    [강사용 정답] D23-03-B01 · make_passages
        지식 목록을 E5 문서 입력 문자열 목록으로 변환하세요.
        문서에는 'passage: ' + 제목 + ' ' + 본문을 사용합니다.
        한 행마다 정확히 한 문자열을 만들어 순서를 유지하세요.
    """
    # 해설 D23-03-B01: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    # 문서마다 고정된 순서로 passage를 구성하여 ID와 행 인덱스를 보존합니다.
    return [passage_text(row) for row in rows]
# END D23-03-B01

# BEGIN D23-03-B02
def make_queries(questions):
    """
    [강사용 정답] D23-03-B02 · make_queries
        질문 목록 각 요소 앞에 query: 공백을 붙이세요.
        출력: 입력과 동일한 순서의 문자열 리스트.
        빈 질문을 추가해 그럴듯한 벡터를 만들지 마세요.
    """
    # 해설 D23-03-B02: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    return ['query: '+q for q in questions]
# END D23-03-B02

# BEGIN D23-03-B03
def encode_both(encoder,passages,queries):
    """
    [강사용 정답] D23-03-B03 · encode_both
        같은 Encoder에 문서와 질문을 나누어 encode하세요.
        반드시 normalize_embeddings=True, convert_to_numpy=True를 전달합니다.
        결과: (doc_vectors, query_vectors). 기본필수의 모의 모드와
        --mode live의 E5 실측을 구분하여 같은 API를 사용합니다.
    """
    # 해설 D23-03-B03: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    # 동일 모델로 두 역할을 인코딩합니다. 인코딩은 모델을 새로 학습하지 않습니다.
    docs=encoder.encode(passages,normalize_embeddings=True,convert_to_numpy=True,batch_size=8)
    queries_vec=encoder.encode(queries,normalize_embeddings=True,convert_to_numpy=True)
    return np.asarray(docs,dtype=np.float32),np.asarray(queries_vec,dtype=np.float32)
# END D23-03-B03


def run(mode,level,args):
    rows=load_knowledge()[:3] if level==1 else load_knowledge()
    encoder=get_encoder(mode)
    passages=make_passages(rows)
    questions=make_queries(['서버는 어디에서 실행하나요?'])
    docs,queries=encode_both(encoder,passages,questions)
    result=dict(exercise=3,level=level,source_mode='e5_live' if mode=='live' else 'simulated',
                model_id=E5_MODEL_ID if mode=='live' else encoder.model_id,
                document_shape=list(docs.shape),query_shape=list(queries.shape),
                example_passage=passages[0],example_query=questions[0])
    if level>=2:
        result['alignment']=verify_alignment(rows,docs)
        result['vectors_valid']=check_shapes_vectors(docs,queries,len(rows))
    if level>=3:result['model_contract']=make_model_stamp(encoder,mode)
    return result


def main():
    parser=argparse.ArgumentParser(description='Day23 실습 03 · E5 문장 Embedding')
    parser.add_argument('--mode',choices=['fixture','live'],default='fixture',
        help='fixture=모의 벡터/오프라인, live=실제 E5/DB가 필요한 단계')
    args=parser.parse_args()
    result=run(args.mode,1,args)
    path=save_result(Path(__file__).resolve().parent,'exercise_03.json',result)
    import json
    print(json.dumps(result,ensure_ascii=False,indent=2,default=str))
    print('결과 저장:',path)

if __name__=='__main__':
    main()
