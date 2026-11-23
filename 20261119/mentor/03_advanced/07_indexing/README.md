# 실습 07 · pgvector 안전한 갱신·실패 복구

**난이도:** 03_advanced · **용도:** 강사용 정답·해설

## 목표
E5 Embedding을 DB 변경 전에 완료하고 Stage/Publish Transaction의 원자성을 검증합니다.

## 먼저 알아야 할 용어
- **UPSERT**: 같은 키의 삽입·갱신 전략
- **Stage/Publish**: 준비와 검색 공개 분리
- **Rollback**: Transaction 실패 시 변경 취소
- **Version Pointer**: 현재 검색에 보이는 원문·처리 판

## 구현할 TODO

| ID | 요구사항 |
|---|---|
| `D24-07-A01` | DOC-ATTEND v1·v2를 동일한 Markdown Parser로 처리하고, 문서 ID·원문 버전·처리 설정을 보존합니다. |
| `D24-07-A02` | E5 passage Embedding을 DB Transaction 전에 계산·검증합니다. |
| `D24-07-A03` | 벡터·원문·출처를 새 버전으로 Stage하고 ID 충돌을 검사합니다. |
| `D24-07-A04` | 현재 문서의 공개 포인터(source_version, pipeline_version)를 조회합니다. Publish는 A06에서 처리합니다. |
| `D24-07-A05` | 강제로 예외를 발생시킨 Transaction에서 Rollback 후 현재 포인터가 유지되는지 확인합니다. |
| `D24-07-A06` | v2를 짧은 Transaction에서 Publish하고, 정확 검색에서 이전 v1 청크가 제외되는지 확인합니다. |

## 실행 방법
- 수정 대상: `tasks.py`. `main.py`는 실행 진입점입니다.
- VS Code의 **Git Bash**에서 이 폴더로 이동하여 실행합니다. 기존 Python 가상환경을 사용합니다.
- `python main.py`
- 추가 실행: `python main.py --live-db` (PostgreSQL 18.6 + pgvector + E5 + `.env` 준비 시에만).
- DB 없는 기본 실행은 `prepared_only_not_db` 또는 `not_run`이며, DB 성공을 의미하지 않습니다.

## 완료 기준
실제 DB 미연결 기본 표기 not_run. --live-db 시 v1 공개→v2 Stage→의도적 Rollback→v2 재공개·검색 검증.

## 독립 실습과 결과
- 앞 교시가 미완성이어도 현재 폴더의 준비 코드와 `coursekit/` Checkpoint로 시작할 수 있습니다.
- 출력 파일은 해당 폴더의 `outputs/`에 생성됩니다. `data/raw/` 원문은 수정하지 않습니다.
- `expected/EXPECTED.md`는 평가 기준이지 실제 실행 로그가 아닙니다.
- 수강생은 실행 결과 외에 “어느 원문·어느 처리 버전·어느 실패 지점인가?”를 설명해야 합니다.

## 현업 연결 / 한계
- 제공된 `parse_markdown_units()`는 제목·절 경계가 정해진 **수업용 Markdown Parser**입니다. Code Fence·중첩 Block 등 모든 Markdown 구문을 처리하는 범용 Parser는 아닙니다.
- v1·v2는 모두 두 절(`sec-1`, `sec-2`)입니다. 이번 회귀 검사는 **이전 공개 버전의 청크 제외**를 확인하며 청크 수 감소를 검증하는 시나리오는 아닙니다.
- 이 실습은 **11월 19일 독립 HTML 강의자료**와 본 폴더의 설명·코드만으로 진행할 수 있습니다.
- Chunking Coverage 100%는 파싱 전에 원문이 온전했음을 보장하지 않습니다.
- Parsing/Embedding/DB 검색은 서로 다른 단계이며, 결과가 `not_run`이면 실제 성공으로 기록하지 않습니다.

## 강사 해설 포인트
1. 원본과 정제 텍스트, 청크 본문, 검색 결과를 서로 다른 데이터로 구분하여 설명합니다.
2. TODO ID의 BEGIN~END 블록에 완성 코드와 근거 주석이 있습니다. 학생 코드와 동일한 함수 이름을 사용합니다.
3. 정상 예제 이후 빈 결과·잘못된 ID·잘못된 출처의 반례를 직접 제시합니다.
4. 숫자·부정 표현·버전이 삭제되면 임베딩/LLM만으로 자동 복구하지 못합니다.
5. 실제 DB 검증을 수행하지 않은 경우 `fixture`와 `not_run`을 명확히 구분합니다.

## 자동 검사

```bash
python -m pytest -q tests
```
이 테스트는 작은 정상·오류 계약을 확인합니다. 특히 07·08은 별도 `--live-db` 실행 없이 PostgreSQL 사용 성공을 보증하지 않습니다.
