# Day23 · Embedding · pgvector (수강생용 TODO)

- 날짜: 2026-11-18 (수), HTML 강의자료 80개 화면 / 실습 01~08.
- 기준: Windows 11, 기존 PostgreSQL 18.6, 기존 Python 가상환경, VS Code / Git Bash. Docker·WSL 불필요.
- E5: `intfloat/multilingual-e5-small`, `query: ` / `passage: `, 정규화, 384차원.
- 자료: `common/data/knowledge_search_v2.json` (101~109, 기존 101~103 원문 유지).
- SQL: 기존 knowledge 테이블 변경 금지, `day23_search_docs`에서만 작업.
- 최종 과제: GPT 생성이 아니라 검색 후보 ID·제목·본문·거리 반환.

## 처음 실행

VS Code에서 이 `mentee` 폴더를 열고 **기존 인터프리터**를 선택합니다.

```bash
python -c "import sys; print(sys.executable)"
python -m pip show numpy sentence-transformers psycopg pgvector python-dotenv
# 누락된 패키지만 설치합니다. 기존 torch·venv 일괄 --upgrade 금지.
python 01_basic/01_knowledge/main.py --mode fixture
python 01_basic/02_similarity/main.py --mode fixture
```

`NotImplementedError: TODO ...`가 표시되는 것은 정상입니다. 명시된 요구사항을 직접 작성한 다음 다시 실행하세요.

## 폴더

- `01_basic`: 실습마다 **3개의 핵심 TODO**, `main.py` 단일 진입 파일 중심.
- `02_intermediate`: 실습마다 **5개의 TODO**, `main.py`와 `tasks.py`로 책임 분리.
- `03_advanced`: 실습마다 **6개의 TODO**, `main.py` + 실습별 `app/` 도메인 모듈 2개; 검증·연산·검색 등 이유가 명확한 기능만 분리.
- `common`: 배포 가능한 공통 교실 코드, **이미 구현된 입출력 스캐폴딩**. TODO 정답을 대신하지 않습니다.
- `docs/WINDOWS_PGVECTOR_SETUP.md`: pgAdmin·Native Tools CMD·VS Code를 어디서 사용할지 단계별 안내.
- `docs/COMMANDS.md`: 실습 01~08 실행 순서·실제 DB 테스트 절차.
- `docs/HTML_ALIGNMENT.md`: HTML과 코드의 일치표.

## 두 실행 경로를 혼동하지 마세요

`--mode fixture`는 E5 벡터나 DB 점수를 **만들어냈다고 주장하지 않는 모의 경로**입니다.
`--mode live`는 03의 실제 E5 로드, 04의 실제 DB 연결, 05~08의 실제 PostgreSQL 검색을 수행할 때만 지정합니다.
실제 모델을 최초 로드하는 경우 네트워크 다운로드가 발생할 수 있고, 서버 확장은 설치되어 있어야 합니다.

비밀번호가 들어 있는 `.env`는 실습별 `main.py` 바로 옆에 저장하며 제출하지 않습니다.
실행 결과는 각 실습의 `outputs/exercise_XX.json`로 저장됩니다.
