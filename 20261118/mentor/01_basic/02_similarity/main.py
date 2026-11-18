"""Day23 실습 02 · Vector·Similarity·Distance (기본필수, mentor).

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
from day23kit.mathops import cosine_distance
from day23kit.io import save_result


# BEGIN D23-02-B01
def dot(a,b):
    """
    [강사용 정답] D23-02-B01 · dot
        같은 위치의 숫자를 곱해 합산하는 내적을 구현하세요.
        예: (1,0)·(0.8,0.6)=0.8. 입력 NumPy 배열 2개, 출력 float.
    """
    # 해설 D23-02-B01: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    # 좌표별 곱을 모두 합산. 내적은 벡터 크기에도 영향을 받습니다.
    return float(np.dot(a,b))
# END D23-02-B01

# BEGIN D23-02-B02
def cosine(a,b):
    """
    [강사용 정답] D23-02-B02 · cosine
        내적을 두 벡터 길이의 곱으로 나누어 Cosine similarity를 구하세요.
        q=(1,0), A=(0.8,0.6)라면 0.8입니다.
        입력: NumPy 배열 2개. 출력: float. 영벡터는 무조건 거부합니다.
    """
    # 해설 D23-02-B02: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    # ① 길이 ② 분모 확인 ③ 정규화한 내적.
    na=float(np.linalg.norm(a));nb=float(np.linalg.norm(b))
    if na<=1e-12 or nb<=1e-12:raise ValueError('zero_vector')
    return dot(a,b)/(na*nb)
# END D23-02-B02

# BEGIN D23-02-B03
def l2(a,b):
    """
    [강사용 정답] D23-02-B03 · l2
        두 벡터의 좌표 차이로 L2 거리를 구하세요. 출력 float.
        q=(1,0), A=(0.8,0.6) → sqrt(0.4) ≈ 0.6325.
    """
    # 해설 D23-02-B03: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    # 좌표 간 차이의 길이: 값이 작을수록 가깝습니다.
    return float(np.linalg.norm(a-b))
# END D23-02-B03


def run(mode,level,args):
    q=np.array([1.,0.]);a=np.array([.8,.6]);u=np.array([1.,0.]);v=np.array([10.,10.])
    result=dict(exercise=2,level=level,source_mode='local_math',
                dot=round(dot(q,a),6),cosine=round(cosine(q,a),6),l2=round(l2(q,a),6),
                cosine_distance=round(1-cosine(q,a),6))
    if level>=2:
        result['normalized_v']=normalize(v).round(6).tolist()
        result['rankings']=rank_dot_vs_cosine(q,{'U':u,'V':v})
    if level>=3:
        result['validated']=validate_pair(q,a)
        errors={}
        for label,x,y in [('dimension_mismatch',q,np.array([1.,0.,2.])),
                           ('nonfinite',q,np.array([np.nan,1.])),
                           ('zero_vector',q,np.array([0.,0.]))]:
            try:validate_pair(x,y)
            except ValueError as e:errors[label]=str(e)
        result['invalid_inputs']=errors
    return result


def main():
    parser=argparse.ArgumentParser(description='Day23 실습 02 · Vector·Similarity·Distance')
    parser.add_argument('--mode',choices=['fixture','live'],default='fixture',
        help='fixture=모의 벡터/오프라인, live=실제 E5/DB가 필요한 단계')
    args=parser.parse_args()
    result=run(args.mode,1,args)
    path=save_result(Path(__file__).resolve().parent,'exercise_02.json',result)
    import json
    print(json.dumps(result,ensure_ascii=False,indent=2,default=str))
    print('결과 저장:',path)

if __name__=='__main__':
    main()
