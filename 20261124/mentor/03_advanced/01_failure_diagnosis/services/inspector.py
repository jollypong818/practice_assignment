"""단계별 역할 분리: services/inspector.py / 독립 실행은 main.py. """

def reason_for_stage(case, stage):
    """진단할 때 사용한 근거 3개를 기록합니다."""
    # BEGIN D27-01-A03
    # ANSWER D27-01-A03: 진단할 때 사용한 근거 3개를 기록합니다.
    # 1. 입력: case, stage (필요한 값만 받습니다.)
    # 2. 절차: 진단할 때 사용한 근거 3개를 기록합니다.
    # 3. 반환: 호출한 Stage가 사용할 값/상태를 반환합니다.
    # 4. 주의: 오류를 빈 결과로 숨기지 않고 출처·필터 계약을 유지합니다.
    return {'reason':stage,'evidence':{'ambiguous':case['ambiguous'],
              'gold_in_candidates':case['gold_in_candidates'],
              'gold_in_context':case['gold_in_context']}}
    # END D27-01-A03


def audit_case(case, row):
    """권한·버전·준비 상태를 실패 진단 로그에 포함합니다."""
    # BEGIN D27-01-A04
    # ANSWER D27-01-A04: 권한·버전·준비 상태를 실패 진단 로그에 포함합니다.
    # 1. 입력: case, row (필요한 값만 받습니다.)
    # 2. 절차: 권한·버전·준비 상태를 실패 진단 로그에 포함합니다.
    # 3. 반환: 호출한 Stage가 사용할 값/상태를 반환합니다.
    # 4. 주의: 오류를 빈 결과로 숨기지 않고 출처·필터 계약을 유지합니다.
    return {'case_id':case['id'],'policy':{'authorized':case['authorized'],
            'current':case['current'],'ready':case['ready']},'stage':row['stage']}
    # END D27-01-A04
