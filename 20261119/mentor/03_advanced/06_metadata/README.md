# 실습 06 · Metadata·Current Filter·Citation Mapping

**난이도:** 03_advanced · **용도:** 강사용 정답·해설

## 목표
ID 충돌·버전 오염·권한 범위와 정수 Citation Mapping을 검증합니다.

## 먼저 알아야 할 용어
- **Metadata Contract**: 필수 출처 필드의 약속
- **Authorization Scope**: 서버가 확인한 허용 문서 범위
- **Citation Mapping**: DB 정수 출처 ID와 Chunk ID의 대응
- **Current Version**: 현재 공개된 원문 판과 처리 판

## 구현할 TODO

| ID | 요구사항 |
|---|---|
| `D24-06-A01` | doc_id·version·category·Span·locator와 page_number 자료형을 검증합니다. |
| `D24-06-A02` | doc_id·원문 판·처리 판·unit_id·Span으로 안정적인 chunk_id를 만듭니다. |
| `D24-06-A03` | 서버가 확인한 allowed_doc_ids 목록으로만 후보를 제한합니다. |
| `D24-06-A04` | 문서별 current source_version·pipeline_version 쌍과 category가 맞는 후보를 선택합니다. |
| `D24-06-A05` | 양의 정수 citation_id와 문자열 chunk_id 사이의 중복 없는 매핑을 만듭니다. |
| `D24-06-A06` | 정상·차단·미공개·Metadata 오류 상태를 구분해 감사 결과를 출력합니다. |

## 실행 방법
- 수정 대상: `tasks.py`. `main.py`는 실행 진입점입니다.
- VS Code의 **Git Bash**에서 이 폴더로 이동하여 실행합니다. 기존 Python 가상환경을 사용합니다.
- `python main.py`

## 완료 기준
설명용 Citation 202만 선택. DB에서 반환한 ID가 아니며 실제 연동 시 DB citation_id 사용.

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
