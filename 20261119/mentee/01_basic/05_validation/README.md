# 실습 05 · Chunk Validation · Span

**난이도:** 01_basic · **용도:** 수강생 TODO

## 목표
생성된 청크가 정제 본문의 정확한 문자 구간인지 검사합니다.

## 먼저 알아야 할 용어
- **Span**: clean_text의 [시작,끝) 범위
- **Validation**: 계약에 맞는지 검사
- **Coverage**: 검사 대상 구간 중 한 번 이상 포함된 비율

## 구현할 TODO

| ID | 요구사항 |
|---|---|
| `D24-05-B01` | 범위 0 <= start < end <= len(clean_text)를 검사합니다. |
| `D24-05-B02` | chunk.text와 clean_text[start:end]가 같고 공백만 있는 청크가 아닌지 검사합니다. |

## 실행 방법
- 수정 대상: `main.py`. `main.py`는 실행 진입점입니다.
- VS Code의 **Git Bash**에서 이 폴더로 이동하여 실행합니다. 기존 Python 가상환경을 사용합니다.
- `python main.py`

## 완료 기준
정상 Chunk 통과, 문자열 불일치 Chunk 실패, 빈 본문/범위 오류도 구분.

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
