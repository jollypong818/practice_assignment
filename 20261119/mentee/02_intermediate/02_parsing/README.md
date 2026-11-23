# 실습 02 · 형식별 Parsing

**난이도:** 02_intermediate · **용도:** 수강생 TODO

## 목표
TXT·Markdown·HTML·PDF를 공통 ParsedUnit 구조로 변환하고 비정상 상태를 구분합니다.

## 먼저 알아야 할 용어
- **TXT**: 일반 텍스트
- **Markdown**: 제목·문단을 가진 경량 마크업
- **HTML**: main·table 등 구조
- **PDF**: 페이지별 추출; OCR과 다름

## 구현할 TODO

| ID | 요구사항 |
|---|---|
| `D24-02-I01` | 파일 확장자로 파서 경로를 결정합니다. 미지원 확장자를 정상 취급하지 않습니다. |
| `D24-02-I02` | TXT를 UTF-8로 읽고 오류와 빈 결과를 구분합니다. |
| `D24-02-I03` | Markdown·HTML에서 제목·본문·표의 구조를 가진 ParsedUnit을 추출합니다. |
| `D24-02-I04` | PDF는 페이지별 위치를 기록하고 이미지 PDF는 별도 needs_ocr로 분류합니다. |

## 실행 방법
- 수정 대상: `tasks.py`. `main.py`는 실행 진입점입니다.
- VS Code의 **Git Bash**에서 이 폴더로 이동하여 실행합니다. 기존 Python 가상환경을 사용합니다.
- `python main.py`

## 완료 기준
상태: parsed 4, needs_ocr 1, unsupported 1. HTML 메뉴·script는 실제 본문에서 제외.

## 독립 실습과 결과
- 앞 교시가 미완성이어도 현재 폴더의 준비 코드와 `coursekit/` Checkpoint로 시작할 수 있습니다.
- 출력 파일은 해당 폴더의 `outputs/`에 생성됩니다. `data/raw/` 원문은 수정하지 않습니다.
- `expected/EXPECTED.md`는 평가 기준이지 실제 실행 로그가 아닙니다.
- 수강생은 실행 결과 외에 “어느 원문·어느 처리 버전·어느 실패 지점인가?”를 설명해야 합니다.

## 현업 연결 / 한계
- 이 실습은 **11월 19일 독립 HTML 강의자료**와 본 폴더의 설명·코드만으로 진행할 수 있습니다.
- Chunking Coverage 100%는 파싱 전에 원문이 온전했음을 보장하지 않습니다.
- Parsing/Embedding/DB 검색은 서로 다른 단계이며, 결과가 `not_run`이면 실제 성공으로 기록하지 않습니다.

## 자동 검사

```bash
python -m pytest -q tests
```
이 테스트는 작은 정상·오류 계약을 확인합니다. 특히 07·08은 별도 `--live-db` 실행 없이 PostgreSQL 사용 성공을 보증하지 않습니다.
