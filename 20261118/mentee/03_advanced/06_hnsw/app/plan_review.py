# Day23 / 실습 06 / 심화 plan_review / mentee



# BEGIN D23-06-A03
def read_scan_type(plan_lines):
    """
    TODO D23-06-A03 · read_scan_type
        PostgreSQL EXPLAIN 텍스트에서 Index Scan / Seq Scan / 기타를 구분하세요.
        계획이 없으면 unknown, index가 있으면 index, seq면 seq로 반환합니다.
        작은 9건 테이블에서 Seq Scan은 오류가 아닙니다.
    """
    # TODO D23-06-A03: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-06-A03: 직접 구현하세요")
# END D23-06-A03

# BEGIN D23-06-A04
def check_operator_compatibility(sql,operator_class):
    """
    TODO D23-06-A04 · check_operator_compatibility
        SQL이 cosine <=> 를 사용하면 vector_cosine_ops가 맞는지 검사하세요.
        불일치 시 ValueError, 정상 시 True.
        L2 / negative inner product와 혼동하지 않습니다.
    """
    # TODO D23-06-A04: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-06-A04: 직접 구현하세요")
# END D23-06-A04

# BEGIN D23-06-A05
def compare_topk(exact_ids,ann_ids):
    """
    TODO D23-06-A05 · compare_topk
        Exact Top-k와 ANN Top-k의 ID 집합 일치율을 계산하세요.
        겹치는 ID 수 / exact_ids 수. 빈 exact_ids는 None.
        인덱스 속도나 모델 품질을 만들어 내면 안 됩니다.
    """
    # TODO D23-06-A05: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-06-A05: 직접 구현하세요")
# END D23-06-A05

# BEGIN D23-06-A06
def filtered_ann_warning(k,returned,exact_count):
    """
    TODO D23-06-A06 · filtered_ann_warning
        ANN + Metadata 필터에서 반환 개수가 부족한지 판정하세요.
        기대 최대 개수=min(k,exact_count). 반환이 부족하면 검토 메시지를 반환하세요.
        이는 성능 측정이 아니라 후보 누락 가능성을 알려주는 진단입니다.
    """
    # TODO D23-06-A06: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-06-A06: 직접 구현하세요")
# END D23-06-A06
