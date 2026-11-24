# Stage별 자료형 · 실무 연계

1. 사용자 질문 입력(`query`, `history`, `category`, `candidate_k`, `context_k`)
2. `RewriteResult`: `status`, `search_query`, `reason` (`clarification_required`이면 검색 중단)
3. `queries: list[str]`: 처음 질문 보존. Multi-query가 켜진 경우 추가 검색 요청은 최대 2건
4. `Document`: `page_content`(본문) + `metadata`(chunk_id/doc_id/citation_id/source_locator/version/category/권한)
5. `ranked: list[Document]`: 원래 ID 보존, `pre_rank`/`post_rank`/`rerank_score` 추가
6. `context: str`·`included`: 실제 LLM에 넣은 근거와 출처
7. Structured Output: `status`, `answer`, `source_ids`, `missing_information`
8. FastAPI Response: `result`, `sources`, `trace`, `status`

**보안:** HTTP Body에서 직접 권한을 결정하지 않습니다. `trusted_role`은 서버측 고정 역할(교육용)이며 실제 서비스에서는 인증·인가 계층에서 주입해야 합니다.

**주의:** Retriever가 찾지 못한 청크는 Reranker가 복구하지 않습니다. 점수는 정답 확률이 아니며, 자동 출처 ID 검사는 Grounding이 아닙니다. 고정 Fixture와 실제 LLM/DB/모델 성능은 다릅니다.
