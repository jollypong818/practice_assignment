# 2026-11-20 Report Agent · 01_basic mentee

**목적:** SRS v1.4를 보고 완성하는 최소 Skeleton 프로젝트. **동일 난이도의 mentor/01_basic과 같은 Router, 함수 시그니처, 데이터 모델을 가진 미완성본입니다. CRUD 구현은 포함하지 않습니다.**

## 시작

1. 공통 제공 `common/sql/schema.sql`→`common/sql/seed.sql`을 **PostgreSQL 18.6** DB에서 실행하세요.
2. 공통 `requirements.txt`, `.env.example`, `sql` 폴더를 이 프로젝트에 복사하세요.
3. 기존 Python `.venv`를 활성화하고 `pip install -r requirements.txt` 실행. `.env.example`을 `.env`로 복사해 DB 정보/LLM 설정을 입력하고 `PROJECT_LEVEL=basic`을 확인합니다.
4. `TODO B-*`가 붙은 함수의 본문을 구현하세요. `app/main.py`의 `main()`과 Router의 경로/시그니처, ORM·Pydantic 구조, DB 연결은 제공됩니다. 기능 로직(CRUD/검색/LLM)은 미완성입니다. 같은 파일 경로의 `mentor/01_basic`은 이 TODO가 완료된 정답이며, Basic API-00~09만 구현 대상입니다.
5. 아래 체크포인트 순서대로 구현합니다. 등록 전에 E5 어댑터를 완성하고, CRUD 다음에 `python scripts/index_overviews.py`로 초기 Overview 180건을 실제 E5로 일괄 색인합니다.
6. 1단계부터 `python -m app.main`으로 서버를 실행해 확인하고 코드 변경 후 재시작합니다. Postman JSON을 Import해 Basic API-00~09를 단계별로 검증합니다. 유료 요청은 마지막에 선택 실행합니다.

## 실습 순서: B-01~B-15

**DB·Seed → 제공 ORM·Session → E5 어댑터 → CRUD → 일괄 색인 → Hybrid → LLM·Agent → Postman**.

B-05 등록은 B-10의 `encode()`·`encode_overview()`를 사용합니다. 두 함수를 먼저 완성하고, 초기 개요 180건의 일괄 색인은 검색 전에 실행합니다.

- `app/models`: ERD→ORM (title/content/author는 상세 테이블 6종에 실제 컬럼)
- `app/repositories`: SQL 조회 / `app/services`: Transaction·업무 규칙
- `app/api`: HTTP Method·JSON Contract·Status / `app/integrations`: E5·LLM
- **지금 `NotImplementedError`는 정상입니다.** TODO 구현 후 해당 줄을 제거합니다.

## 오후 구현 체크포인트

각 행을 완료한 뒤 오른쪽 증거를 확인하고 다음 단계로 갑니다. `api/`의 함수는 해당 `services/` 함수를 호출하는 얇은 연결부입니다. 시드 데이터가 있으므로 등록 구현 전에도 조회부터 확인할 수 있습니다.

| 순서 | 구현할 함수 묶음 | 확인할 증거 |
| --- | --- | --- |
| 1. 환경·조회 | 제공 `models/report.py`, `db/session.py` 확인. Repository의 `get_report_and_detail/plain_value/serialize_report/read_report/list_reports`, Service의 `categories/get_report/list_reports`, 대응 Router | `/health`, 카테고리 6개, 시드 ID 조회 200/없는 ID 404, 제목 목록 |
| 2. E5·첫 등록 | `embedding_client.encode`, `report_service.encode_overview/validate_details/create_report`, Repository의 `category_for_code`, 생성 Router | 실험 보고서 POST 201 → GET의 title/content/author/overview/details 일치 → 상세·벡터 각 1행 |
| 3. 수정·삭제 | `report_service.update_report/delete_report`, 대응 Router | PUT → GET 변경값·revision·벡터 확인. DELETE 204 → GET 404 |
| 4. 일괄 색인·검색 | `scripts/index_overviews.index_overviews`, `search_service.find_similar`, 검색 Router | 초기 개요 색인·ready·최신 revision, 관련 후보 또는 not_found, 아래 평가셋 기록 |
| 5. 요약·Agent | `llm_client.call_llm/summarize`, `report_service.summarize_report`, `agent_service.run_agent`, 대응 Router | 실제 요약/실패 응답 구분, 명시적 action, 검색 ID와 요약 출처 일치 |

모든 TODO의 최종 목표는 B-15까지입니다. 시간이 부족하면 완료한 체크포인트와 남은 요구사항 ID를 README에 기록합니다. 상위 단계는 기본 흐름을 완성한 뒤 선택합니다.

## 검색 의미 확인과 마지막 연결 시연

Postman의 형식 검사가 통과해도 관련 보고서를 골랐는지는 따로 확인합니다. Basic은 다음 수동 확인으로 충분합니다.

1. 공통 폴더의 `common/data/search_cases.json`을 열고 5개 `query`를 API-07에 차례로 보냅니다. `expected_category_codes`와 `expected_keyword`는 후보를 확인하는 참고 기준입니다.
2. `found`이면 `best_match.report_id`를 API-03으로 조회해 제목·개요·본문이 질문과 관련되는지 확인합니다. 예시 ID 1이나 12를 고정 정답으로 삼지 않습니다.
3. 무관 질문은 `not_found`가 되는지 확인합니다. `found`이면 반환 원문과 similarity·`SEARCH_MIN_SIMILARITY`를 보고 오탐 여부와 보정 이유를 기록합니다. 실제 Cosine 값을 예시 숫자에 맞추지 않습니다.
4. 다음 표를 README 또는 제출 기록에 남깁니다. 반환 점수가 없으면 빈칸으로 두고 응답 상태와 후보를 적습니다.

| query | found/not_found | 반환 report_id·분류 | similarity·threshold | 관련/무관 판단 및 근거 |
| --- | --- | --- | --- | --- |
| 실행한 질문 | 실제 응답 | 실제 후보 또는 없음 | 실제 값 | 제목·원문 근거, 오탐 시 조치 |

**마지막 연결 시연:** API-07에서 찾은 ID로 API-03을 조회한 뒤, 같은 ID를 API-08 요약 URL에 넣습니다. 요약 응답의 `report_id`와 `source_revision`이 방금 조회한 ID·revision과 같은지 확인합니다. 검색이 `not_found`이면 요약을 호출하지 않습니다. Basic에 새 자동 연결 API를 만들 필요는 없습니다.

Postman Environment의 `allow_paid_llm`은 기본 `false`입니다. 실제 요약을 확인할 때만 키·모델·비용을 확인한 후 `true`로 바꾸고 별도 유료 선택 폴더의 요청을 수동 실행합니다. 확인 후 `false`로 돌립니다.

## 완료 기준

`report_categories=6`, `reports=180`(새 생성 전), 6종 상세 각 30, `prompt_versions=60`, E5 Vector 실제 180;
등록→조회→수정→삭제, Keyword/Semantic 검색, LLM 요약, 기본 Action Router 동작을 Postman으로 확인합니다.
데이터 수는 본인이 CREATE/DELETE한 이후 달라질 수 있습니다. 검증 SQL 실행 시점에 주의하세요.

## 비전공자 확인

- **flush**: SQL을 DB에 보내고 자동 ID를 확보할 수 있지만, 아직 **commit 전**이므로 롤백 가능.
- **commit**: DB가 변경을 확정. **rollback**: 미확정 변경 취소.
- **ORM**: Python 클래스로 DB 테이블을 표현.
- **Transaction**: 보고서+상세+Vector를 함께 성공/실패시키는 단위.
- **E5 Prefix**: passage는 저장할 문서, query는 검색어. 384차원은 Vector의 요소 384개.
- **Mock/Fixture**: 테스트 대체값. 실제 DB·E5·LLM 성공이라고 말하면 안 됩니다.

## mentee와 mentor 일대일 대응 원칙

- `mentee/01_basic/app/**/*.py`는 `mentor/01_basic/app/**/*.py`와 파일명·클래스·함수 시그니처·HTTP Method/Path가 같습니다.
- 빈칸은 TODO가 표시된 **함수 본문**뿐입니다. 실행을 위해 필요한 ORM 필드 매핑·Pydantic 계약·DB Session·`main()`은 공통 골격으로 제공합니다.
- `mentor/01_basic`의 API는 **API-00~09 (10개)**입니다. API-10~11은 Intermediate, API-12~14는 Advanced에서 새로 작성하는 기능입니다.
- `scripts/index_overviews.py`도 두 폴더에 `index_overviews()`와 완성된 `main()`이 동일하게 존재합니다.
- 기본 기능이 미완성인 상태에서 `NotImplementedError`가 발생하는 것은 정상입니다. TODO가 완료되면 제거하세요.
