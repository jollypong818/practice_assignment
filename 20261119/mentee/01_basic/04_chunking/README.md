# 실습 04 · Chunking · Size와 Overlap

**난이도:** 01_basic · **용도:** 수강생 TODO

## 목표
문자 범위 [start,end)와 종료 조건을 직접 구현합니다.

## 먼저 알아야 할 용어
- **Chunk Size**: 한 청크의 최대 길이
- **Overlap**: 인접 청크가 공유하는 범위
- **[start,end)**: 시작 포함·끝 제외의 문자 범위

## 구현할 TODO

| ID | 요구사항 |
|---|---|
| `D24-04-B01` | size와 overlap을 정수로 검사하고 0 <= overlap < size를 보장합니다. |
| `D24-04-B02` | start·end·text가 있는 Chunk 목록을 만들고 본문 끝에 닿으면 종료합니다. |

## 실행 방법
- 수정 대상: `main.py`. `main.py`는 실행 진입점입니다.
- VS Code의 **Git Bash**에서 이 폴더로 이동하여 실행합니다. 기존 Python 가상환경을 사용합니다.
- `python main.py`

## 완료 기준
71자 가상 입력에서 [0,40), [30,70), [60,71). 실제 E5 Token 수가 아닌 문자 수.

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
