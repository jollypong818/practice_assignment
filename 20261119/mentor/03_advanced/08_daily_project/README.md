# 실습 08 · Daily Project · 운영형 Ingestion

**난이도:** 03_advanced · **용도:** 강사용 정답·해설

## 목표
수집·Parsing·Cleaning·Validation·E5 Embedding·pgvector Publish를 연결하고 실패 후 회귀까지 검증합니다.

## 먼저 알아야 할 용어
- **Ingestion Report**: 파일별 단계·상태 결과
- **Model Contract**: 동일 E5/Tokenizer/Prefix/Normalization
- **Transactional Publish**: 검증된 버전만 공개
- **Citation ID**: DB 정수 출처

## 구현할 TODO

| ID | 요구사항 |
|---|---|
| `D24-08-A01` | Manifest의 빈 목록·중복 doc_id를 검사하고, unsupported 문서도 포함해 ID순 목록을 반환합니다. |
| `D24-08-A02` | Parsing·Cleaning·Chunking·Span 검사 후 정상 청크만 준비합니다. |
| `D24-08-A03` | main()이 한 번 로드한 E5 모델을 재사용해 문서별 passage 입력 길이·벡터 정규화를 검증합니다. |
| `D24-08-A04` | 각 문서를 분리된 Transaction에서 Stage하고 완성본만 Publish합니다. |
| `D24-08-A05` | v2에도 동일한 Markdown Parser를 적용하고, 실패·Rollback·정상 Publish 전후의 공개 포인터를 비교합니다. |
| `D24-08-A06` | 문서별 상태·청크 수를 기록하고, Live 실행 시에만 검색 결과·Citation ID·원문 Locator를 포함합니다. |

## 실행 방법
- 수정 대상: `tasks.py`. `main.py`는 실행 진입점입니다.
- VS Code의 **Git Bash**에서 이 폴더로 이동하여 실행합니다. 기존 Python 가상환경을 사용합니다.
- `python main.py`
- 추가 실행: `python main.py --live-db` (Advanced에서 실제 End-to-End 검증).

## 완료 기준
기본은 준비 결과, --live-db만 실제 E5+pgvector. 6건의 입력 상태·Citation ID·v2 실패/복구 기록.

## 독립 실습과 결과
- 앞 교시가 미완성이어도 현재 폴더의 준비 코드와 `coursekit/` Checkpoint로 시작할 수 있습니다.
- 출력 파일은 해당 폴더의 `outputs/`에 생성됩니다. `data/raw/` 원문은 수정하지 않습니다.
- `expected/EXPECTED.md`는 평가 기준이지 실제 실행 로그가 아닙니다.
- 수강생은 실행 결과 외에 “어느 원문·어느 처리 버전·어느 실패 지점인가?”를 설명해야 합니다.

## 현업 연결 / 한계
- 제공된 `parse_markdown_units()`는 제목·절 경계가 정해진 **수업용 Markdown Parser**입니다. Code Fence·중첩 Block 등 모든 Markdown 구문을 처리하는 범용 Parser는 아닙니다.
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
