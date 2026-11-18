from __future__ import annotations
import numpy as np

def vector2(values):
    arr = np.asarray(values, dtype=np.float64)
    if arr.shape != (2,) or not np.isfinite(arr).all():
        raise ValueError("유효한 2차원 수치 벡터가 필요합니다")
    if np.linalg.norm(arr) < 1e-12:
        raise ValueError("코사인 계산에 영벡터를 사용할 수 없습니다")
    return arr

def cosine_distance(a, b):
    a = vector2(a);b=vector2(b)
    return float(1.0 - (a @ b) / (np.linalg.norm(a) * np.linalg.norm(b)))
