# 실습 04 · Structure-aware Chunking · 입력 계약

**난이도:** 03_advanced · **용도:** 수강생 TODO

## 목표
제목·문단 경계를 먼저 고려하고 E5 입력 길이와 원문 Offset을 함께 검증합니다.

## 먼저 알아야 할 용어
- **Structure-aware**: 문서 제목·문단 경계를 먼저 고려하는 분할
- **Offset**: clean_text 문자 위치
- **Rechunk**: 너무 긴 청크의 재분할
- **Token Budget**: 모델 특수 토큰 포함 입력 길이

## 구현할 TODO

| ID | 요구사항 |
|---|---|
| `D24-04-A01` | 문단 경계 후보를 찾아 원문 구간을 정확히 추출합니다. |
| `D24-04-A02` | 긴 문단만 문자 창으로 재분할하며 짧은 문단은 그대로 유지합니다. |
| `D24-04-A03` | 각 Span을 doc_id·unit_id·source_locator에 연결해 Chunk를 만듭니다. |
| `D24-04-A04` | 본문과 선택적 제목을 합쳐 `passage: ` 입력을 만들고 Offset과 분리합니다. |
| `D24-04-A05` | 모델이 제공되면 Tokenizer로 길이를 측정하고 초과 결과를 격리합니다. |
| `D24-04-A06` | 동일 원문·설정의 재실행에서 Chunk ID·본문·문자 범위가 동일한지 검사합니다. |

## 실행 방법
- 수정 대상: `tasks.py`. `main.py`는 실행 진입점입니다.
- VS Code의 **Git Bash**에서 이 폴더로 이동하여 실행합니다. 기존 Python 가상환경을 사용합니다.
- `python main.py`
- 선택 실행: `python main.py --live-e5` (모델 다운로드·실제 Tokenizer 길이 측정).
- 옵션이 없을 때 Token 측정값은 `not_run`으로 표시합니다.

## 완료 기준
Title/Body/Span 분리, 재실행 일관; Token 길이는 --live-e5에서만 실제 측정.

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
