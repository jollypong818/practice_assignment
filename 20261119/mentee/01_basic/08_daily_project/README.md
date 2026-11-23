# 실습 08 · Daily Project · 문서 한 건 끝까지

**난이도:** 01_basic · **용도:** 수강생 TODO

## 목표
앞선 단계의 제공 체크포인트로 TXT를 Parsing → Cleaning → Chunking → Validation 합니다.

## 먼저 알아야 할 용어
- **Pipeline**: 여러 처리 단계의 입력·출력 연결
- **Checkpoint**: 이전 단원 미완료를 보완하는 제공 구현
- **Report**: 수집·검증 상태를 기록한 결과

## 구현할 TODO

| ID | 요구사항 |
|---|---|
| `D24-08-B01` | DOC-ASSIGN의 Parsing 결과를 읽어 정제하고 110자/15자 설정으로 청크를 만듭니다. |
| `D24-08-B02` | 원문 ID·Chunk 수·Span 일치 여부를 기록하고 문제가 있으면 성공으로 처리하지 않습니다. |

## 실행 방법
- 수정 대상: `main.py`. `main.py`는 실행 진입점입니다.
- VS Code의 **Git Bash**에서 이 폴더로 이동하여 실행합니다. 기존 Python 가상환경을 사용합니다.
- `python main.py`

## 완료 기준
DOC-ASSIGN 원문·정제·청크 ID 연결, status=prepared_not_embedded. 실제 DB 저장이라고 표시하지 않음.

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
