# Windows 11 · VS Code 준비

## 1. 현재 폴더와 Python부터 확인

ZIP을 완전히 풀고 수강생은 `mentee`, 강사는 `mentor` 폴더를 VS Code로 엽니다. ZIP 안에서 직접 실행하지 않습니다. 기존 수업에서 정상 사용하던 가상환경을 선택합니다.

1. VS Code에서 `Ctrl+Shift+P` → **Python: Select Interpreter** → 기존 수업용 Python 선택.
2. **Terminal → New Terminal**에서 Git Bash를 엽니다.
3. 아래 명령은 **mentee 또는 mentor 루트**에서 실행합니다.

```bash
python -c "import sys; print(sys.executable)"
python tools/check_environment.py --group base
```

터미널의 Python 경로가 선택한 가상환경과 같은지 확인합니다. `.venv`가 이 폴더 안에 있다면 Git Bash에서 `source .venv/Scripts/activate`로 활성화할 수 있습니다. 가상환경 위치가 다르면 해당 환경의 실제 경로를 사용합니다. 실행 도구는 계속 VS Code이며 Jupyter는 필요하지 않습니다.

## 2. 패키지

새로 쓰는 LangChain 패키지와 검사 도구를 설치합니다. 이미 정상인 환경은 먼저 `pip show`와 위 검사 결과를 확인하세요.

```bash
python -m pip install -r requirements.txt
python -m pip install -r requirements_test.txt
python tools/check_environment.py --group llm
```

| 파일 | 범위 |
|---|---|
| requirements_base.txt | Document·Prompt·Runnable, Pydantic, FastAPI, 로컬 TestClient |
| requirements_llm.txt | 기본 패키지 + 실제 ChatOpenAI 어댑터 |
| requirements.txt | 위 LLM 묶음과 동일한 기본 설치 진입점 |
| requirements_live.txt | 기본 묶음 + E5·psycopg·pgvector |
| requirements_test.txt | pytest |

기본 경로는 Python 3.11 이상으로 작성했고, 제작 검수는 Python 3.12에서 진행했습니다. `docs/TESTED_ENVIRONMENT.md`의 검수 버전과 실제 실행 범위를 구분해서 읽으세요. 설치 충돌이 나면 오류에 나타난 두 패키지 버전을 강사와 확인합니다. 작업 중인 다른 프로젝트의 환경을 무조건 재설치하지 않습니다.

## 3. LLM 설정 — 실습 05·06·08

역할 루트의 `.env.example`을 복사하여 **같은 위치**에 `.env`를 만듭니다. 기존 `.env`가 있다면 덮어쓰지 말고 필요한 항목만 보완합니다.

```dotenv
OPENAI_API_KEY=본인의_유효한_API_Key
LLM_MODEL=수업에서_사용권한을_확인한_정확한_모델_ID
```

코드에는 Responses API와 `json_schema` Structured Output을 사용하는 설정이 들어 있습니다. 앞서 사용하던 모델의 지원 여부와 계정 권한을 확인하여 `LLM_MODEL`에 지정합니다. Key나 모델명을 Python 소스에 붙여 넣지 않습니다. `.env`는 제출하거나 Git에 올리지 않습니다.

`.env` 위치는 `01_basic/05_prompt_model` 안이 아니라 **mentee 또는 mentor 루트**입니다. 터미널에 같은 환경 변수가 이미 설정되어 있으면 그 값이 우선하므로 `.env`를 고쳤는데도 이전 설정을 사용한다면 새 터미널을 열고 확인합니다.

실습 05·06에서 `python main.py`는 실제 호출입니다. `--offline`은 고정 예시로 입력·출력 연결을 확인하는 선택입니다. 두 실행은 결과 JSON에 구분하여 기록됩니다. 실제 호출 실패를 자동으로 예시 답변으로 바꾸지 않습니다.

## 4. E5·PostgreSQL 준비 — 실습 04 선택 / 실습 08 실제 경로

이번 실습은 Windows에 이미 설치한 PostgreSQL을 사용합니다. 별도 Docker나 WSL은 필요하지 않습니다. 먼저 기존 E5 환경을 확인합니다.

```bash
python tools/check_environment.py --group live
```

필요한 패키지가 없을 때만 설치 파일을 확인하여 추가합니다.

```bash
python -m pip install -r requirements_live.txt
```

E5는 `intfloat/multilingual-e5-small`을 CPU에서 사용합니다. 첫 실행에는 모델 파일 다운로드와 디스크 공간이 필요합니다. 같은 모델을 이미 내려받았다면 캐시를 사용합니다. 문서와 질문을 동일한 모델·revision·접두어 규칙으로 처리하며, 저장한 Embedding 계약이 달라지면 검색을 중단합니다. 이 입력 규칙과 384차원은 [공식 모델 카드](https://huggingface.co/intfloat/multilingual-e5-small)에서 확인할 수 있습니다.

### 4-1. pgAdmin에서 대상 DB와 vector 확장 확인

1. pgAdmin 왼쪽에서 수업용 DB(예: `knowledge_lab`)를 선택합니다.
2. 해당 DB의 **Query Tool**을 엽니다.
3. 다음 SQL을 실행합니다.

```sql
SELECT current_database();
SELECT extname, extversion FROM pg_extension WHERE extname = 'vector';
SELECT name, default_version, installed_version
FROM pg_available_extensions WHERE name = 'vector';
```

- 두 번째 조회에 한 행이 있으면 현재 DB에서 확장을 사용할 수 있습니다.
- 두 번째 조회는 비어 있고 세 번째 조회에 `vector`가 있다면, 확장 설치 권한이 있는 계정으로 현재 DB에서 다음을 실행합니다.

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

- 세 번째 조회에도 없다면 PostgreSQL **서버 확장 파일**이 아직 설치되지 않은 상태입니다. `pip install pgvector`로 해결되지 않습니다. 강사가 [pgvector 공식 Windows 설치 절차](https://github.com/pgvector/pgvector#windows)를 통해 현재 PostgreSQL의 버전·설치 경로와 맞는 확장을 준비한 뒤 다시 확인합니다. 일반 Git Bash의 pip 작업과 Visual Studio의 서버 확장 빌드 작업을 혼동하지 않습니다.

### 4-2. `.env`의 DB 값 입력

```dotenv
PGHOST=localhost
PGPORT=5432
PGDATABASE=knowledge_lab
PGUSER=postgres
PGPASSWORD=본인의_DB_비밀번호
RAG_SCHEMA=d26_rag
E5_REVISION=main
```

`PGUSER`·DB 이름은 자신의 실제 계정에 맞춥니다. 공백이나 `#`가 포함된 값은 dotenv 형식에 맞게 따옴표로 감쌉니다. 이전 수업의 `.env` 전체를 코드와 함께 복사하지 말고 필요한 연결 값만 확인합니다.

### 4-3. 오늘 사용할 세 문서 준비

역할 루트에서 먼저 안내를 읽습니다.

```bash
python tools/setup_db.py
```

이 명령은 준비 계획만 출력합니다. 실제 준비는 다음 명령입니다.

```bash
python tools/setup_db.py --apply
```

준비 코드는 강의의 출석·과제·시설 본문을 실제 E5로 임베딩하고, Day26 전용 Schema에 저장하여 현재 버전을 공개합니다. 이전 실습의 Schema를 가져오지 않으며, 삭제 명령도 포함하지 않습니다. 11월 19일 ZIP은 폴더·실행 구조를 참고한 것이므로 이 패키지는 그 ZIP이나 Python 모듈 없이 실행할 수 있습니다.

정상 완료 뒤 `outputs/db_setup.json`에서 실제 `citation_id`, 문서 ID, 버전, 원문 위치를 확인합니다. 실제 ID가 201·202·203이 아니어도 정상입니다. 이 숫자로 바꾸면 안 됩니다. 같은 설정으로 재실행하면 기존 청크 ID를 유지합니다. Embedding 계약이 달라진 기존 Schema를 덮어쓰지 않으며, 새로 준비하려면 예를 들어 `RAG_SCHEMA=d26_rag_v2`처럼 새 전용 이름을 사용합니다.

### 4-4. API 연결

실습 08의 TODO를 마친 뒤 해당 폴더에서 실행합니다.

```bash
python main.py
```

FastAPI TestClient는 TCP 서버를 열지 않고 실제 경로 함수·요청 검사를 실행합니다. 이 실습의 기본 모드는 그 내부에서 실제 E5·DB·LLM을 사용합니다. **TestClient를 쓴다는 사실만으로 모든 의존성이 모의 실행이 되는 것은 아닙니다.** `--offline`을 붙여야 제공된 고정 Retriever·Generation을 사용합니다.

서버를 직접 열 때는 다음을 사용합니다.

```bash
python main.py --serve
```

브라우저에서 `http://127.0.0.1:8000/docs`를 열고 `POST /rag/answer`의 **Try it out**으로 아래 JSON을 보냅니다. 종료는 서버 터미널에서 `Ctrl+C`입니다.

```json
{"query":"15분 늦으면 어떻게 기록되나요?","category":"학사","candidate_k":3,"context_k":2}
```

`candidate_k`는 검색 후보 수의 상한, `context_k`는 Context에 실제 포함할 수의 상한입니다. 둘 다 보장 개수가 아니며, 중복·문자 상한·자료 상태에 따라 실제 개수는 더 적을 수 있습니다.

## 자주 발생하는 문제

| 현상 | 확인 순서 |
|---|---|
| NotImplementedError: D26-… | 현재 TODO의 ID를 찾고 해당 함수부터 완성합니다. |
| ModuleNotFoundError | `sys.executable` 확인 → 같은 Python의 `python -m pip`로 설치합니다. |
| 401 / token_invalidated | 현재 Key가 유효한지 확인하고 필요한 경우 유효한 Key로 교체합니다. 파일이 있다는 사실만으로 인증이 성공하지 않습니다. |
| 404 / 모델 접근 오류 | 정확한 모델 ID, 계정 권한, Responses/Structured Output 지원 여부를 확인합니다. |
| 429 / Timeout | 요청 제한·연결 실패입니다. 근거 부족 결과로 바꾸지 않습니다. |
| password authentication failed | 실제 DB 계정·비밀번호와 접속 DB를 확인합니다. |
| vector 확장 오류 | Python 패키지와 PostgreSQL 서버 확장을 구분하고 4-1을 다시 확인합니다. |
| Day26 Schema/테이블 없음 | `tools/setup_db.py --apply`의 성공 여부와 `RAG_SCHEMA`를 확인합니다. |
| Embedding 계약 불일치 | 같은 E5·revision으로 준비했는지 확인합니다. 같은 384차원만으로는 충분하지 않습니다. |
| 예상 문장과 실제 답변이 다름 | 상태·출처·핵심 주장과 원문을 대조합니다. 문장 일치만으로 평가하지 않습니다. |

공식 참고: [FastAPI TestClient](https://fastapi.tiangolo.com/tutorial/testing/), [LangChain Structured Output](https://reference.langchain.com/python/langchain-openai/chat_models/base/ChatOpenAI/with_structured_output), [pgvector Python](https://github.com/pgvector/pgvector-python).
