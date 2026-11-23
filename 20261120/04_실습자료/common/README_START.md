# 보고서 처리 Agent · 오후 개인 프로젝트 시작 안내

**반드시 명세서 v1.4를 먼저 읽으세요.** 실습 기준은 SRS → ERD → API/JSON → 완료 체크리스트입니다.

## 1. 제공 자료 역할

- `common/docs/요구사항명세서_v1_4.html`: 상세 ERD·15개 API·33개 기능 요구사항.
- `common/sql/schema.sql`: **10개 물리 테이블**, FK/PK/NOT NULL/CHECK/DEFAULT + 조회용 VIEW (VIEW는 테이블이 아님).
- `common/sql/seed.sql`: 6개 카테고리, 180개 보고서/상세(각 30), Prompt 버전 60행. 재실행 중복 방지.
- `common/sql/verify.sql`: DB 상태/데이터 개수 검사. 시드 직후 벡터는 0개가 정상.
- `common/postman`: Postman Collection/Environment 및 실행 순서 문서.
- `common/.env.example`, `common/requirements.txt`: 환경 계약. API 키/DB 비밀번호를 공개하지 않습니다.

## 2. 난이도별 시작 상태 (최종 구조는 동일)

- **01_basic:** Router/Service/Repository/Embedding/LLM 함수 시그니처와 상세 TODO를 제공합니다. `app/main.py`의 `main()`과 실행 진입 코드는 완성. CRUD 본문은 미완성입니다.
- **02_intermediate:** 디렉터리만 제공합니다. Python 파일은 본인이 생성합니다. 명세서의 B + I 요구사항을 구현합니다.
- **03_advanced:** 빈 프로젝트 디렉터리만 있습니다. 폴더·Python 파일 모두 직접 작성합니다. 공통 SQL·환경 파일은 별도 사용합니다.

## 3. Windows 11 · Git Bash 실행 순서

1. 아래 4절대로 공통 파일을 선택한 프로젝트로 복사합니다. 기존 `.venv`를 활성화하고 `pip install -r requirements.txt`를 실행합니다. `.env.example`을 `.env`로 복사해 DB·LLM 값과 **선택한 PROJECT_LEVEL**을 설정합니다.
2. DB가 없으면 `sql/00_create_database.sql`을 **postgres 기본 DB**에서 1회 실행합니다. pgvector가 설치된 상태에서 `sql/schema.sql` → `sql/seed.sql`을 **실습 DB의 pgAdmin Query Tool**에서 실행하고 6/180/각30/60건을 확인합니다.
3. ORM·DB Session·FastAPI 진입점을 확인하고 카테고리·시드 ID/제목 조회를 연결합니다. Basic은 제공 골격을 사용합니다. `python -m app.main`으로 서버를 실행해 확인하고 코드 변경 후에는 재시작합니다.
4. `embedding_client.encode()`와 `report_service.encode_overview()`를 준비한 뒤 CRUD를 구현합니다. **POST가 개요 벡터도 저장하므로 E5 어댑터가 먼저 필요합니다.**
5. `scripts/index_overviews.py`를 구현·실행해 초기 개요 180건을 실제 E5로 일괄 색인합니다. `sql/verify.sql`로 벡터·ready·revision을 확인한 뒤 Hybrid 검색을 연결합니다.
6. LLM 요약·Agent를 연결합니다. Postman JSON을 Import해 API-00~09를 단계별로 확인합니다. 확장 요청은 해당 단계 구현 후 실행합니다.
7. Postman 응답과 SQL 저장값을 비교하고 `common/data/search_cases.json`으로 검색 의미를 확인합니다. 마지막으로 검색 결과 ID를 요약 API에 넘겨 출처를 대조합니다. Basic 상세 순서는 `mentee/01_basic/README.md`의 체크포인트를 따릅니다.

180건은 초기 시드 기준입니다. CRUD에서 생성한 보고서는 정리하거나 추가 건수를 구분해 검사합니다. `/health`의 vector ready는 pgvector 확장 준비 확인이며 180건 색인 완료 증거는 검증 SQL로 확인합니다.

## 4. 프로젝트 파일 복사

`common/`의 `sql/`, `.env.example`, `requirements.txt`, `.gitignore`를 **선택한 난이도의 프로젝트 루트**로 복사하세요.
Advanced에는 처음부터 파일이 없지만 제공된 공통 환경·SQL까지 구현하라는 뜻은 아닙니다.

### 선택한 단계의 환경값

공통 `.env.example`의 기본값은 `basic`입니다. 상위 단계는 `.env`에서 반드시 바꿉니다.

| 프로젝트 | PROJECT_LEVEL |
| --- | --- |
| 01_basic | basic |
| 02_intermediate | intermediate |
| 03_advanced | advanced |

프로젝트 루트에서 실제 적용값을 확인합니다. 기대값과 다르면 서버 실행 전에 `.env`와 터미널 환경값을 점검합니다.

```bash
python -c "from app.core.config import settings; print(settings.project_level)"
```

**기본 구현 순서**: DB·Seed → ORM·Session → E5 어댑터 → CRUD → 일괄 색인 → Hybrid → LLM·Agent → Postman.

**요약 비용**: Postman 유료 요청 5개는 별도 선택 폴더에 있습니다. Environment의 `allow_paid_llm`은 기본 `false`이며, 키·모델·비용을 확인한 뒤 실행할 때만 `true`로 바꿉니다. 사용 후 다시 `false`로 돌립니다.
