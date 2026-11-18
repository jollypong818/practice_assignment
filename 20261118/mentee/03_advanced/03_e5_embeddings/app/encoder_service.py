# Day23 / 실습 03 / 심화 encoder_service / mentee
import numpy as np
from day23kit.data import E5_MODEL_ID
from day23kit.embedding import get_model_revision, validate_vectors


# BEGIN D23-03-A03
def encode_both(encoder,passages,queries):
    """
    TODO D23-03-A03 · encode_both
        같은 Encoder에 문서와 질문을 나누어 encode하세요.
        반드시 normalize_embeddings=True, convert_to_numpy=True를 전달합니다.
        결과: (doc_vectors, query_vectors). 기본필수의 모의 모드와
        --mode live의 E5 실측을 구분하여 같은 API를 사용합니다.
    """
    # TODO D23-03-A03: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-03-A03: 직접 구현하세요")
# END D23-03-A03

# BEGIN D23-03-A04
def verify_alignment(rows,vectors):
    """
    TODO D23-03-A04 · verify_alignment
        지식 행 수와 벡터 행 수가 같은지 확인하고 [(ID,행번호),...]를 반환하세요.
        ID가 중복되어 있거나 행 수가 다르면 ValueError.
        예: 지식 102는 vectors[1]과 짝입니다.
    """
    # TODO D23-03-A04: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-03-A04: 직접 구현하세요")
# END D23-03-A04

# BEGIN D23-03-A05
def check_shapes_vectors(docs,queries,doc_count):
    """
    TODO D23-03-A05 · check_shapes_vectors
        문서 벡터 shape=(doc_count,384), 질문 shape=(1,384)를 검사하세요.
        두 배열 모두 유한하고 길이가 1인지 검증합니다.
        정상일 때 True, 오류일 때 ValueError.
    """
    # TODO D23-03-A05: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-03-A05: 직접 구현하세요")
# END D23-03-A05

# BEGIN D23-03-A06
def make_model_stamp(encoder,mode):
    """
    TODO D23-03-A06 · make_model_stamp
        모델 ID·revision·접두어·차원·정규화를 JSON 직렬화 가능한 dict로 기록하세요.
        모의 벡터이면 model_id에 SIMULATED를 분명히 표시합니다.
        실제 revision을 알 수 없으면 'unverified'로 두며 임의 해시를 만들지 않습니다.
    """
    # TODO D23-03-A06: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-03-A06: 직접 구현하세요")
# END D23-03-A06
