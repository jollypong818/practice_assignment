# Day23 · Windows 11 PostgreSQL 18.6 및 pgvector 0.8.7

**기준**: 11/18 HTML 강의자료 4교시. Docker·WSL 사용하지 않음. 이미 설치한 PostgreSQL과 수업용 Python 가상환경을 유지합니다.
관리자 권한이나 C++ Build Tools 설치가 기관 정책으로 차단되면 강사/관리자에게 요청하고, 기존 DB를 삭제하거나 보안 기능을 해제하지 마세요.

## 0. 명령어를 실행하는 프로그램 3개

- **pgAdmin Query Tool**: 서버 버전·DB·CREATE EXTENSION·SQL 검사
- **x64 Native Tools Command Prompt for VS(관리자)**: C/C++ pgvector 서버 확장 빌드/설치
- **VS Code Git Bash(기존 Python 인터프리터)**: Python 패키지·실습 `main.py`

`.venv`는 실행 환경, `.env`는 비밀번호 등의 설정 파일입니다. 새 가상환경·Docker 컨테이너를 만들지 마세요.

## 1. pgAdmin에서 사전 확인

```sql
SELECT version();
SELECT current_database(), current_user;
SELECT name, default_version, installed_version
FROM pg_available_extensions WHERE name='vector';
```

`vector` 행이 없으면 PostgreSQL 서버 확장이 아직 제공되지 않은 상태입니다. `installed_version=NULL`은 해당 DB에서 활성화되지 않은 상태입니다. 현재 접속한 DB를 기록하세요.

## 2. VS Code가 아닌 Visual Studio Build Tools 준비

Microsoft 공식 Visual Studio Build Tools에서 **Desktop development with C++**, MSVC x64/x86, Windows SDK 설치를 확인합니다. VS Code 설치와 별개입니다. 이전 설치가 완료됐다면 재설치하지 않습니다.

공식: https://visualstudio.microsoft.com/downloads/

## 3. x64 Native Tools CMD를 관리자 권한으로 열기

아래부터 **CMD**입니다. Git Bash/PowerShell에서 CMD의 `set`과 `nmake`를 그대로 실행하지 않습니다.

```cmd
where cl
where nmake
where git
echo %VSCMD_ARG_TGT_ARCH%
"C:\Program Files\PostgreSQL\18\bin\pg_config.exe" --version
set "PGROOT=C:\Program Files\PostgreSQL\18"
echo %PGROOT%
dir "%PGROOT%\include\server\postgres.h"
dir "%PGROOT%\lib\postgres.lib"
```

확인값: x64, PostgreSQL 18.6, 헤더·라이브러리 실제 존재. 실패하면 `nmake`를 시작하지 않습니다.

## 4. 공식 pgvector 소스 고정 및 빌드

```cmd
if not exist C:\pgvector-build mkdir C:\pgvector-build
cd /d C:\pgvector-build
git clone --branch v0.8.7 --depth 1 https://github.com/pgvector/pgvector.git
cd pgvector
git describe --tags --exact-match
dir Makefile.win
nmake /F Makefile.win
```

**중요**: 이미 `C:\pgvector-build\pgvector` 폴더가 있으면 새로 clone하지 말고 버전을 확인합니다. `nmake` 실패 후에는 설치하지 않습니다.

## 5. 서버 확장 파일 설치 (CMD 관리자)

```cmd
nmake /F Makefile.win install
dir "%PGROOT%\lib\vector.dll"
dir "%PGROOT%\share\extension\vector.control"
dir "%PGROOT%\share\extension\vector--*.sql"
```

이것은 서버의 DLL/control/SQL 파일 설치입니다. 아직 개별 DB에서 활성화한 것은 아닙니다.

## 6. pgAdmin → 정확한 수업 DB에서 활성화

```sql
SELECT current_database();
SELECT name,default_version,installed_version
FROM pg_available_extensions WHERE name='vector';
CREATE EXTENSION IF NOT EXISTS vector;
SELECT extname,extversion FROM pg_extension WHERE extname='vector';
SELECT
 '[1,0,0]'::vector <=> '[1,0,0]'::vector AS same_direction,
 '[1,0,0]'::vector <=> '[0,1,0]'::vector AS perpendicular,
 '[1,0,0]'::vector <=> '[-1,0,0]'::vector AS opposite_direction;
```

기대 거리 0 / 1 / 2. 실패한 트랜잭션이 열린 상태라면 **본인의 미확정 작업을 확인한 뒤** 필요시 `ROLLBACK;`을 실행합니다.

원본 knowledge 테이블과 다른 별도 임시 검사(필요한 경우):

```sql
BEGIN;
CREATE TEMP TABLE day23_vector_check (
 id integer PRIMARY KEY,label text NOT NULL,embedding vector(3) NOT NULL
) ON COMMIT DROP;
INSERT INTO day23_vector_check VALUES
 (1,'같은 방향','[1,0,0]'),(2,'가까운 방향','[0.8,0.6,0]'),(3,'직각','[0,1,0]');
SELECT id,label,embedding <=> '[1,0,0]'::vector AS distance
FROM day23_vector_check
ORDER BY embedding <=> '[1,0,0]'::vector ASC LIMIT 3;
COMMIT;
```

기대 ID: 1→2→3. 임시 테이블은 COMMIT 때 삭제됩니다.

## 7. VS Code / 기존 Python / Git Bash로 복귀

```bash
python -c "import sys; print(sys.executable)"
python -m pip show numpy sentence-transformers psycopg pgvector python-dotenv
# 없는 패키지에 한해서만 설치합니다. 아래는 예시이며 환경을 통째로 --upgrade 하지 않습니다.
python -m pip install pgvector
python -m pip install 'psycopg[binary]' python-dotenv
python -m pip install sentence-transformers
python -m pip check
```

모델 `intfloat/multilingual-e5-small` 최초 로드는 다운로드가 필요할 수 있습니다. CPU로 실행합니다. 384차원, `query:`/`passage:` 접두어, normalize=True를 모두 적용합니다.

## 8. 실습별 `.env`와 실제 연결

`04_pgvector_setup/main.py` 옆 `.env.example`을 `.env`로 **복사**하고 본인의 PostgreSQL 비밀번호를 입력합니다. 05~08의 DB 실습도 각 폴더에 별도의 `.env`를 복사합니다. Git에 `.env`를 올리지 않습니다.

```ini
PGHOST=127.0.0.1
PGPORT=5432
PGDATABASE=knowledge_lab
PGUSER=본인_DB계정
PGPASSWORD=본인_DB비밀번호
```

`knowledge_lab`은 HTML 예시이므로 **pgAdmin에서 조회한 실제 current_database()**로 교체합니다. 각 실습의 `.env`는 `main.py` 위치를 기준으로 읽으며 OS의 이전 `PG*` 값을 몰래 우선 적용하지 않습니다.

## 9. 재현 확인 및 순서

1. 먼저 `python main.py --mode fixture`로 TODO와 구조를 확인합니다. 이 결과는 **E5/DB 실측이 아닙니다**.
2. 03 `--mode live`: 실제 E5 모델 로드/384차원 확인.
3. 04 `--mode live`: 실제 PG 버전/확장 상태/수치 거리 확인.
4. 05 `--mode live`: 실제 E5 9건 → 새 테이블 `day23_search_docs` 저장·Top-k.
5. 06 `--mode live`: 실행 계획 확인. 인덱스 생성은 명시적인 `--create-index`가 있을 때만.
6. 07·08 `--mode live`: 실측 검색·원문 확인 (11/20 RAG 전 단계).

실습 중 다른 DB 객체를 삭제하거나 기존 `knowledge` 테이블을 초기화하지 마세요. `09`나 다른 가상 문서를 만들지 않습니다.

## 오류별 위치

| 증상 | 우선 확인 |
|---|---|
| `cl`·`nmake` 없음 | x64 Native Tools CMD와 Build Tools의 C++ workload |
| `postgres.h` 없음 | PGROOT가 18의 최상위 경로인지, 개발 헤더 존재 여부 |
| `vector.control` 없음 | 서버 파일 nmake install 및 현재 사용 중인 PostgreSQL 설치 경로 |
| `extension vector is not available` | 서버 파일과 현재 DB 연결 서버 일치 |
| `type vector does not exist` | 정확한 DB의 CREATE EXTENSION 결과 |
| `ModuleNotFoundError` | VS Code Python 인터프리터와 pip 설치 대상 동일성 |
| `current transaction is aborted` | 원래 오류 확인 → 미확정 작업 검토 → ROLLBACK |
| `connection refused` | PostgreSQL 서비스·호스트·포트·DB 접속 설정 확인 |

**실습 HTML의 시뮬레이션과 Python의 `fixture` 실행은 설치 성공의 증거가 아닙니다.**
