# Day23 / 실습 07 / 응용 / mentor


# BEGIN D23-07-I01
def make_casebook():
    """
    [강사용 정답] D23-07-I01 · make_casebook
        강의의 질문 3종과 확인할 지식 ID를 구성하세요.
        server(102), retention(101: 보관 기간 없음), error(103/108).
        자동 생성한 정답이 아니라 사람이 평가할 고정 기준 샘플임을 표시합니다.
    """
    # 해설 D23-07-I01: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    return [
       {'case_id':'server','question':'서버는 어디에서 실행하나요?','reference_ids':[102]},
       {'case_id':'retention','question':'실습 파일은 몇 년 동안 보관하나요?','reference_ids':[]},
       {'case_id':'error','question':'오류를 질문할 때 무엇을 적어야 하나요?','reference_ids':[103,108]},
    ]
# END D23-07-I01

# BEGIN D23-07-I02
def judge_training_reference(case_id,doc_id):
    """
    [강사용 정답] D23-07-I02 · judge_training_reference
        교안에 미리 주어진 원문 근거로 관련/부분 관련/무관을 수동 기준표로 판정하세요.
        server:102 관련,106 부분 관련. retention:101 부분 관련(기간 없음).
        error:103,108 관련. 그 밖에는 무관.
        *이 표는 사람이 만든 교육용 기준이며 모델 검색 평가점수가 아닙니다.*
    """
    # 해설 D23-07-I02: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    gold={'server':{102:'관련',106:'부분 관련'},
          'retention':{101:'부분 관련'},
          'error':{103:'관련',108:'관련'}}
    if case_id not in gold:raise ValueError('unknown_case')
    return gold[case_id].get(doc_id,'무관')
# END D23-07-I02

# BEGIN D23-07-I03
def make_review_row(case,hit):
    """
    [강사용 정답] D23-07-I03 · make_review_row
        질문 ID·검색된 ID·본문·거리·교재 기준 라벨을 한 행으로 만드세요.
        distance는 정답 확률로 표현하지 않습니다.
        human_reviewed는 False로 두어 실제 수강생의 근거 검토 전임을 표시합니다.
    """
    # 해설 D23-07-I03: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    return dict(case_id=case['case_id'],query=case['question'],
                retrieved_id=hit['id'],content=hit['content'],
                distance=round(hit['distance'],6),
                teaching_reference=judge_training_reference(case['case_id'],hit['id']),
                human_reviewed=False)
# END D23-07-I03

# BEGIN D23-07-I04
def classify_search_state(rows,error=None):
    """
    [강사용 정답] D23-07-I04 · classify_search_state
        데이터베이스 예외(error)는 error, 정상 조회 결과 []는 empty,
        후보가 있으면 candidates를 반환하세요. 결과 없음과 DB 장애를 섞지 마세요.
    """
    # 해설 D23-07-I04: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    if error is not None:return 'error'
    return 'candidates' if rows else 'empty'
# END D23-07-I04

# BEGIN D23-07-I05
def review_filter_effect(before,after):
    """
    [강사용 정답] D23-07-I05 · review_filter_effect
        필터 전후 ID 목록을 비교해 빠진 ID와 추가된 ID를 반환하세요.
        출력 {'removed': [...], 'added': [...]} 정렬된 목록.
        필터 때문에 k보다 적게 반환될 수 있습니다.
    """
    # 해설 D23-07-I05: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    return {'removed':sorted(set(before)-set(after)),
            'added':sorted(set(after)-set(before))}
# END D23-07-I05
