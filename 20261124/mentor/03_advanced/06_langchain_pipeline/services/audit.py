"""단계별 역할 분리: services/audit.py / 독립 실행은 main.py. """

def audit_pipeline(result):
    """Stage 시간과 출처 연결을 기록하되 진위 판단은 별도로 수행합니다."""
    # BEGIN D27-06-A04
    # ANSWER D27-06-A04: Stage 시간과 출처 연결을 기록하되 진위 판단은 별도로 수행합니다.
    # 1. 입력: result (필요한 값만 받습니다.)
    # 2. 절차: Stage 시간과 출처 연결을 기록하되 진위 판단은 별도로 수행합니다.
    # 3. 반환: 호출한 Stage가 사용할 값/상태를 반환합니다.
    # 4. 주의: 오류를 빈 결과로 숨기지 않고 출처·필터 계약을 유지합니다.
    t=result['trace'];return {'mode':t['source_mode'],'stage_times':sorted(t['timing_ms']),
            'output_source_ids':[r['citation_id'] for r in result['sources']],
            'manual_grounding_review':True}
    # END D27-06-A04
