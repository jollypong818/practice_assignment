"""단계별 역할 분리: policies/diagnosis.py / 독립 실행은 main.py. """

def diagnose_stage(case):
    """어떤 문제가 먼저 발생했는지 위에서부터 조건을 검사합니다."""
    # BEGIN D27-01-A01
    # ANSWER D27-01-A01: 어떤 문제가 먼저 발생했는지 위에서부터 조건을 검사합니다.
    # 1. 입력: case (필요한 값만 받습니다.)
    # 2. 절차: 어떤 문제가 먼저 발생했는지 위에서부터 조건을 검사합니다.
    # 3. 반환: 호출한 Stage가 사용할 값/상태를 반환합니다.
    # 4. 주의: 오류를 빈 결과로 숨기지 않고 출처·필터 계약을 유지합니다.
    if not case['authorized']:return 'authorization_filter'
    if not case['current']:return 'version_filter'
    if not case['ready']:return 'index_not_ready'
    if case['ambiguous']:return 'rewrite'
    if not case['gold_in_candidates']:return 'retrieval'
    if not case['gold_in_context']:return 'reranking'
    if case['valid_source'] is False:return 'validation'
    return 'healthy' 
    # END D27-01-A01


def recommend_action(stage):
    """문제 단계에 맞는 개선 방법을 반환합니다. Reranker는 누락된 후보를 새로 찾지 않습니다."""
    # BEGIN D27-01-A02
    # ANSWER D27-01-A02: 문제 단계에 맞는 개선 방법을 반환합니다. Reranker는 누락된 후보를 새로 찾지 않습니다.
    # 1. 입력: stage (필요한 값만 받습니다.)
    # 2. 절차: 문제 단계에 맞는 개선 방법을 반환합니다. Reranker는 누락된 후보를 새로 찾지 않습니다.
    # 3. 반환: 호출한 Stage가 사용할 값/상태를 반환합니다.
    # 4. 주의: 오류를 빈 결과로 숨기지 않고 출처·필터 계약을 유지합니다.
    return {'authorization_filter':'서버에서 접근 권한을 검사합니다.',
            'version_filter':'현재 유효한 문서만 검색합니다.',
            'index_not_ready':'Indexing 공개 상태를 확인합니다.',
            'rewrite':'History에서 명확한 대상만 복원합니다.',
            'retrieval':'검색 대상·필터·Top-k를 점검합니다.',
            'reranking':'후보 문서의 관련성 순위를 다시 평가합니다.',
            'validation':'답변과 실제 근거를 대조합니다.',
            'healthy':'정상 흐름을 유지합니다.'}[stage]
    # END D27-01-A02
