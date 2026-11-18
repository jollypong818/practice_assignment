# Day23 / 실습 03 / 심화 encoder_service / mentor
import numpy as np
from day23kit.data import E5_MODEL_ID
from day23kit.embedding import get_model_revision, validate_vectors


# BEGIN D23-03-A03
def encode_both(encoder,passages,queries):
    """
    [강사용 정답] D23-03-A03 · encode_both
        같은 Encoder에 문서와 질문을 나누어 encode하세요.
        반드시 normalize_embeddings=True, convert_to_numpy=True를 전달합니다.
        결과: (doc_vectors, query_vectors). 기본필수의 모의 모드와
        --mode live의 E5 실측을 구분하여 같은 API를 사용합니다.
    """
    # 해설 D23-03-A03: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    # 동일 모델로 두 역할을 인코딩합니다. 인코딩은 모델을 새로 학습하지 않습니다.
    docs=encoder.encode(passages,normalize_embeddings=True,convert_to_numpy=True,batch_size=8)
    queries_vec=encoder.encode(queries,normalize_embeddings=True,convert_to_numpy=True)
    return np.asarray(docs,dtype=np.float32),np.asarray(queries_vec,dtype=np.float32)
# END D23-03-A03

# BEGIN D23-03-A04
def verify_alignment(rows,vectors):
    """
    [강사용 정답] D23-03-A04 · verify_alignment
        지식 행 수와 벡터 행 수가 같은지 확인하고 [(ID,행번호),...]를 반환하세요.
        ID가 중복되어 있거나 행 수가 다르면 ValueError.
        예: 지식 102는 vectors[1]과 짝입니다.
    """
    # 해설 D23-03-A04: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    ids=[r['id'] for r in rows]
    if len(ids)!=len(set(ids)) or len(rows)!=len(vectors):raise ValueError('id_vector_alignment')
    return [(r['id'],i) for i,r in enumerate(rows)]
# END D23-03-A04

# BEGIN D23-03-A05
def check_shapes_vectors(docs,queries,doc_count):
    """
    [강사용 정답] D23-03-A05 · check_shapes_vectors
        문서 벡터 shape=(doc_count,384), 질문 shape=(1,384)를 검사하세요.
        두 배열 모두 유한하고 길이가 1인지 검증합니다.
        정상일 때 True, 오류일 때 ValueError.
    """
    # 해설 D23-03-A05: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    # 모의 모드와 실제 E5 모두 같은 차원/정규화 계약을 갖습니다.
    validate_vectors(docs,doc_count)
    validate_vectors(queries,1)
    return True
# END D23-03-A05

# BEGIN D23-03-A06
def make_model_stamp(encoder,mode):
    """
    [강사용 정답] D23-03-A06 · make_model_stamp
        모델 ID·revision·접두어·차원·정규화를 JSON 직렬화 가능한 dict로 기록하세요.
        모의 벡터이면 model_id에 SIMULATED를 분명히 표시합니다.
        실제 revision을 알 수 없으면 'unverified'로 두며 임의 해시를 만들지 않습니다.
    """
    # 해설 D23-03-A06: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    model_id=E5_MODEL_ID if mode=='live' else encoder.model_id
    return {'model_id':model_id,'revision':get_model_revision(encoder),
            'dimension':384,'query_prefix':'query: ',
            'document_prefix':'passage: ', 'normalize_embeddings':True,
            'source_mode':'e5_live' if mode=='live' else 'simulated'}
# END D23-03-A06
