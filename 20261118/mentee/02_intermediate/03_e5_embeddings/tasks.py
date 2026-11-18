# Day23 / 실습 03 / 응용 / mentee
import numpy as np
from day23kit.data import passage_text
from day23kit.embedding import validate_vectors

# BEGIN D23-03-I01
def make_passages(rows):
    """
    TODO D23-03-I01 · make_passages
        지식 목록을 E5 문서 입력 문자열 목록으로 변환하세요.
        문서에는 'passage: ' + 제목 + ' ' + 본문을 사용합니다.
        한 행마다 정확히 한 문자열을 만들어 순서를 유지하세요.
    """
    # TODO D23-03-I01: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-03-I01: 직접 구현하세요")
# END D23-03-I01

# BEGIN D23-03-I02
def make_queries(questions):
    """
    TODO D23-03-I02 · make_queries
        질문 목록 각 요소 앞에 query: 공백을 붙이세요.
        출력: 입력과 동일한 순서의 문자열 리스트.
        빈 질문을 추가해 그럴듯한 벡터를 만들지 마세요.
    """
    # TODO D23-03-I02: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-03-I02: 직접 구현하세요")
# END D23-03-I02

# BEGIN D23-03-I03
def encode_both(encoder,passages,queries):
    """
    TODO D23-03-I03 · encode_both
        같은 Encoder에 문서와 질문을 나누어 encode하세요.
        반드시 normalize_embeddings=True, convert_to_numpy=True를 전달합니다.
        결과: (doc_vectors, query_vectors). 기본필수의 모의 모드와
        --mode live의 E5 실측을 구분하여 같은 API를 사용합니다.
    """
    # TODO D23-03-I03: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-03-I03: 직접 구현하세요")
# END D23-03-I03

# BEGIN D23-03-I04
def verify_alignment(rows,vectors):
    """
    TODO D23-03-I04 · verify_alignment
        지식 행 수와 벡터 행 수가 같은지 확인하고 [(ID,행번호),...]를 반환하세요.
        ID가 중복되어 있거나 행 수가 다르면 ValueError.
        예: 지식 102는 vectors[1]과 짝입니다.
    """
    # TODO D23-03-I04: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-03-I04: 직접 구현하세요")
# END D23-03-I04

# BEGIN D23-03-I05
def check_shapes_vectors(docs,queries,doc_count):
    """
    TODO D23-03-I05 · check_shapes_vectors
        문서 벡터 shape=(doc_count,384), 질문 shape=(1,384)를 검사하세요.
        두 배열 모두 유한하고 길이가 1인지 검증합니다.
        정상일 때 True, 오류일 때 ValueError.
    """
    # TODO D23-03-I05: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-03-I05: 직접 구현하세요")
# END D23-03-I05
