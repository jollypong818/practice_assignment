"""단계별 역할 분리: checks.py / 독립 실행은 main.py. """

def check_conditions(case, before, ranked):
    """Gold Label은 검색과 Reranker의 입력이 아니라 평가할 때만 사용합니다."""
    # BEGIN D27-07-I03
    # ANSWER D27-07-I03: Gold Label은 검색과 Reranker의 입력이 아니라 평가할 때만 사용합니다.
    # 1. 입력: case, before, ranked (필요한 값만 받습니다.)
    # 2. 절차: Gold Label은 검색과 Reranker의 입력이 아니라 평가할 때만 사용합니다.
    # 3. 반환: 호출한 Stage가 사용할 값/상태를 반환합니다.
    # 4. 주의: 오류를 빈 결과로 숨기지 않고 출처·필터 계약을 유지합니다.
    return {'question_id':case['id'],'category':case['category'],
            'gold_separate':all('gold' not in d.metadata for d in before),
            'same_candidates':set(d.metadata['chunk_id'] for d in ranked).issubset(
                set(d.metadata['chunk_id'] for d in before))}
    # END D27-07-I03
