# Day23 / 실습 02 / 심화 validation / mentor
import numpy as np


# BEGIN D23-02-A06
def validate_pair(a,b):
    """
    [강사용 정답] D23-02-A06 · validate_pair
        배열 1차원·shape 일치·유한값·영벡터 여부를 검증하세요.
        각각 dimension_mismatch, nonfinite, zero_vector ValueError로 구분합니다.
        양쪽 입력이 올바르면 True.
    """
    # 해설 D23-02-A06: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    # 현업 검색에서 조용히 NaN 점수나 잘못된 차원으로 계산하지 않습니다.
    if a.ndim!=1 or b.ndim!=1 or a.shape!=b.shape:raise ValueError('dimension_mismatch')
    if not np.isfinite(a).all() or not np.isfinite(b).all():raise ValueError('nonfinite')
    if np.linalg.norm(a)<=1e-12 or np.linalg.norm(b)<=1e-12:raise ValueError('zero_vector')
    return True
# END D23-02-A06
