"""단계별 역할 분리: schemas/request.py / 독립 실행은 main.py. """

def prepare_pipeline_request(case):
    """원 질문과 History를 함께 보존하고 검색용 질문은 Chain 내부에서 만듭니다."""
    # BEGIN D27-06-A01
    # ANSWER D27-06-A01: 원 질문과 History를 함께 보존하고 검색용 질문은 Chain 내부에서 만듭니다.
    # 1. 입력: case (필요한 값만 받습니다.)
    # 2. 절차: 원 질문과 History를 함께 보존하고 검색용 질문은 Chain 내부에서 만듭니다.
    # 3. 반환: 호출한 Stage가 사용할 값/상태를 반환합니다.
    # 4. 주의: 오류를 빈 결과로 숨기지 않고 출처·필터 계약을 유지합니다.
    return {'query':case['question'],'history':case['history'],
            'category':case['category'],'candidate_k':5,'context_k':2,
            'use_rewrite':True,'use_multiquery':False,'use_rerank':True}
    # END D27-06-A01
