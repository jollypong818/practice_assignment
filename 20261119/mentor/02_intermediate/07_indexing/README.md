# 실습 07 · pgvector · Stage → Publish → Search

**난이도:** 02_intermediate · **용도:** 강사용 정답·해설

## 목표
실제 E5 임베딩·pgvector 저장을 구현하며, 미실행을 성공으로 표시하지 않습니다.

## 먼저 알아야 할 용어
- **Stage**: 공개하기 전에 새 버전을 저장하는 단계
- **Publish**: 검증된 버전을 현재 검색 대상으로 선택
- **Transaction**: 성공·실패에 따라 묶어서 COMMIT/ROLLBACK

## 구현할 TODO

| ID | 요구사항 |
|---|---|
| `D24-07-I01` | 여러 ParsedUnit을 정제·분할하고 입력 청크의 출처·버전 계약을 통일합니다. |
| `D24-07-I02` | 실제 E5 Encoder로 384차원 passage 벡터를 만들고 개수·길이·유한값을 확인합니다. |
| `D24-07-I03` | 짧은 DB Transaction 안에서 Chunk·벡터를 Staging 합니다. |
| `D24-07-I04` | 검증된 버전만 Publish하고 동일 계약의 query: 벡터로 Top-k를 조회합니다. |

## 실행 방법
- 수정 대상: `tasks.py`. `main.py`는 실행 진입점입니다.
- VS Code의 **Git Bash**에서 이 폴더로 이동하여 실행합니다. 기존 Python 가상환경을 사용합니다.
- `python main.py`
- 추가 실행: `python main.py --live-db` (PostgreSQL 18.6 + pgvector + E5 + `.env` 준비 시에만).
- DB 없는 기본 실행은 `prepared_only_not_db` 또는 `not_run`이며, DB 성공을 의미하지 않습니다.

## 완료 기준
기본: prepared_only_not_db. --live-db에서 실제 저장·검색. 데이터 1~N행, 점수/시간은 실제 실행 후 확인.

## 독립 실습과 결과
- 앞 교시가 미완성이어도 현재 폴더의 준비 코드와 `coursekit/` Checkpoint로 시작할 수 있습니다.
- 출력 파일은 해당 폴더의 `outputs/`에 생성됩니다. `data/raw/` 원문은 수정하지 않습니다.
- `expected/EXPECTED.md`는 평가 기준이지 실제 실행 로그가 아닙니다.
- 수강생은 실행 결과 외에 “어느 원문·어느 처리 버전·어느 실패 지점인가?”를 설명해야 합니다.

## 현업 연결 / 한계
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
