# Report Agent · 03_advanced Mentor 정답

## 이 정답의 구현 범위

- `01_basic`: B-01~B-15 (API-00~09, 실제 E5·PostgreSQL·LLM 연동 경로)
- `02_intermediate`: B + I-01~09 (Prompt 버전 생성/조회·추가 검색·구조화 요약)
- `03_advanced`: B + I + A-01~09 (Revision·재색인·활성 버전·도구 호출·실행 이력)

현재 폴더는 **advanced 정답**입니다. `.env.example`을 `.env`로 복사하고 필수 환경 값을 설정하십시오. `PROJECT_LEVEL=advanced`을 확인합니다.

```bash
python -c "from app.core.config import settings; print(settings.project_level)"
```

`python scripts/index_overviews.py`는 **가짜 벡터가 아닌 실제 E5**를 사용합니다.
`python -m app.main`으로 서버를 실행한 뒤 Postman으로 검증합니다.

### 기능별 코드 해설

- `app/models/report.py`: ERD 10개 테이블을 매핑합니다. 상세 6종의 공통 필드는 `DetailMixin`을 사용하나 실제 DB에는 각각 존재합니다.
- `app/db/session.py`: `Session`의 생성과 종료. **Commit은 Service의 Transaction 범위**에서 확정합니다.
- `app/repositories/report_repository.py`: 조회 SQL 및 API 응답으로 변환. HTTP 로직 없음.
- `app/services/report_service.py`: Create/Update/Delete를 **단일 Transaction**으로 묶고 비싼 E5 계산은 시작 전에 수행합니다.
- `app/services/search_service.py`: Keyword 일치 점수(제목 3 + 개요 2 + 본문 1)와 Semantic 점수를 구분합니다. 선정 근거를 응답에 남기며 `not_found`는 HTTP 200입니다.
- `app/integrations/embedding_client.py`: `query: ` / `passage: ` Prefix; normalize_embeddings=True.
- `app/integrations/llm_client.py`: Responses API 실제 호출, 키/타임아웃 실패를 성공으로 위장하지 않습니다.
- `app/services/agent_service.py`: Basic에서는 **명시적 Action Router**이고, Advanced에서만 제한된 Tool Calling으로 확장합니다.

### 심화 동작을 해석하는 기준

- LLM의 Timeout·429·일시적 서버 오류 재시도 한도는 **각 LLM 호출당 최초 1회 + 재시도 2회, 최대 3회**입니다. Tool Calling의 **도구 결정 단계와 실제 도구 실행 횟수는 각각 최대 3회**로 별도 제한합니다. `LLM_MAX_OUTPUT_TOKENS`는 **호출별 출력 토큰 상한**이며 전체 금액 예산을 자동 관리하는 기능은 아닙니다.
- 일반 요약의 `usage_scope=last_completed_response`는 마지막 완료 응답의 사용량입니다. Tool Calling의 `completed_responses_only`는 완료 응답과 완료된 내부 요약 호출을 합산합니다. 사용량을 확인할 수 없는 실패 요청의 과금은 포함하지 않으므로 실제 청구액으로 해석하지 않습니다.
- `python scripts/evaluate_search.py`는 현재 모델 조건으로 JSON·CSV 평가 결과를 만듭니다. 잘못된 ID를 선택하면 오탐(FP)과 정답 누락(FN)에 모두 기록합니다. 두 수치는 서로 배타적인 건수 합계가 아닙니다.

**실행 검증:** 실제 Windows 11 PostgreSQL·pgvector·E5·LLM 연동 통합 검증은 강사 PC에서 완료해야 합니다. 함께 제공한 재검수 기록의 오프라인 검사·테스트 더블 결과를 실제 연동 성공으로 해석하지 않습니다.
