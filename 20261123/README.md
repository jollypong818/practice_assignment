# 2026-11-23 · Day26 Basic RAG & LangChain 실습자료

**8개 실습 × 3수준 × 수강생·강사용 대응**입니다. 11월 23일 **82페이지 HTML 강의자료**의 실습 안내와 연결됩니다.

- `mentee/`: **수강생용**. 직접 완성할 TODO가 있습니다. 학생에게 배포하는 폴더입니다.
- `mentor/`: **강사용**. 완성 코드, 상세 주석, 강사 운영 가이드가 있습니다.
- `01_basic`(기본필수), `02_intermediate`(응용), `03_advanced`(심화) 중 **한 단계만 선택**합니다. 특심화는 없습니다.
- 수강생은 `mentee/`, 강사는 `mentor/`를 각각 **VS Code 프로젝트 폴더**로 엽니다. 역할 폴더만 따로 복사해도 실행할 수 있습니다.
- 11월 19일 실습자료에서는 **폴더·실행·안내의 구성 방식만** 참고했습니다. 학습 내용은 Day26 RAG·LangChain용입니다.

**실습 순서:** RAG 흐름 → Hit/Context → LangChain 객체 → Document Adapter → Prompt/Chat Model → Runnable/Structured Output → Validation → FastAPI RAG.

> **중요:** 실습 05·06·08의 `python main.py`는 기본적으로 **실제 LLM API 경로**입니다. 실행하면 API 사용량과 비용이 발생할 수 있습니다. 연결을 연습할 때만 `--offline`을 명시하세요. `--offline`의 고정 결과는 실제 검색·모델 성능을 의미하지 않습니다.

---

## 1. 실습 환경과 준비 순서

이 자료는 **Windows 11 + VS Code + Python 가상환경 + Git Bash**를 기준으로 설명합니다. PostgreSQL은 Windows에 직접 설치되어 있다고 가정합니다. **Docker·WSL·Jupyter는 필수가 아닙니다.**

| 항목 | 사용 목적 | 필요한 실습 |
|---|---|---|
| Python **3.11 이상** (새 환경은 3.12 권장) | Python 코드 실행 | 전체 |
| VS Code + Python 확장 | 파일 편집, interpreter 선택, Terminal | 전체 |
| `langchain-core`, `pydantic`, `fastapi` 등 | Document·Prompt·Runnable 및 API | 전체 |
| `langchain-openai`, `openai` | 실제 Chat Model 호출 | 05·06·08 |
| OpenAI API Key + 사용 가능한 모델 ID | 인증·모델 실행 | 05·06·08 실제 경로 |
| PostgreSQL + **서버 확장 pgvector** | 문서 Embedding 저장·검색 | 04 `--live-db`, 08 실제 경로 |
| `sentence-transformers`, PyTorch, `psycopg`, `pgvector`(Python) | CPU E5 Embedding 및 PostgreSQL 연결 | 04 `--live-db`, 08 실제 경로 |
| `pytest` | 실습별 테스트 | 테스트 실행 시 |

**추천 순서:** ZIP 압축 해제 → VS Code로 역할 폴더 열기 → Python/venv 확인 → 기본 패키지 설치 → `.env` 입력 → 로컬 실습 01~04 → LLM 연결 05~06 → pgvector·E5 준비 → 실습 08 → API 문서·결과 확인.

### 1-1. 압축 해제 후 폴더 위치 확인

ZIP을 완전히 해제합니다. ZIP 내부의 파일을 압축 해제하지 않은 상태에서 실행하면 안 됩니다.

```text
20261123_Day26_RAG_LangChain/
├─ README.md                  ← 지금 읽고 있는 문서
├─ mentee/                    ← 수강생은 이 폴더를 VS Code로 엽니다
│  ├─ .env.example
│  ├─ README.md
│  ├─ requirements.txt
│  ├─ requirements_live.txt
│  ├─ requirements_test.txt
│  ├─ coursekit/
│  ├─ data/
│  ├─ docs/
│  ├─ tools/
│  ├─ 01_basic/
│  ├─ 02_intermediate/
│  └─ 03_advanced/
└─ mentor/                    ← 강사는 이 폴더를 VS Code로 엽니다
```

이하 명령은 **`mentee/` 또는 `mentor/` 폴더를 현재 작업 폴더로 연 Terminal**에서 실행한다고 가정합니다. `README.md`만 있는 바깥쪽 최상위 폴더에서 실행하면 `requirements.txt`가 없다는 오류가 발생합니다.

### 1-2. Python과 VS Code interpreter 확인

VS Code에서 **File → Open Folder**로 `mentee` 또는 `mentor`를 열고, `Ctrl+Shift+P` → **Python: Select Interpreter**를 선택합니다. **Terminal → New Terminal**을 열고 현재 Python 경로를 확인합니다.

```bash
python --version
python -c "import sys; print(sys.executable)"
python -m pip --version
```

Python 3.11 이상이어야 합니다. 아래 명령에서 **Python 실행 경로와 pip 경로가 선택한 가상환경인지** 확인하세요. Windows에 여러 Python이나 `.venv`가 있는 경우 특히 중요합니다.

#### 기존 수업용 가상환경 사용

기존 환경이 정상이라면 그대로 사용할 수 있습니다. 다만 아래 패키지는 버전이 지정되어 있으므로, **다른 프로젝트에서 사용 중인 가상환경에 무조건 설치하지 마세요.** 패키지 충돌이 걱정되면 Day26 전용 환경을 만듭니다.

#### 새 가상환경 생성 — Git Bash

새 환경을 만드는 경우 Python 3.12가 설치되어 있다면 다음 예시를 사용합니다. `py -3.12`가 없다면 `py -0p`로 설치된 Python 목록을 확인하거나, 3.11 이상의 기존 Python 명령을 사용하세요.

```bash
py -3.12 -m venv .venv
source .venv/Scripts/activate
python --version
python -c "import sys; print(sys.executable)"
python -m pip install --upgrade pip
```

Git Bash에서 `source .venv/Scripts/activate` 대신 **PowerShell**을 사용한다면 다음처럼 활성화합니다.

```powershell
.\.venv\Scripts\Activate.ps1
```

PowerShell 실행 정책에 따라 활성화가 막힌 경우, 정책 변경을 강요하지 않고 `.venv\Scripts\python.exe`로 직접 실행할 수 있습니다. VS Code에서 `.venv\Scripts\python.exe`를 interpreter로 선택하는 방법도 가능합니다.

가상환경 종료: `deactivate`.

---

## 2. 필요한 Python 패키지 설치

`requirements*.txt`는 **각 역할 폴더에 존재합니다.** 설치는 반드시 현재 interpreter를 사용하는 `python -m pip`로 실행합니다.

### 2-1. 필수 패키지 — 전체 실습의 기본 준비

```bash
python -m pip install -r requirements.txt
python -m pip install -r requirements_test.txt
python tools/check_environment.py --group base
python tools/check_environment.py --group llm
python tools/check_environment.py --group test
```

`requirements.txt`는 내부적으로 `requirements_llm.txt` → `requirements_base.txt`를 포함합니다. 즉 **LangChain 기본 구성, FastAPI, OpenAI 어댑터**가 한 번에 설치됩니다. 테스트용 `pytest`는 `requirements_test.txt`로 별도 설치합니다.

### 2-2. DB·E5 실제 연동 패키지 — 실습 04 선택 / 실습 08 필수

```bash
python -m pip install -r requirements_live.txt
python tools/check_environment.py --group live
```

`requirements_live.txt`는 기본·LLM 패키지 외에 `numpy`, `psycopg[binary]`, **Python용 `pgvector`**, `sentence-transformers`를 설치합니다. `sentence-transformers`는 PyTorch를 사용합니다. **이 Python 패키지 설치와 PostgreSQL 서버의 `vector` 확장 설치는 별개**입니다.

첫 E5 실행 때 `intfloat/multilingual-e5-small` 모델이 인터넷에서 다운로드될 수 있습니다. 모델은 **CPU 사용**으로 구현되어 있으므로 CUDA GPU를 필수로 요구하지 않습니다. 실행 중 다운로드가 막힌 경우 인터넷·프록시·Hugging Face 접근 정책을 확인해야 합니다.

### 2-3. 설치된 버전 확인

```bash
python -m pip show langchain-core langchain-openai openai pydantic fastapi
python -m pip show sentence-transformers torch psycopg pgvector
python -m pip check
python tools/check_environment.py --group all
```

`--group all`은 실제 연동과 테스트용 패키지까지 전부 요구하므로, 1~03만 준비했다면 일부 미설치가 정상입니다. `check_environment.py`는 **패키지 존재와 버전만 검사**하며, API 인증·DB 접속·모델 다운로드 성공까지 보장하지는 않습니다.

참고로 배포 자료에서 버전이 지정된 주요 패키지는 `langchain-core==1.8.4`, `langchain-openai==1.8.5`, `openai==3.57.0`, `pydantic==2.13.4`, `fastapi==0.141.1`, `pytest==9.2.0`, `psycopg[binary]==3.3.9`, `pgvector==0.5.1`입니다. `sentence-transformers`는 `>=3.0,<7.0` 범위로 지정되어 있습니다. 실제 전체 사양은 역할 폴더의 `requirements*.txt`가 기준입니다.

---

## 3. 환경변수 `.env` 설정

`.env`는 **`mentee/.env` 또는 `mentor/.env`**에 생성합니다. `01_basic/05_prompt_model/` 등의 개별 실습 폴더 안이 아닙니다.

Git Bash에서 파일 복사:

```bash
cp .env.example .env
```

PowerShell에서 복사:

```powershell
Copy-Item .env.example .env
```

VS Code로 `.env`를 열고 아래 항목을 본인 환경에 맞게 수정합니다.

```dotenv
# 실습 05·06·08의 실제 Chat Model 호출에 사용
OPENAI_API_KEY=본인의_실제_API_Key
LLM_MODEL=수업에서_사용가능함을_확인한_정확한_모델_ID

# 실습 04 --live-db 및 실습 08 실제 DB 연결
PGHOST=localhost
PGPORT=5432
PGDATABASE=knowledge_lab
PGUSER=postgres
PGPASSWORD=본인의_PostgreSQL_비밀번호
RAG_SCHEMA=d26_rag
E5_REVISION=main
```

**주의:** 예시의 `본인의_실제_API_Key`와 모델 ID는 설명용 값입니다. 실제 입력이 필요합니다. `OPENAI_API_KEY`에 접근할 수 있고 `LLM_MODEL`이 정확히 존재하며, 해당 모델이 **Responses API + JSON Schema Structured Output**을 지원해야 합니다. API Key가 있어도 무효화됐거나 접근 권한이 없다면 호출은 실패합니다.

- **API Key·비밀번호는 README, Python 코드, 결과 JSON, Git에 올리지 않습니다.** `.env`를 제출하지 마세요.
- 기존 `.env`가 있다면 덮어쓰지 말고 필요한 값만 확인합니다.
- 터미널의 OS 환경변수에 같은 이름이 존재하면 코드의 dotenv 로드보다 **기존 환경변수가 우선**합니다. `.env`를 수정했는데 이전 값을 사용하면 터미널 환경을 확인하세요.
- 실습 01~04의 기본 실행과 실습 07에는 실제 LLM 인증이 필요 없습니다. 실습 05·06·08의 실제 경로만 필요합니다.
- `401`, `token_invalidated`는 인증 실패입니다. Key나 권한을 갱신해야 하며, `.env` 파일이 존재한다는 사실만으로 해결되지 않습니다.

---

## 4. PostgreSQL·pgvector 준비 — 실제 DB 연동 시

실습 환경은 **Windows에 직접 설치한 PostgreSQL**입니다. Docker/WSL은 사용하지 않습니다. DB를 준비하지 않아도 실습 01~03, 04 기본 실행, 05·06 `--offline`, 07, 08 `--offline`은 진행할 수 있습니다.

### 4-1. pgAdmin에서 PostgreSQL 접속과 확장 확인

1. Windows에서 **pgAdmin 4**를 실행해 PostgreSQL 서버에 접속합니다.
2. 수업용 데이터베이스 `knowledge_lab`(또는 본인의 DB)를 선택하고 **Query Tool**을 엽니다.
3. 다음 SQL을 실행합니다.

```sql
SELECT current_database();
SELECT extname, extversion FROM pg_extension WHERE extname = 'vector';
SELECT name, default_version, installed_version
FROM pg_available_extensions WHERE name = 'vector';
```

- 두 번째 결과에 `vector`가 있으면 **현재 DB에 pgvector 확장이 생성된 상태**입니다.
- 두 번째 결과가 비었지만 세 번째에 `vector`가 있다면, 해당 DB에서 적절한 권한으로 다음을 실행합니다.

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

- 세 번째 결과에도 `vector`가 없다면 **PostgreSQL 서버용 확장 자체가 설치되지 않은 상태**입니다. `pip install pgvector`만으로는 해결할 수 없습니다. 강사가 해당 PostgreSQL 버전에 맞춰 서버 확장을 설치해야 합니다. 공식 절차: https://github.com/pgvector/pgvector#windows
- 새 데이터베이스가 필요한 경우 강사가 생성·권한을 확인하고 `.env`의 `PGDATABASE`를 동일하게 수정합니다. 실습 코드는 **Day26 전용 Schema**를 사용하므로, 이전 날짜의 테이블을 임의로 수정할 필요가 없습니다.

### 4-2. DB 데이터 준비

역할 폴더 루트의 Git Bash에서 실행합니다.

```bash
# 계획만 출력: 아직 모델 다운로드·DB 기록 없음
python tools/setup_db.py

# 실제 E5 Embedding 생성 및 Day26 Schema 저장·공개
python tools/setup_db.py --apply
```

`--apply`는 **실제 E5 모델을 CPU에서 준비하고 PostgreSQL에 연결**합니다. 제공된 출석·과제·시설 3개 문서를 사용합니다. 성공 결과는 역할 폴더의 `outputs/db_setup.json`에 저장됩니다.

- 기본 Schema는 `d26_rag`이며 11월 19일의 Schema를 그대로 사용하지 않습니다.
- 문서는 `intfloat/multilingual-e5-small`, **384차원**, 문서의 `passage: ` / 질문의 `query: ` 접두어와 정규화된 벡터로 처리합니다.
- 실제 DB가 부여하는 `citation_id`는 강의용 고정 예시 `201/202/203`과 다를 수 있습니다. **고정 예시 번호로 덮어쓰지 않습니다.**
- 모델 ID·revision·접두어·차원 등 Embedding 계약이 기존 저장 내용과 다르면 검색을 중단합니다. 이 경우 별도의 Day26 전용 Schema 이름을 지정하고 다시 준비하세요.
- 준비 스크립트가 실패하면 성공 결과를 임의로 생성하거나 `--offline` 결과를 실제 성공이라고 기록하지 않습니다.

---

## 5. 실습 실행 방법

### 5-1. 본인의 난이도 한 단계 선택

| 수준 | 폴더 | TODO 특징 |
|---|---|---|
| 기본필수 | `01_basic` | 실습별 핵심 TODO 2개, `main.py` 중심 |
| 응용 | `02_intermediate` | 실습별 TODO 3개, `tasks.py` 사용 |
| 심화 | `03_advanced` | 실습별 TODO 4개, 추가 오류·경계 조건 검증 |

처음에는 **기본필수 한 단계만** 수행해도 됩니다. 세 단계를 모두 할 필요가 없습니다. TODO가 남아 있다면 `NotImplementedError: D26-...`가 발생할 수 있으며, 정상적인 학습 시작 상태입니다.

예시: 기본필수 실습 01

```bash
# mentee 또는 mentor 루트에서 시작
cd 01_basic/01_rag_flow
python main.py
python -m pytest -q tests
```

다음 실습으로 진행할 때는 해당 폴더의 `README.md`를 먼저 읽습니다. 각 실습은 앞 실습의 미완성 출력 파일이 없어도 시작할 수 있도록 Checkpoint가 제공됩니다. 현재 TODO를 Checkpoint 호출로 건너뛰지는 마세요.

### 5-2. 실제 호출과 고정 예시 실행 구분

| 실습 | 기본 `python main.py` | 추가 실행 |
|---|---|---|
| 01~03 | 로컬 개념·자료형·문자열 확인 | 별도 외부 서비스 필요 없음 |
| 04 | 제공 Hit를 LangChain Document로 변환 | `--live-db`로 실제 E5/DB Hit 변환 |
| 05 | 실제 Chat Model 호출 | `python main.py --offline` |
| 06 | 실제 Structured Output 호출 | `python main.py --offline` |
| 07 | 고정된 정상·오류 응답 Validation | 외부 모델 호출 없음 |
| 08 | 실제 E5·DB·LLM + FastAPI TestClient | `--offline`, `--serve` |

**실제 API 과금 주의:** 05·06·08의 기본 경로는 모델의 `invoke()`가 수행됩니다. 재시도 설정에 따라 실제 네트워크 요청이 더 많을 수 있습니다. TestClient를 사용해도 내부적으로 진짜 LLM·DB를 호출할 수 있습니다. `--offline`은 테스트용 고정 응답이며 실제 연동 결과와 구분해 기록합니다.

### 5-3. 실습 08: FastAPI 테스트와 브라우저 접속

실습 08의 TODO를 완료한 후:

```bash
# 역할 루트에서 해당 실습으로 이동
cd 01_basic/08_rag_api

# 실제 DB·E5·LLM으로 API 경로를 TestClient에서 호출
python main.py

# 외부 연결 없이 API 처리 흐름 확인
python main.py --offline

# 자동 테스트(외부 네트워크 사용 안 함)
python -m pytest -q tests

# 실제 HTTP 서버: 종료는 Ctrl+C
python main.py --serve
```

서버 실행 후 브라우저에서 `http://127.0.0.1:8000/docs` → `POST /rag/answer` → **Try it out**에서 아래 JSON을 보냅니다.

```json
{
  "query": "15분 늦으면 어떻게 기록되나요?",
  "category": "학사",
  "candidate_k": 3,
  "context_k": 2
}
```

`candidate_k`는 Retriever의 후보 수 상한, `context_k`는 실제 Context 포함 수 상한입니다. 응답 `result` 및 `sources`를 확인하고, 답변의 출처가 실제 선택한 Context에 포함된 문서인지 대조합니다. 브라우저에서 `/docs`가 열리지 않으면 서버가 실행 중인지, 터미널에 표시된 포트가 맞는지 확인하세요. 포트를 변경하려면 `python main.py --serve --port 8001`을 사용할 수 있습니다.

### 5-4. 한 수준의 전체 로컬 점검

아래 명령은 **역할 루트**에서 실행합니다. 진행 중인 실습의 TODO가 미완성이면 실패하는 것이 정상입니다. 05·06·08은 도구에서 자동으로 `--offline`을 사용합니다.

```bash
python tools/run_all.py --level 01_basic
python tools/run_all.py --level 01_basic --tests
```

정답 코드를 확인하려면 강사는 `mentor/`를 사용하고, 수강생에게는 `mentee/`만 배포하세요.

---

## 6. HTML 강의자료와 실습 연결

**기준 강의자료:** `Day26_20261123_Basic_RAG_LangChain_강의실습연계수정.html` (82페이지).

| 실습 | 강의 실습 안내 페이지 | 핵심 목표 |
|---|---:|---|
| 01 · RAG Flow | 9 | 검색·Context·응답의 단계별 역할 |
| 02 · Hit → Context | 18 | Context와 `included_ids` 생성 |
| 03 · LangChain Objects | 30 | Document·Retriever·Prompt·Chat Model 입력·출력 |
| 04 · Document Adapter | 40 | 검색 Hit의 본문·Metadata 유지 |
| 05 · Prompt & Model | 49 | `prompt.invoke()`와 `chat_model.invoke()` 구분 |
| 06 · Runnable Chain | 59 | Context·Structured Output 연결 |
| 07 · Validation | 70 | 형식·출처·원문 대조 |
| 08 · RAG API | 80 | 실제 검색·생성·검증·FastAPI 연결 |

강의 21페이지의 VS Code 프로젝트 구조는 **실무 서비스 파일 분리의 교육용 예시**로, 실습 ZIP의 파일명과 동일하지 않습니다. 역할별 `docs/LECTURE_CODE_MAP.md`를 참고해 실제 파일과 연결하세요.

---

## 7. 문제 해결 체크리스트

| 오류 또는 현상 | 확인할 사항 |
|---|---|
| `python`을 찾을 수 없음 | Python 설치 및 VS Code Terminal의 PATH, 선택 interpreter 확인 |
| `ModuleNotFoundError` | `python -c "import sys; print(sys.executable)"` → 그 Python에서 `python -m pip install -r requirements.txt` 실행 |
| `NotImplementedError: D26-...` | 학습용 TODO가 아직 미완성. 코드의 같은 ID 위치를 완성 |
| `401`, `token_invalidated` | API Key가 무효화됐거나 권한 없음. 유효한 Key·계정·모델 권한 확인 |
| `404`, 모델 접근 불가 | `LLM_MODEL`의 **정확한 모델 ID**, Responses/Structured Output 지원 여부 확인 |
| `429`, Timeout | Rate Limit·네트워크·요청 제한·재시도 기록 확인. 근거 부족 응답과 구분 |
| PostgreSQL 인증 실패 | `.env`의 `PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER`, `PGPASSWORD` 확인 |
| `vector` 확장 없음 | `pip install pgvector`가 아니라 PostgreSQL **서버 확장** 설치·`CREATE EXTENSION` 필요 |
| `d26_rag` 테이블 없음 | 역할 루트에서 `python tools/setup_db.py --apply` 실행했는지 확인 |
| E5 모델 다운로드 실패 | 인터넷, Hugging Face 접근, 디스크 공간, Python 패키지 확인 |
| Embedding 계약 불일치 | 모델·revision·prefix·차원·정규화 조건 확인. 기존 벡터를 섞지 않음 |
| 422 | API 요청 JSON의 `query`, `category`, `candidate_k`, `context_k` 검증 |
| 502 | 검색·모델·출력 검증 오류 상세 확인. 정상적인 `insufficient_context`와 구분 |
| 응답 문장이 예시와 다름 | 모델의 표현은 달라질 수 있음. 상태·근거·조건·출처를 원문과 대조 |

## 8. 완료 기준과 보안 유의사항

- 선택한 난이도의 실습 8개에서 TODO를 완성하고 각 `tests/`를 실행합니다.
- 실습별 `outputs/`의 결과를 확인하며, `reports/review.md`에 본인의 설명과 출처 대조를 작성합니다.
- **`--offline`과 live 결과를 반드시 구분**합니다. 실습 08은 실제 DB·Embedding·LLM 경로를 실행했을 때만 실연동 성공으로 기록합니다.
- `.env`, API Key, PostgreSQL 비밀번호는 제출·Git Commit·공유 화면에 노출하지 않습니다.
- 21페이지 파일 대응 관계는 `docs/LECTURE_CODE_MAP.md`, 자세한 Windows 도움말은 `docs/SETUP_WINDOWS.md`, 검수 환경과 한계는 `docs/TESTED_ENVIRONMENT.md`를 참고합니다.

**검수 범위 안내:** 패키지와 코드의 원본 실행 전제를 기준으로 작성했습니다. `check_environment.py` 실행 성공은 실제 PostgreSQL/E5/LLM 연결을 보장하지 않습니다. 수업 PC에서 모델 다운로드, DB 서버 확장 및 API 인증을 각각 확인해야 합니다.

### 참고 자료

- [LangChain Python](https://docs.langchain.com/oss/python/langchain/overview)
- [FastAPI TestClient](https://fastapi.tiangolo.com/tutorial/testing/)
- [pgvector](https://github.com/pgvector/pgvector) / [pgvector Python](https://github.com/pgvector/pgvector-python)
- [multilingual-e5-small 모델 카드](https://huggingface.co/intfloat/multilingual-e5-small)
