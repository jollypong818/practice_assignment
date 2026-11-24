"""단계별 역할 분리: app/services/audit.py / 독립 실행은 main.py. """

def audit_http_response(payload, response):
    """HTTP 오류를 정보 부족 응답으로 숨기지 않고 Stage·모드·상태를 기록합니다."""
    # BEGIN D27-08-A04
    # ANSWER D27-08-A04: HTTP 오류를 정보 부족 응답으로 숨기지 않고 Stage·모드·상태를 기록합니다.
    # 1. 입력: payload, response (필요한 값만 받습니다.)
    # 2. 절차: HTTP 오류를 정보 부족 응답으로 숨기지 않고 Stage·모드·상태를 기록합니다.
    # 3. 반환: 호출한 Stage가 사용할 값/상태를 반환합니다.
    # 4. 주의: 오류를 빈 결과로 숨기지 않고 출처·필터 계약을 유지합니다.
    body=response.json();trace=body.get('trace',{})
    return {'status_code':response.status_code,'query':payload['query'],
            'execution_mode':trace.get('source_mode','error'),
            'stages':list(trace.get('timing_ms',{})),
            'policy_role':'server_learner'}
    # END D27-08-A04
