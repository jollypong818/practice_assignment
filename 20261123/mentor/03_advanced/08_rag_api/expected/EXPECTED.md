# 실습 08 · 기대 조건

실제 실행과 Fixture 결과 파일을 구분합니다. 아래 표의 문장은 기대 의미이며 실제 LLM 출력 문자열의 정답지가 아닙니다.

| 요청 | HTTP | 기대 상태·관찰 |
|---|---:|---|
| 15분 출석 질문 | 200 | answered, 현재 출석 문서 출처, 숫자·사전 승인 예외 대조 |
| 정확한 과제 마감 날짜 | 200 | insufficient_context, source_ids와 sources는 빈 목록 |
| candidate_k=0 | 422 | 검색·생성 시도 0회 |
| 별도 Timeout Fixture | 502 | generation_error, 실제 연동 결과와 분리 |

모든 200 응답에서 result.source_ids와 sources[*].citation_id의 순서가 같아야 하고, 반환 출처는 실제 included_ids의 부분집합이어야 합니다. 실제 DB의 ID를 201로 강제하지 않습니다. Fixture의 정상 출석 ID는 201입니다.

최상위 source_mode는 기본 실행 `live_api_smoke`, --offline은 `fixture_api_smoke`입니다. 두 모드 모두 fixed_failure_examples는 항상 고정 예시이며 모델·DB의 실제 실패 기록이 아닙니다. api_transport는 FastAPI TestClient이고 TCP 서버를 시작했다는 뜻이 아닙니다.

실제 답변 표현, Token 수, 지연 시간은 고정하지 않습니다. 본 실습은 원문에 없는 날짜를 추정하지 않는지 사람의 대조도 필요합니다.

`--compare-k` 요청에서는 같은 질문·category·candidate_k를 유지하고 context_k만 1로 바뀝니다. 기준 요청은 context_k=2로 남아야 합니다. 실제 포함 수는 상한 이하이며 답변의 source_ids는 여전히 포함 ID에 한정됩니다.

심화의 empty_context Fixture는 HTTP 200 + insufficient_context이며 generation_attempts=0입니다. Timeout Fixture는 generation_attempts=1, HTTP 502입니다. 생성하지 않은 상태와 생성하려다 실패한 상태를 구분합니다.
