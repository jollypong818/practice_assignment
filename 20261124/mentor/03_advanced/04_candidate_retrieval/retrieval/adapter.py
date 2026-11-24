"""단계별 역할 분리: retrieval/adapter.py / 독립 실행은 main.py. """

def make_candidate_request(case):
    """candidate_k와 context_k는 다른 제한값입니다."""
    # BEGIN D27-04-A01
    # ANSWER D27-04-A01: candidate_k와 context_k는 다른 제한값입니다.
    # 1. 입력: case (필요한 값만 받습니다.)
    # 2. 절차: candidate_k와 context_k는 다른 제한값입니다.
    # 3. 반환: 호출한 Stage가 사용할 값/상태를 반환합니다.
    # 4. 주의: 오류를 빈 결과로 숨기지 않고 출처·필터 계약을 유지합니다.
    return {'query':case['question'],'category':case['category'],
            'candidate_k':5,'context_k':2}
    # END D27-04-A01


def fetch_documents(retriever, payload):
    """Day26에서 배운 Runnable.invoke로 후보 Document를 받아옵니다."""
    # BEGIN D27-04-A02
    # ANSWER D27-04-A02: Day26에서 배운 Runnable.invoke로 후보 Document를 받아옵니다.
    # 1. 입력: retriever, payload (필요한 값만 받습니다.)
    # 2. 절차: Day26에서 배운 Runnable.invoke로 후보 Document를 받아옵니다.
    # 3. 반환: 호출한 Stage가 사용할 값/상태를 반환합니다.
    # 4. 주의: 오류를 빈 결과로 숨기지 않고 출처·필터 계약을 유지합니다.
    docs=retriever.invoke(payload)
    if len(docs)>payload['candidate_k']:raise ValueError('candidate_k 초과')
    return docs
    # END D27-04-A02
