# 실습 03 · LangChain 객체의 입력·출력과 invoke

**난이도:** 03_advanced · 심화  
**대상:** 강사 완성 코드  
**강의 연결:** 2026-11-23 HTML의 실습 안내 30페이지 / Chapter 3

## 목표

네 구성요소가 받는 값·돌려주는 값과 값 읽기·invoke 실행의 차이를 설명합니다.

## 먼저 알아야 할 용어

- **Document**: 본문 page_content와 출처 metadata를 보관하는 데이터 객체입니다.
- **invoke**: 한 입력으로 해당 구성요소를 실행하고 결과를 받는 메서드 이름입니다. 구성요소에 따라 하는 일이 다릅니다.
- **ChatPromptValue**: 질문과 Context가 채워진 메시지를 담는 Prompt의 출력입니다.
- **AIMessage**: Chat Model의 응답을 담는 객체입니다. Prompt 작성 결과와 구분해야 합니다.

## 입력과 출력

- 입력: tasks.py의 COMPONENT_INPUTS 구성요소 입력표와 출석 본문을 사용합니다. 출석 본문은 data/lecture_hits.json에서 읽어 Prompt 입력 dict를 만드는 데만 사용합니다.
- 수정할 파일: tasks.py. main.py는 tasks.py의 main을 실행합니다.
- 결과: 이 실습 폴더의 outputs/object_contracts.json. 파일 위치는 실행한 Terminal의 위치가 아니라 현재 실습 파일 경로를 기준으로 정합니다.
- 이 실습은 구성요소의 역할·자료형을 대응시키는 로컬 확인입니다. Retriever·Prompt·Chat Model의 invoke를 실제 실행하지 않습니다.

## 구현할 부분

| ID | 함수 | 요구사항 |
|---|---|---|
| D26-03-A01 | component_outputs | 네 구성요소의 반환값을 구분해 dict로 반환합니다. |
| D26-03-A02 | access_kinds | Document는 data, 실행 구성요소는 invoke로 표시합니다. |
| D26-03-A03 | repair_document_call | 잘못된 Document 호출과 올바른 본문 읽기·생성 역할을 기록합니다. |
| D26-03-A04 | make_prompt_input | question과 context 문자열을 두 Key의 dict로 반환합니다. |

동일 ID가 수강생 코드의 TODO와 대응합니다. BEGIN/END 사이의 주석을 읽으며 왜 이 처리가 필요한지 설명하세요.

## 실행 방법

1. ZIP을 풀고 역할 폴더인 mentee 또는 mentor를 VS Code로 엽니다.
2. 기존에 사용하던 Python 가상환경이 선택되어 있는지 역할 루트의 안내로 확인합니다.
3. Git Bash Terminal에서 현재 실습 폴더(03_advanced/03_langchain_objects)로 이동합니다.
4. 다음 명령으로 실행하고 검사합니다.

~~~bash
python main.py
python -m pytest -q tests
~~~

강사용은 모든 TODO가 완성되어 있습니다. 테스트는 현재 실습 함수의 결과를 검사하며 API·DB를 호출하지 않습니다.

## 완료 기준

- 네 구성요소 각각에 input·output·access가 있는 표가 생성됩니다.
- Prompt의 출력은 ChatPromptValue이며 Chat Model의 출력은 AIMessage입니다.
- Document는 본문·출처를 담는 data로 표시하고 실제 API는 호출하지 않습니다.

expected/EXPECTED.md와 outputs의 JSON을 비교한 뒤 reports/review.md의 질문에 답합니다. 자동 테스트는 자료형·연결·경계 조건을 확인하며 설명의 의미나 실제 답변의 Grounding을 대신 평가하지 않습니다.

## 문제가 생겼을 때

표의 Key를 바꾸면 KeyError가 날 수 있습니다. Document·Retriever·Prompt·Chat Model의 이름을 일정하게 사용합니다. 이 실습에서 API Key를 요구한다면 실행한 파일과 실습 폴더가 맞는지 먼저 확인합니다.

## 독립 실습과 다음 단계

앞 실습이 미완성이어도 오늘의 공통 데이터와 현재 폴더만으로 시작할 수 있습니다. 다른 학생이나 mentor의 출력 파일을 복사해 성공 결과로 제출하지 않습니다.

객체 이름만 외우지 말고 “무엇을 받아 무엇을 돌려주는가?”를 한 문장으로 설명합니다. 이 장에서는 Prompt 객체 생성과 invoke를 실제로 실행하지 않습니다. 실습 05에서 지금 정리한 입력·출력을 실제 객체로 확인합니다.
