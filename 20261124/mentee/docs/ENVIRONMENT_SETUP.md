# Windows 11 · VS Code · Git Bash 기준 상세 환경설정

## 0. 사전 점검

- **Python 3.12** 권장. `py -0p`로 목록, `py -3.12 --version`으로 설치 여부 확인
- **VS Code**에서 `mentee` 또는 `mentor` 폴더를 열고 Terminal → New Terminal
- PostgreSQL은 Windows 11에 직접 설치되어 있다고 가정합니다. Docker/WSL은 사용하지 않습니다.
- NVIDIA GPU·Driver가 있어야 합니다. `nvidia-smi` 출력에서 GPU/Driver/VRAM 확인
- 회사 보안 정책에서 모델 다운로드 또는 API 호출이 차단될 수 있습니다.

## 1. 가상환경 만들기

Git Bash:

```bash
py -3.12 -m venv .venv
source .venv/Scripts/activate
python --version
python -m pip --version
```

PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python --version
```

PowerShell에서 실행 정책이 막히면 Git Bash를 사용하십시오. VS Code: `Ctrl+Shift+P` → `Python: Select Interpreter` → 현재 역할 폴더의 `.venv/Scripts/python.exe` 선택. 새 Terminal을 열어 반영을 확인합니다.

## 2. PyTorch CUDA 먼저 설치

- 공식 설치 선택기: https://pytorch.org/get-started/locally/
- **Windows / Pip / Python / CUDA** 조합을 현재 PC에 맞춰 선택한 뒤 제시되는 명령을 실행합니다.
- 단순 `pip install torch`로 CUDA Build가 준비됐다고 가정하지 않습니다.

```bash
nvidia-smi
python -c "import torch; print('torch:',torch.__version__); print('built CUDA:',torch.version.cuda); print('available:',torch.cuda.is_available()); print('gpu:',torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'NOT AVAILABLE')"
```

`torch.cuda.is_available()`가 `False`이면 실제 실습 실행 전에 GPU 환경부터 해결하십시오. 수업에서는 **CPU 자동 Fallback을 사용하지 않습니다.**

## 3. 라이브러리 설치

역할 폴더에서 순서대로 실행합니다.

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -r requirements_test.txt
python -m pip install -r requirements_live.txt
python -m pip check
python tools/check_environment.py
```

- `requirements.txt`: LangChain Core·OpenAI·FastAPI
- `requirements_test.txt`: pytest
- `requirements_live.txt`: NumPy·E5·Cross-Encoder·psycopg·pgvector Python Adapter
- `pip install pgvector`는 **Python Adapter**를 설치할 뿐, PostgreSQL Server의 `vector` 확장을 설치하지 않습니다.
- 기존 정상 환경과 충돌할 때는 무조건 재설치하지 말고 가상환경/실행 Interpreter를 먼저 확인합니다.

## 4. .env 만들기 (Key 비공개)

```bash
cp .env.example .env
```

`.env`에서 `OPENAI_API_KEY`, `LLM_MODEL`, `PGPASSWORD`를 본인 값으로 변경합니다.

```dotenv
OPENAI_API_KEY=실제_API_Key
LLM_MODEL=사용_가능한_OpenAI_모델_ID
PGHOST=localhost
PGPORT=5432
PGDATABASE=knowledge_lab
PGUSER=postgres
PGPASSWORD=본인_DB_비밀번호
RAG_SCHEMA=d27_rag
E5_REVISION=main
```

- 모델은 **Structured Output(JSON Schema)**를 지원하는 모델을 사용합니다. 해당 프로젝트의 계정/모델 설정을 사용하십시오.
- Key를 README·과제 파일·터미널 출력·GitHub에 업로드하지 마세요.
- 401=인증 정보, 429=사용량 제한, 5xx=서버 측 실패를 구분합니다.

## 5. pgAdmin으로 PostgreSQL·pgvector 확인

1. pgAdmin → 연결 서버 → Databases → `knowledge_lab` → Query Tool
2. 다음을 실행합니다.

```sql
SELECT version();
SELECT extname, extversion FROM pg_extension WHERE extname = 'vector';
```

`vector`가 없다면 Windows용 PostgreSQL **서버 확장**을 해당 PostgreSQL 버전에 맞춰 별도로 설치해야 합니다. 그 후 권한 있는 계정으로 아래 SQL을 실행합니다.

```sql
CREATE EXTENSION IF NOT EXISTS vector;
SELECT extname, extversion FROM pg_extension WHERE extname = 'vector';
```

`ERROR: extension "vector" is not available`은 Python 패키지를 설치해도 해결되지 않습니다. PostgreSQL 버전과 서버 DLL/extension 설치 여부를 확인하십시오. Docker·WSL은 이번 수업의 필수 경로가 아닙니다.

## 6. E5 + Corpus → DB 준비 (실제 GPU/DB)

```bash
# 먼저 현재 상태만 확인; 실제 모델/DB는 열지 않음
python tools/check_environment.py
# --apply 없는 setup_db는 설명만 출력
python tools/setup_db.py
# GPU 모델을 준비하고 d27_rag Schema에 24개 청크 Embedding·저장
python tools/setup_db.py --apply
```

`intfloat/multilingual-e5-small`은 384차원이며, **query: / passage: Prefix**, `normalize_embeddings=True`를 유지합니다. 모델 revision/차원/정규화·최대 Token 길이 계약이 다르면 저장 벡터를 재사용하지 않습니다.

`d27_rag`는 Day27 전용 Schema입니다. Day26과 이전 수업 DB를 삭제하지 않습니다. 저장은 Transaction으로 묶고 재실행 시 기존 chunk_id의 citation_id를 보존합니다.

```sql
SELECT COUNT(*) FROM d27_rag.rag_chunks;
SELECT chunk_id, ready, is_current FROM d27_rag.rag_chunks ORDER BY chunk_id LIMIT 10;
```

## 7. Cross-Encoder GPU 준비

모델 `BAAI/bge-reranker-v2-m3`는 처음 실행 시 Hugging Face에서 다운로드할 수 있습니다. 실제 설치된 PyTorch가 CUDA를 지원해야 합니다.

```bash
python -c "from coursekit.config import require_cuda; print(require_cuda())"
```

VRAM 부족 시 다른 프로그램의 GPU 점유량을 확인하고, 동시에 여러 모델을 중복 로드하지 마세요. 제공 Reranker의 작은 Batch Size부터 시작하십시오. **CPU Fallback은 자동으로 실행하지 않습니다.**

## 8. 실습 실행

```bash
# 설치 검증을 위한 외부 호출 없는 예시
python 01_basic/01_failure_diagnosis/main.py --offline
python 01_basic/05_cross_encoder_reranking/main.py --offline
# TODO 완성 후 라이브 연결
python 01_basic/02_query_rewrite/main.py
python 01_basic/04_candidate_retrieval/main.py
python 01_basic/05_cross_encoder_reranking/main.py
python 01_basic/08_enhanced_rag_api/main.py
```

- `--offline`: 고정 Retrieval 순위·고정 Rerank 점수·고정 Rewrite·고정 답변. **실제 성능 아님**
- `--offline` 없이: 실제 API·GPU·DB·모델 호출. LLM API 비용 발생 가능
- `outputs/day27_XX_live.json`: 실제 실행의 후보·점수·출처·오류 기록
- 각 실습의 `expected/EXPECTED.md`, `reports/review.md`를 확인합니다.

## 9. 흔한 오류

| 현상 | 원인/확인 |
|---|---|
| `ModuleNotFoundError` | VS Code Interpreter가 `.venv`인지, `python -m pip list` 확인 |
| `CUDA GPU를 사용할 수 없습니다` | PyTorch CPU Build, Driver, 다른 venv, GPU 비활성화 점검 |
| `torch.cuda.OutOfMemoryError` | 모델 중복 로드/Batch Size/다른 GPU 작업 점검 |
| `psycopg.OperationalError` | DB 실행 여부·호스트·포트·암호·DB 이름 확인 |
| `extension "vector" is not available` | **서버** pgvector 설치 필요; Python Adapter와 별개 |
| `embedding_contract 불일치` | 모델·Revision·차원·Prefix를 동일하게 설정하거나 새 Schema 생성 |
| `AuthenticationError` | 유효한 API Key, 현재 모델 권한, 환경변수 확인 |
| `RateLimitError` | 사용량·요청 속도 제한, 재시도·비용 정책 확인 |
| 출처 ID 불일치 | 이번 Context included_ids만 인용하도록 검사, DB ID는 Fixture와 다를 수 있음 |
| 입력 부족인데 답변 생성 | Context의 원문 확인, Grounding은 인간 평가 필요 |

## 10. 안전 및 제출

`LLM_MODEL`, Key의 **존재 여부**만 점검하고 비밀 값은 로그에 남기지 않습니다. 사용자가 보낸 `role=staff`는 서버의 권한이 아닙니다. 평가용 Gold Label은 검색 함수에 전달하지 않습니다. 학습 결과와 실행 모드를 `reports/review.md`에 기록하십시오.
