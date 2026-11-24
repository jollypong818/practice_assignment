"""단계별 역할 분리: services/audit.py / 독립 실행은 main.py. """

def audit_ranking(before, ranked):
    """Reranking으로 새 문서를 창작하지 않으며 출처와 이전 순위를 유지합니다."""
    # BEGIN D27-05-A04
    # ANSWER D27-05-A04: Reranking으로 새 문서를 창작하지 않으며 출처와 이전 순위를 유지합니다.
    # 1. 입력: before, ranked (필요한 값만 받습니다.)
    # 2. 절차: Reranking으로 새 문서를 창작하지 않으며 출처와 이전 순위를 유지합니다.
    # 3. 반환: 호출한 Stage가 사용할 값/상태를 반환합니다.
    # 4. 주의: 오류를 빈 결과로 숨기지 않고 출처·필터 계약을 유지합니다.
    before_ids={d.metadata['chunk_id'] for d in before}
    return {'same_candidate_pool':all(d.metadata['chunk_id'] in before_ids for d in ranked),
            'metadata_kept':all('source_locator' in d.metadata and
                               'citation_id' in d.metadata for d in ranked),
            'pre_rank_recorded':all('pre_rank' in d.metadata for d in ranked)}
    # END D27-05-A04
