# Day27 HTML ↔ 실제 실습 1:1 대응

| HTML | 수업 | 기본 입력 | 실행 Stage / 파일 | 확인할 출력 |
|---|---|---|---|---|
| 15p | 01 실패 진단 | 고정 실패 사례 7개 | `coursekit.workshops.run_01` + 현재 TODO | 오류 위치/조치 기록 |
| 25p | 02 Query Rewrite | `query`, `history` | `coursekit.rewrite` + 현재 TODO | original·search_query·clarification |
| 34p | 03 Multi-query | 검색 질문 2~3개 | `coursekit.multi_query` + 현재 TODO | found_by_query·unique chunk_id |
| 42p | 04 Candidate Retrieval | candidate_k·category | `coursekit.live/db` + 현재 TODO | Document/Metadata/Top-k |
| 54p | 05 Reranking | 질문+문서 후보 | `coursekit.reranking` + 현재 TODO | before/after·score·source |
| 64p | 06 LangChain Pipeline | state dict | `coursekit.pipeline` + 현재 TODO | 단계별 trace·Context IDs |
| 73p | 07 Before/After | 같은 질문·Gold Labels | `coursekit.evaluation` + 현재 TODO | Top-k 포함 여부·실행 시간 |
| 81p | 08 FastAPI | HTTP JSON | `coursekit.api/pipeline` + 현재 TODO | 정상/정보 부족/오류와 sources |

**학습 포인트:** 폴더·파일은 책임별 코드 구성이고, Runnable 노드는 실행 단위입니다. 폴더 하나가 반드시 실행 노드 하나를 뜻하지 않습니다.

`01_basic`: 실습당 main.py 중심. `02_intermediate`: steps.py/checks.py 분리. `03_advanced`: 해당 문제에 필요한 서비스·검증·정책·API 모듈을 목적별로 분리합니다. 전날 Day26 파일을 별도 설치하지 않아도 됩니다.
