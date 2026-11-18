# Day23 / 실습 02 / 응용 / mentor
import numpy as np

# BEGIN D23-02-I01
def dot(a,b):
    """
    [강사용 정답] D23-02-I01 · dot
        같은 위치의 숫자를 곱해 합산하는 내적을 구현하세요.
        예: (1,0)·(0.8,0.6)=0.8. 입력 NumPy 배열 2개, 출력 float.
    """
    # 해설 D23-02-I01: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    # 좌표별 곱을 모두 합산. 내적은 벡터 크기에도 영향을 받습니다.
    return float(np.dot(a,b))
# END D23-02-I01

# BEGIN D23-02-I02
def cosine(a,b):
    """
    [강사용 정답] D23-02-I02 · cosine
        내적을 두 벡터 길이의 곱으로 나누어 Cosine similarity를 구하세요.
        q=(1,0), A=(0.8,0.6)라면 0.8입니다.
        입력: NumPy 배열 2개. 출력: float. 영벡터는 무조건 거부합니다.
    """
    # 해설 D23-02-I02: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    # ① 길이 ② 분모 확인 ③ 정규화한 내적.
    na=float(np.linalg.norm(a));nb=float(np.linalg.norm(b))
    if na<=1e-12 or nb<=1e-12:raise ValueError('zero_vector')
    return dot(a,b)/(na*nb)
# END D23-02-I02

# BEGIN D23-02-I03
def l2(a,b):
    """
    [강사용 정답] D23-02-I03 · l2
        두 벡터의 좌표 차이로 L2 거리를 구하세요. 출력 float.
        q=(1,0), A=(0.8,0.6) → sqrt(0.4) ≈ 0.6325.
    """
    # 해설 D23-02-I03: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    # 좌표 간 차이의 길이: 값이 작을수록 가깝습니다.
    return float(np.linalg.norm(a-b))
# END D23-02-I03

# BEGIN D23-02-I04
def normalize(a):
    """
    [강사용 정답] D23-02-I04 · normalize
        임의 벡터 a를 길이가 1인 단위 벡터로 변환하세요.
        기존 배열을 직접 변경하지 않습니다. 영벡터는 ValueError.
    """
    # 해설 D23-02-I04: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    n=float(np.linalg.norm(a))
    if n<=1e-12:raise ValueError('zero_vector')
    return a/n
# END D23-02-I04

# BEGIN D23-02-I05
def rank_dot_vs_cosine(q,candidates):
    """
    [강사용 정답] D23-02-I05 · rank_dot_vs_cosine
        후보 {이름:벡터}를 Dot 내림차순과 Cosine 내림차순으로 각각 정렬하세요.
        결과: {'dot':[이름...], 'cosine':[이름...]}.
        크기가 큰 벡터가 Dot 순위를 바꿀 수 있음을 확인합니다.
    """
    # 해설 D23-02-I05: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    # 동점이면 이름 오름차순으로 정렬하여 결과를 재현 가능하게 만듭니다.
    d=sorted(candidates,key=lambda n:(-dot(q,candidates[n]),n))
    c=sorted(candidates,key=lambda n:(-cosine(q,candidates[n]),n))
    return {'dot':d,'cosine':c}
# END D23-02-I05
