# 실습 02 · Hit에서 Context 만들기

**난이도:** 03_advanced · 심화  
**대상:** 수강생 TODO  
**강의 연결:** 2026-11-23 HTML의 실습 안내 18페이지 / Chapter 2

## 목표

선택한 Hit의 본문과 출처를 Context 문자열과 included_ids에 함께 담습니다.

## 먼저 알아야 할 용어

- **Hit**: 검색 결과 한 건을 표현하는 dict입니다. 본문과 출처가 함께 들어 있습니다.
- **f-string**: 문자열 안에 변수 값을 넣는 Python 표현입니다. 대괄호 속 citation_id도 실제 값으로 채웁니다.
- **join**: 문자열 목록을 구분자로 연결하는 메서드입니다. 빈 목록이면 빈 문자열이 됩니다.
- **included_ids**: 실제로 Context에 포함한 Hit의 ID 목록입니다. 검색 후보 전체의 ID와 구분합니다.

## 입력과 출력

- 입력: 오늘 제공한 data/lecture_hits.json의 강의 예시입니다. 출석 v2·과제 v1·시설 v1의 본문과 출처가 들어 있습니다.
- 수정할 파일: tasks.py. main.py는 tasks.py의 main을 실행합니다.
- 결과: 이 실습 폴더의 outputs/hit_context.json. 파일 위치는 실행한 Terminal의 위치가 아니라 현재 실습 파일 경로를 기준으로 정합니다.
- 예시 데이터의 201·202·203은 설명용 ID입니다. 기본 실행 결과를 실제 DB 검색이나 LLM 생성 결과로 기록하지 않습니다.

## 구현할 부분

| ID | 함수 | 요구사항 |
|---|---|---|
| D26-02-A01 | format_hit | [ID] 원문위치, 줄바꿈, 본문 순서로 한 블록을 만듭니다. |
| D26-02-A02 | select_hits | 입력 순서대로 앞의 최대 max_items건을 선택합니다. |
| D26-02-A03 | make_context | 선택 결과를 문자열로 연결하고 같은 Hit의 citation_id 목록을 반환합니다. |
| D26-02-A04 | compare_empty_and_one | 빈 목록과 한 건을 각각 호출해 두 결과를 저장합니다. |

각 TODO의 입출력과 힌트를 읽고 작은 부분부터 완성하세요. NotImplementedError를 없애기만 하면 완료가 아니라 함수가 요구한 값을 반환해야 합니다.

## 실행 방법

1. ZIP을 풀고 역할 폴더인 mentee 또는 mentor를 VS Code로 엽니다.
2. 기존에 사용하던 Python 가상환경이 선택되어 있는지 역할 루트의 안내로 확인합니다.
3. Git Bash Terminal에서 현재 실습 폴더(03_advanced/02_hit_context)로 이동합니다.
4. 다음 명령으로 실행하고 검사합니다.

~~~bash
python main.py
python -m pytest -q tests
~~~

수강생 초기 버전은 TODO가 있어 NotImplementedError로 멈추고 자동 검사도 실패합니다. 정상적인 시작 상태입니다.

## 완료 기준

- Context 첫 줄은 [201] attendance_v2.md#sec-1이며 다음 줄에 원문 전체가 이어집니다.
- included_ids는 [201]이며 실제 선택한 Hit와 일치합니다.
- 빈 입력의 결과는 빈 문자열과 빈 목록입니다. character_count는 문자 수이며 Token 수가 아닙니다.

expected/EXPECTED.md와 outputs의 JSON을 비교한 뒤 reports/review.md의 질문에 답합니다. 자동 테스트는 자료형·연결·경계 조건을 확인하며 설명의 의미나 실제 답변의 Grounding을 대신 평가하지 않습니다.

## 문제가 생겼을 때

KeyError가 발생하면 Hit에 body·citation_id·source_locator가 있는지 확인합니다. 줄바꿈이 문자 그대로 보이면 문자열의 줄바꿈 표현을 확인합니다. 빈 목록의 Context는 정상적으로 빈 문자열입니다.

## 독립 실습과 다음 단계

앞 실습이 미완성이어도 오늘의 공통 데이터와 현재 폴더만으로 시작할 수 있습니다. 다른 학생이나 mentor의 출력 파일을 복사해 성공 결과로 제출하지 않습니다.

이번 실습은 순수 Python의 dict·list·str를 연결합니다. 검색 순위를 새로 계산하지 않고 준비된 Hit의 순서를 사용합니다. 중복 제거·전체 블록 길이 제한은 실습 06에서 구현하므로 지금은 선택한 본문과 ID가 같은 출처를 가리키는지 집중합니다.
