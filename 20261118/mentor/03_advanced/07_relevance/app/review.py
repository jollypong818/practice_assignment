# Day23 / 실습 07 / 심화 review / mentor
from day23kit.data import load_knowledge

from .reference import judge_training_reference

# BEGIN D23-07-A03
def make_review_row(case,hit):
    """
    [강사용 정답] D23-07-A03 · make_review_row
        질문 ID·검색된 ID·본문·거리·교재 기준 라벨을 한 행으로 만드세요.
        distance는 정답 확률로 표현하지 않습니다.
        human_reviewed는 False로 두어 실제 수강생의 근거 검토 전임을 표시합니다.
    """
    # 해설 D23-07-A03: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    return dict(case_id=case['case_id'],query=case['question'],
                retrieved_id=hit['id'],content=hit['content'],
                distance=round(hit['distance'],6),
                teaching_reference=judge_training_reference(case['case_id'],hit['id']),
                human_reviewed=False)
# END D23-07-A03

# BEGIN D23-07-A04
def classify_search_state(rows,error=None):
    """
    [강사용 정답] D23-07-A04 · classify_search_state
        데이터베이스 예외(error)는 error, 정상 조회 결과 []는 empty,
        후보가 있으면 candidates를 반환하세요. 결과 없음과 DB 장애를 섞지 마세요.
    """
    # 해설 D23-07-A04: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    if error is not None:return 'error'
    return 'candidates' if rows else 'empty'
# END D23-07-A04

# BEGIN D23-07-A05
def review_filter_effect(before,after):
    """
    [강사용 정답] D23-07-A05 · review_filter_effect
        필터 전후 ID 목록을 비교해 빠진 ID와 추가된 ID를 반환하세요.
        출력 {'removed': [...], 'added': [...]} 정렬된 목록.
        필터 때문에 k보다 적게 반환될 수 있습니다.
    """
    # 해설 D23-07-A05: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    return {'removed':sorted(set(before)-set(after)),
            'added':sorted(set(after)-set(before))}
# END D23-07-A05

# BEGIN D23-07-A06
def check_evaluation_integrity(rows):
    """
    [강사용 정답] D23-07-A06 · check_evaluation_integrity
        같은 case_id의 retrieved_id가 중복되면 ValueError.
        지식 101~109에 없는 ID나 원문 버전 불일치도 구분하세요.
        정상일 때 true. 주의: 이 검사는 사람의 관련성 평가를 대체하지 않습니다.
    """
    # 해설 D23-07-A06: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    snapshot={r['id']:r for r in load_knowledge()}
    seen=set()
    for row in rows:
        key=(row['case_id'],row['retrieved_id'])
        if key in seen:raise ValueError('duplicate_result')
        seen.add(key)
        if row['retrieved_id'] not in snapshot:raise ValueError('unknown_id')
        if row.get('source_version') != snapshot[row['retrieved_id']]['source_version']:
            raise ValueError('stale_source_version')
    return True
# END D23-07-A06
