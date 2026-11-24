"""단계별 역할 분리: app/api/routes.py / 독립 실행은 main.py. """

def check_http_response(response):
    """성공 응답의 source_ids와 실제 연결된 sources의 ID가 같은지 검사합니다."""
    # BEGIN D27-08-A03
    # ANSWER D27-08-A03: 성공 응답의 source_ids와 실제 연결된 sources의 ID가 같은지 검사합니다.
    # 1. 입력: response (필요한 값만 받습니다.)
    # 2. 절차: 성공 응답의 source_ids와 실제 연결된 sources의 ID가 같은지 검사합니다.
    # 3. 반환: 호출한 Stage가 사용할 값/상태를 반환합니다.
    # 4. 주의: 오류를 빈 결과로 숨기지 않고 출처·필터 계약을 유지합니다.
    body=response.json()
    if response.status_code!=200:return {'http_ok':False,'error_detail':body.get('detail')}
    ids=[src['citation_id'] for src in body['sources']]
    return {'http_ok':True,'citation_consistent':ids==body['result']['source_ids']}
    # END D27-08-A03
