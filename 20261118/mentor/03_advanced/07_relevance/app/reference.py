# Day23 / 실습 07 / 심화 reference / mentor



# BEGIN D23-07-A01
def make_casebook():
    """
    [강사용 정답] D23-07-A01 · make_casebook
        강의의 질문 3종과 확인할 지식 ID를 구성하세요.
        server(102), retention(101: 보관 기간 없음), error(103/108).
        자동 생성한 정답이 아니라 사람이 평가할 고정 기준 샘플임을 표시합니다.
    """
    # 해설 D23-07-A01: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    return [
       {'case_id':'server','question':'서버는 어디에서 실행하나요?','reference_ids':[102]},
       {'case_id':'retention','question':'실습 파일은 몇 년 동안 보관하나요?','reference_ids':[]},
       {'case_id':'error','question':'오류를 질문할 때 무엇을 적어야 하나요?','reference_ids':[103,108]},
    ]
# END D23-07-A01

# BEGIN D23-07-A02
def judge_training_reference(case_id,doc_id):
    """
    [강사용 정답] D23-07-A02 · judge_training_reference
        교안에 미리 주어진 원문 근거로 관련/부분 관련/무관을 수동 기준표로 판정하세요.
        server:102 관련,106 부분 관련. retention:101 부분 관련(기간 없음).
        error:103,108 관련. 그 밖에는 무관.
        *이 표는 사람이 만든 교육용 기준이며 모델 검색 평가점수가 아닙니다.*
    """
    # 해설 D23-07-A02: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    gold={'server':{102:'관련',106:'부분 관련'},
          'retention':{101:'부분 관련'},
          'error':{103:'관련',108:'관련'}}
    if case_id not in gold:raise ValueError('unknown_case')
    return gold[case_id].get(doc_id,'무관')
# END D23-07-A02
