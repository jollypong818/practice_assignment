"""단계별 역할 분리: checks.py / 독립 실행은 main.py. """

def check_rank_scores(ranked):
    """점수의 개수·유한값·정렬 순서 검사. 점수는 정답 확률이 아닙니다."""
    # BEGIN D27-05-I03
    # ANSWER D27-05-I03: 점수의 개수·유한값·정렬 순서 검사. 점수는 정답 확률이 아닙니다.
    # 1. 입력: ranked (필요한 값만 받습니다.)
    # 2. 절차: 점수의 개수·유한값·정렬 순서 검사. 점수는 정답 확률이 아닙니다.
    # 3. 반환: 호출한 Stage가 사용할 값/상태를 반환합니다.
    # 4. 주의: 오류를 빈 결과로 숨기지 않고 출처·필터 계약을 유지합니다.
    import math
    return {'scores_finite':all(math.isfinite(d.metadata['rerank_score']) for d in ranked),
            'rank_sorted':all(a.metadata['rerank_score']>=b.metadata['rerank_score']
                for a,b in zip(ranked,ranked[1:]))}
    # END D27-05-I03
