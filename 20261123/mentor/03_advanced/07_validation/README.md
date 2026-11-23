# 실습 07 · Validation과 출처 확인

**03_advanced · 심화 · 강사용 정답·해설 / 강의 실습 안내 70페이지 (본문 61~69페이지)**

## 목표

Context에 실제로 포함한 문서에서 허용 출처를 구하고, 정상·근거 부족·미제공 ID의 공통 세 사례, 문자열 ID와 중복 ID, incomplete와 잘못된 주장를 검증합니다. **기계 검증의 통과와 원문이 답변을 지지하는지를 구분**하는 실습입니다. 외부 모델이나 DB를 호출하지 않습니다.

## 먼저 알아야 할 용어

| 용어 | 의미 | 이번 코드에서 확인할 곳 |
|---|---|---|
| Structured Output | 정해진 필드·자료형을 따르는 모델 출력 형식 | `WireAnswer`와 `parsed` |
| Validation | 입력이 정해진 조건을 만족하는지 검사 | `receive_bundle`의 순차 검사 |
| Citation | 답변과 참고 문서를 연결하는 출처 식별자 | `source_ids`와 `included_docs` |
| Grounding | 원문의 내용이 답변의 주장을 실제로 지지하는 관계 | `reports/review.md`의 원문 대조 |
| `raw / parsed / parsing_error` | 원래 AIMessage / 해석된 객체 / 파싱 실패 정보 | 각 사례의 `bundle` |

## 입력과 출력

- 입력: `coursekit.data.example_hit()`의 출석 v2 문서와 의도적으로 만든 응답 묶음. ID 201은 교육용입니다.
- 제공된 이전 단계: `hits_to_documents`와 `build_context`가 Document·Context를 준비합니다.
- 수정 대상: **`tasks.py`의 BEGIN~END 블록**. 현재 실습의 TODO를 `coursekit`으로 우회하지 않습니다.
- 출력: `outputs/validation_report.json`. 포함 ID, 원문 Context, 사례별 `accepted/rejected`, 오류 코드, 검증된 네 필드를 기록합니다.
- `accepted`여도 `human_review_required=true`입니다. 자동 결과가 참/거짓을 결정하지 않습니다.

## 구현할 TODO

| ID | 요구사항 |
|---|---|
| `D26-07-A01` | included_docs의 metadata에서 citation_id를 모아 set으로 반환합니다. |
| `D26-07-A02` | receive_bundle로 검사한 결과를 accepted/rejected 형식으로 기록합니다. |
| `D26-07-A03` | 정상 입력에서 ID만 문자열 또는 중복 정수로 바꾼 두 fixture_bundle 사례를 반환합니다. |
| `D26-07-A04` | incomplete 완료 상태 사례와 올바른 ID의 잘못된 주장 사례를 반환합니다. |

## 실행 방법

1. 역할 폴더의 README대로 기존 Python 가상환경과 기본 패키지를 확인합니다.
2. VS Code의 Git Bash에서 현재 실습 폴더로 이동합니다.

```bash
python main.py
python -m pytest -q tests
```

수강생 파일은 TODO를 채우기 전 `NotImplementedError`로 멈춥니다. 이 실습은 `--live` 옵션이 없고 실행해도 API 비용이 발생하지 않습니다. 앞 실습이 미완성이어도 제공 Checkpoint로 진행할 수 있습니다.

## 결과를 읽는 순서

1. `included_ids`가 현재 Context의 ID와 같은지 확인합니다.
2. `normal`과 `insufficient`는 형식·업무 규칙을 통과하며, `unknown_source`는 거절되는지 봅니다.
3. 오류 코드로 **수신 상태 → 파싱 → 자료형·업무 규칙** 중 어느 경계인지 구분합니다.
4. 통과한 답변의 15분 기준, 초과 조건, 사전 승인 예외를 출석 원문과 대조합니다.
5. 자동 검사가 답변의 의미를 보장하지 않는 이유를 `reports/review.md`에 적습니다.

## 주의할 점과 오류 대응

- 검색 후보 전체의 ID를 허용하면 Context에 없는 문서를 인용할 수 있습니다. `included_docs`만 사용합니다.
- `source_ids=["201"]`를 `int()`로 고쳐 통과시키지 않습니다. strict 자료형 검사를 관찰하는 입력입니다.
- `incomplete`는 모델이 실행을 완료하지 못한 상태이고, `insufficient_context`는 정상 응답의 업무 상태입니다.
- 예상한 검증 거절만 기록합니다. 프로그래밍 오류까지 모두 성공으로 처리하지 않습니다.
- `expected/EXPECTED.md`는 비교 기준이며 실제 모델 성능이나 호출 결과가 아닙니다.

## 완료 기준

공통 세 사례의 통과·거절을 구분하고 허용 ID의 출처를 설명합니다. 자신의 실행 결과에서 통과한 답변 한 개를 골라, 원문 문장과 숫자·조건·예외를 대조한 기록까지 남깁니다.
