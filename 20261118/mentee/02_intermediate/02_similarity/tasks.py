# Day23 / 실습 02 / 응용 / mentee
import numpy as np

# BEGIN D23-02-I01
def dot(a,b):
    """
    TODO D23-02-I01 · dot
        같은 위치의 숫자를 곱해 합산하는 내적을 구현하세요.
        예: (1,0)·(0.8,0.6)=0.8. 입력 NumPy 배열 2개, 출력 float.
    """
    # TODO D23-02-I01: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-02-I01: 직접 구현하세요")
# END D23-02-I01

# BEGIN D23-02-I02
def cosine(a,b):
    """
    TODO D23-02-I02 · cosine
        내적을 두 벡터 길이의 곱으로 나누어 Cosine similarity를 구하세요.
        q=(1,0), A=(0.8,0.6)라면 0.8입니다.
        입력: NumPy 배열 2개. 출력: float. 영벡터는 무조건 거부합니다.
    """
    # TODO D23-02-I02: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-02-I02: 직접 구현하세요")
# END D23-02-I02

# BEGIN D23-02-I03
def l2(a,b):
    """
    TODO D23-02-I03 · l2
        두 벡터의 좌표 차이로 L2 거리를 구하세요. 출력 float.
        q=(1,0), A=(0.8,0.6) → sqrt(0.4) ≈ 0.6325.
    """
    # TODO D23-02-I03: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-02-I03: 직접 구현하세요")
# END D23-02-I03

# BEGIN D23-02-I04
def normalize(a):
    """
    TODO D23-02-I04 · normalize
        임의 벡터 a를 길이가 1인 단위 벡터로 변환하세요.
        기존 배열을 직접 변경하지 않습니다. 영벡터는 ValueError.
    """
    # TODO D23-02-I04: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-02-I04: 직접 구현하세요")
# END D23-02-I04

# BEGIN D23-02-I05
def rank_dot_vs_cosine(q,candidates):
    """
    TODO D23-02-I05 · rank_dot_vs_cosine
        후보 {이름:벡터}를 Dot 내림차순과 Cosine 내림차순으로 각각 정렬하세요.
        결과: {'dot':[이름...], 'cosine':[이름...]}.
        크기가 큰 벡터가 Dot 순위를 바꿀 수 있음을 확인합니다.
    """
    # TODO D23-02-I05: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-02-I05: 직접 구현하세요")
# END D23-02-I05
