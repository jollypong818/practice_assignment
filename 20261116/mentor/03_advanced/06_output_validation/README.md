# 06 · JSON·Schema·참조 검증

PPT **46~55장**, 실습 약 **25분**. 강사용: 정답이 완성된 코드입니다. 실제 모델 응답·평가는 자동으로 채우지 않습니다.

## 목표
문법·Schema·참조 규칙을 구현합니다. 자동 통과 뒤에도 사람이 볼 반례를 남깁니다.

## 편집할 파일
`contracts/parser.py`, `contracts/rules.py`, `contracts/schema.py`, `validation.py`
`# BEGIN/END` 블록의 골격을 완성하고 해당 NotImplementedError 줄을 지웁니다.
각 TODO는 요구·입력·완료 기준을 주석으로 함께 설명합니다.

| 블록 | 요구사항 |
|---|---|
| `D21-06-A01` | PPT 50장의 엄격한 네 필드 계약을 선언하세요. |
| `D21-06-A02` | JSON 문법 실패와 Pydantic Schema 실패를 분리하세요. |
| `D21-06-A03` | 중복 출처와 이번에 제공하지 않은 출처를 서로 구분하세요. |
| `D21-06-A04` | 상태별 필드 조합과 공백·부족 고정문을 검사하세요. |
| `D21-06-A05` | 제공 fixture를 분류하고 모델 정의에서 Schema를 내보내세요. |
| `D21-06-A06` | ID 101을 붙인 서버 답변이 자동 검사만 통과하는 반례를 확인하세요. |
| `D21-06-A07` | 중복 키·NaN·과도한 크기·Schema 경계를 실제 반례로 검사하세요. |

## 실행 위치
터미널에서 **이 README가 있는 폴더**로 이동합니다. `python`은 선택한 가상환경입니다.
```powershell
python main.py
```
`python main.py`를 파일의 절대경로로 실행해도 데이터·출력은 이 폴더 기준입니다.

## 산출물
`fixture_results.json`, `answer_schema.json`. 예상 결과는 `expected/EXPECTED.md`와 대조합니다.

## 한 문장 설명
이 코드가 해결하는 문제와 아직 확인하지 못한 것을 구분해 설명하세요.
실행 성공·샘플 통과만으로 실제 모델 답변 품질이 좋아졌다고 주장하지 않습니다.

## 선택 자동 확인
이 폴더에서 `python -m pytest -q tests`로 **자신의 구현**을 검사합니다. TODO 미완성 상태의 실패는 정상입니다. pytest는 requirements_test.txt로 추가 설치합니다.
