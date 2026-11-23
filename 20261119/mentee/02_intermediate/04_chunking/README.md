# 실습 04 · 문서별 Chunking·E5 Token 길이

**난이도:** 02_intermediate · **용도:** 수강생 TODO

## 목표
두 문서를 독립적으로 분할하고 실제 E5 Tokenizer의 입력 길이 계약을 확인합니다.

## 먼저 알아야 할 용어
- **Chunk Size**: 정제 본문에 적용하는 문자 길이
- **Token Count**: 모델 Tokenizer가 계산한 입력 단위
- **E5 passage prefix**: 본문 인코딩 입력의 일부

## 구현할 TODO

| ID | 요구사항 |
|---|---|
| `D24-04-I01` | 하나의 ParsedUnit을 clean_text에서 문자 창으로 분할합니다. |
| `D24-04-I02` | 각 창에 doc_id·unit_id·버전·Locator와 passage: 접두어를 전달합니다. |
| `D24-04-I03` | SentenceTransformer 모델이 주어졌을 때 특수 토큰 포함 길이를 측정합니다. 모델이 없으면 not_run으로 기록합니다. |
| `D24-04-I04` | 최대 입력 길이를 초과한 청크를 통과시키지 않고 개수와 ID를 기록합니다. |

## 실행 방법
- 수정 대상: `tasks.py`. `main.py`는 실행 진입점입니다.
- VS Code의 **Git Bash**에서 이 폴더로 이동하여 실행합니다. 기존 Python 가상환경을 사용합니다.
- `python main.py`
- 선택 실행: `python main.py --live-e5` (모델 다운로드·실제 Tokenizer 길이 측정).
- 옵션이 없을 때 Token 측정값은 `not_run`으로 표시합니다.

## 완료 기준
기본: Token not_run(가짜 길이 금지). --live-e5: 실제 tokenizer로 Token 길이 확인.

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
