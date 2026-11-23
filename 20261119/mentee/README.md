# 수강생용 (mentee)

# Day24 · Document Parsing · Chunking · Indexing 실습

**2026-11-19(목) · 생성형 AI·LLM 및 RAG 엔지니어링 8/18 · 8개 실습**

이 패키지는 **11월 19일 HTML 강의자료를 기반으로 완결되는 독립 실습자료**입니다. 다른 참고 파일을 별도로 열 필요 없이 진행할 수 있습니다. 원문·출처·벡터와 검증 상태를 연결하여 11월 20일 Basic RAG에 필요한 문서 인덱싱 데이터를 준비합니다.

## 진행 방식

한 번에 **한 수준만** 선택하세요. 앞선 교시의 구현을 마치지 않았어도 현재 실습에 준비된 `coursekit/` Checkpoint로 시작할 수 있습니다.

| 실습 | 주요 목표 | 실제 데이터·핵심 용어 |
|---|---|---|
| 01. Collection | 원본·Manifest·해시 | bytes, SHA-256, source_version |
| 02. Parsing | 형식별 텍스트·구조 추출 | UTF-8, TXT, Markdown, HTML, PDF, OCR |
| 03. Cleaning | 의미 보존·변경 기록 | CRLF, NFC, NFKC, clean_hash |
| 04. Chunking | 크기·Overlap·Offset | Chunk Size, `passage: `, Tokenizer |
| 05. Validation | Span·누락·중복 검사 | Coverage, Gap, Quarantine |
| 06. Metadata | 출처·필터·버전 | Locator, pipeline_version, Citation Mapping |
| 07. pgvector Indexing | E5·저장·검색 | E5-small, Vector(384), Stage/Publish, Transaction |
| 08. Daily Project | 전체 Ingestion 연결 | Report, 재실행, 버전 갱신·복구 |

### 세 난이도

| 폴더 | TODO 총개수 | 8개 실습당 | 프로젝트 구조 |
|---|---:|---|---|
| `01_basic` | 16개 | 각각 2개 | 실습 폴더의 `main.py` 1개가 중심 |
| `02_intermediate` | 32개 | 각각 4개 | `main.py` 실행 / `tasks.py` 구현 분리 |
| `03_advanced` | 48개 | 각각 6개 | 역할별 함수·테스트·계약·DB 스키마 관리 |

**TODO 개수는 하나의 구현 목표를 세는 단위입니다.** 한 TODO 안의 주석에서 입력·출력·검사 조건을 구체적으로 제시합니다. Level을 올리기 위해 의미 없는 클래스나 파일을 추가하지 않습니다.

## Windows 11 · VS Code · Git Bash 실행

1. ZIP을 풀고 **mentee** 또는 **mentor** 폴더를 VS Code로 엽니다. ZIP 내부에서 실행하지 않습니다.
2. 기존에 사용 중인 **동일 Python 가상환경**을 선택합니다. 새 venv를 만들지 않습니다.
3. VS Code의 **Git Bash** Terminal에서 다음을 실행합니다.

```bash
python -c "import sys; print(sys.executable)"
python tools/check_environment.py
python -m pip show pypdf beautifulsoup4
# 설치되지 않은 기본 패키지가 있을 때만:
python -m pip install -r requirements_base.txt
```

실습 폴더로 이동하여 실행합니다.

```bash
cd 01_basic/01_collection
python main.py
python -m pytest -q tests
```

- `mentee`는 TODO가 남아 있으므로 `NotImplementedError`로 멈추는 것이 **정상적인 시작 상태**입니다.
- `mentor`는 해당 TODO의 정답과 해설을 담고 있습니다.
- Python을 IDE에서 바꾼 경우 `python` 명령의 실제 실행 경로부터 다시 확인합니다.
- 결과 JSON은 각 실습의 `outputs/`에 생성되며, `expected/EXPECTED.md`와 대조합니다.
- 자동 테스트가 없다면 `python -m pip install -r requirements_test.txt`로 `pytest`를 추가합니다.

## 실제 Embedding·PostgreSQL 실행 (07·08 중 해당하는 실습)

**로컬 기본 실행과 실제 DB·모델 실행은 엄격히 구분합니다.**

- `python main.py` → 구조·정제·검증·수집 예제를 실행하되, E5·DB 미실행은 `not_run`으로 기록
- `python main.py --live-e5` → 실습 04 Intermediate/Advanced에서 **실제** E5 Tokenizer 길이 검사
- `python main.py --live-db` → 실습 07 전 수준 및 08 Advanced에서 **실제** E5/pgvector 저장·검색

실제 실행에 필요한 패키지가 없는 경우에만 다음을 검토합니다.

```bash
python -m pip show sentence-transformers psycopg pgvector python-dotenv
python -m pip install -r requirements_live.txt
```

기존 `sentence-transformers`와 PyTorch가 정상 작동하면 불필요한 재설치는 하지 않습니다. 기본 실행에는 OpenAI API Key가 필요하지 않습니다.

- PostgreSQL **18.6 x64**는 Windows 11에 이미 설치되어 있다고 가정합니다.
- 사용할 DB에서 pgvector 서버 확장 설치와 `CREATE EXTENSION IF NOT EXISTS vector`가 완료되어야 합니다. `pip install pgvector`는 서버 확장을 설치하지 않습니다.
- `.env.example`을 복사해 폴더 루트에 `.env`를 만들고 **본인 DB 계정·비밀번호**만 입력합니다. `.env`는 Git에 올리지 않습니다.
- 실제 DB 준비: `python tools/setup_db.py --apply` (강사 확인 후 실행). 수업용 전용 Schema `d24_basic07`, `d24_inter07`, `d24_adv07`, `d24_adv08`만 만들며 기존 수업 테이블을 삭제하지 않습니다.
- 권한 때문에 새 Schema를 생성할 수 없다면 해당 DB 관리자에게 Schema 생성 권한을 문의합니다. 인증 정책을 완화하거나 슈퍼유저 비밀번호를 코드에 하드코딩하지 않습니다.
- 예제는 Exact Top-k (`<=>`)를 사용합니다. 작은 문서에서 HNSW 최적화나 속도 측정값을 지어내지 않습니다.

### E5 모델의 입력 계약

- 모델: `intfloat/multilingual-e5-small`, 차원: **384**
- 질의 입력: `query: 사용자 질문`
- 문서 청크 입력: `passage: 청크 본문`
- `normalize_embeddings=True`; 모델·revision·Tokenizer·Input Prefix를 바꾸면 재임베딩 필요 여부를 검토해야 합니다.
- Token 길이 검사는 실제 모델에 전달할 전체 문자열을 같은 Tokenizer로 확인합니다. `model.max_seq_length`를 확인하고 `truncation=False`로 길이를 검사합니다.
- 이 강의에서 수치로 보이는 **71자 또는 20자 예제는 문자 계산용 Fixture**입니다. 실제 모델 Token 개수를 뜻하지 않습니다.

## 제공 문서와 상태

| 원문 | 상태 | 목적 |
|---|---|---|
| DOC-ATTEND · `attendance.md` | Parsing 가능 | 제목·문단·숫자·조건 유지 |
| DOC-ASSIGN · `assignment.txt` | Parsing 가능 | UTF-8, 일반 문단 |
| DOC-FACILITY · `facility.html` | Parsing 가능 | `main`과 표, nav·script 제외 |
| DOC-CAREER · `career.pdf` | Parsing 가능 | 텍스트층이 있는 **2페이지 PDF** |
| DOC-SCAN · `scan.pdf` | `needs_ocr` | 텍스트층 없는 이미지 PDF |
| DOC-UNSUPPORTED · `unsupported.xyz` | `unsupported` | 지원하지 않는 파일 누락 방지 |

본 패키지의 가상 교육센터 데이터입니다. 실제 기관의 출석·상담 규정이 아닙니다. 6건 중 5건이 지원하는 형식이며 그중 4건은 텍스트 파싱이 가능합니다. 샘플 이미지 PDF는 OCR을 실제 실행하지 않습니다.

## 파일과 결과의 출처

- `data/raw/`: 변경하지 않는 원문 파일. `data/versions/attendance_v2.md`는 개정본.
- `coursekit/`: 제공된 Checkpoint와 DB·모델 연결 도구. 실습 TODO의 정답을 감추기 위한 모듈이 아니라 진도 차이를 해소하기 위한 공통 환경입니다.
- `expected/EXPECTED.md`: 기대하는 조건과 위험 사례. `offline_reference_*.json`: mentor의 **DB 미접속** 기본 실행 결과. 검색 모델의 실제 정답 순위가 아닙니다.
- `outputs/`: 실행 중 생성. `.gitignore`로 제외되며 제출에는 필요한 결과 파일만 선택하여 사용합니다.
- `tests/test_exercise.py`: TODO가 정확한 입력·출력 계약을 따르는지 검사하는 작은 테스트입니다. 멘티의 미완성 TODO는 통과할 수 없습니다.

**강의에서 가장 중요한 판단:** 문서가 저장됐다는 사실과 문서의 모든 내용이 보존됐다는 사실은 다릅니다. Coverage 100%도 clean_text 기준의 검사이며 원본 PDF 전체의 정보 추출을 보증하지 않습니다. 검색 결과의 Citation은 원문 ID·버전·위치와 연결해 직접 대조해야 합니다.

## 시작할 때

- 자신에게 맞는 수준 하나를 선택하고 `README.md`의 TODO와 `expected/`를 대조합니다.
- 정답을 단순 복사하지 않고 각 코드가 처리하는 입력·출력과 실패 원인을 설명합니다.
