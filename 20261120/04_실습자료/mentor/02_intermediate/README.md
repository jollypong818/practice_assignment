# Report Agent · 02_intermediate Mentor 정답

## 이 정답의 구현 범위

- `01_basic`: B-01~B-15 (API-00~09, 실제 E5·PostgreSQL·LLM 연동 경로)
- `02_intermediate`: B + I-01~09 (Prompt 버전 생성/조회·추가 검색·구조화 요약)
- `03_advanced`: B + I + A-01~09 (Revision·재색인·활성 버전·도구 호출·실행 이력)

현재 폴더는 **intermediate 정답**입니다. `.env.example`을 `.env`로 복사하고 필수 환경 값을 설정하십시오. `PROJECT_LEVEL=intermediate`을 확인합니다.

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

**실행 검증:** 실제 Windows 11 PostgreSQL·pgvector·E5·LLM 연동 통합 검증은 강사 PC에서 완료해야 합니다. 함께 제공한 재검수 기록의 오프라인 검사·테스트 더블 결과를 실제 연동 성공으로 해석하지 않습니다.
