# 실습 04 · 검색 Hit를 Document로 변환하기

**난이도:** 01_basic · 기본필수  
**대상:** 수강생 TODO  
**강의 연결:** 2026-11-23 HTML의 실습 안내 40페이지 / Chapter 4

## 목표

검색 Hit의 본문·정수 ID·문서 버전·원문 위치를 실제 LangChain Document에 보존합니다.

## 먼저 알아야 할 용어

- **Adapter**: 기존 데이터를 다음 구성요소가 사용할 형태로 바꾸는 연결 코드입니다.
- **page_content**: Document에 저장하는 본문 문자열입니다.
- **metadata**: 문서 ID·버전·원문 위치 등을 보관하는 dict입니다.
- **KeyError**: dict에서 필수 Key를 찾지 못한 오류입니다. 이번 실습에서는 source_locator 누락과 빈 목록을 구분할 때 확인합니다.

## 입력과 출력

- 입력: 오늘 제공한 data/lecture_hits.json의 강의 예시입니다. 출석 v2·과제 v1·시설 v1의 본문과 출처가 들어 있습니다.
- 수정할 파일: main.py. main.py 자체가 실행 진입점입니다.
- 결과: 이 실습 폴더의 outputs/document_adapter.json. 파일 위치는 실행한 Terminal의 위치가 아니라 현재 실습 파일 경로를 기준으로 정합니다.
- 예시 데이터의 201·202·203은 설명용 ID입니다. 기본 실행 결과를 실제 DB 검색이나 LLM 생성 결과로 기록하지 않습니다.

## 구현할 부분

| ID | 함수 | 요구사항 |
|---|---|---|
| D26-04-B01 | to_document | 본문을 page_content로, 제공된 여섯 Key를 metadata로 옮깁니다. |
| D26-04-B02 | hits_to_documents | 입력 순서대로 to_document를 호출해 목록을 반환합니다. |

각 TODO의 입출력과 힌트를 읽고 작은 부분부터 완성하세요. NotImplementedError를 없애기만 하면 완료가 아니라 함수가 요구한 값을 반환해야 합니다.

## 실행 방법

1. ZIP을 풀고 역할 폴더인 mentee 또는 mentor를 VS Code로 엽니다.
2. 기존에 사용하던 Python 가상환경이 선택되어 있는지 역할 루트의 안내로 확인합니다.
3. Git Bash Terminal에서 현재 실습 폴더(01_basic/04_document_adapter)로 이동합니다.
4. 다음 명령으로 실행하고 검사합니다.

~~~bash
python main.py
python -m pytest -q tests
~~~

수강생 초기 버전은 TODO가 있어 NotImplementedError로 멈추고 자동 검사도 실패합니다. 정상적인 시작 상태입니다.

### 실제 DB 검색 Hit를 사용하려면

먼저 역할 폴더 루트의 README와 실제 DB 준비 안내를 완료합니다. 오늘 제공한 전용 Schema에 문서가 저장되어 있어야 합니다. PostgreSQL 준비가 안 된 상태에서 기본 변환을 먼저 진행할 수 있습니다.

~~~bash
python main.py --live-db --question "15분 늦으면 어떻게 기록되나요?" --category "학사" --candidate-k 3
~~~

이 명령은 실제 E5 모델과 DB 조회를 사용하며 LLM은 호출하지 않습니다. 처음 실행할 때 모델 파일이 준비되어 있지 않으면 다운로드 시간이 필요합니다. 실행한 DB의 citation_id가 201과 다르더라도 정상이며 예시 ID로 덮어쓰지 않습니다. 인증·연결·모델 준비 오류가 발생하면 해당 단계를 해결하고 다시 실행합니다. 프로그램은 실패를 예시 데이터로 바꾸지 않습니다.

## 완료 기준

- 기본 실행은 예시 Hit 한 건으로 Document 한 개를 만듭니다.
- body_preserved와 metadata_preserved는 True이며 citation_id_type은 int입니다.
- Metadata는 citation_id·chunk_id·doc_id·source_version·source_locator·category 여섯 필드입니다.
- 빈 Hit 목록은 []; source_locator가 없으면 KeyError가 발생합니다.

expected/EXPECTED.md와 outputs의 JSON을 비교한 뒤 reports/review.md의 질문에 답합니다. 자동 테스트는 자료형·연결·경계 조건을 확인하며 설명의 의미나 실제 답변의 Grounding을 대신 평가하지 않습니다.

## 문제가 생겼을 때

ModuleNotFoundError: langchain_core이면 역할 루트의 requirements_base.txt 설치와 VS Code Python Interpreter를 확인합니다. KeyError: source_locator는 의도한 누락 검사일 수 있습니다. 정상 입력에서도 발생한다면 조회 Hit의 필드를 확인합니다.

## 독립 실습과 다음 단계

앞 실습이 미완성이어도 오늘의 공통 데이터와 현재 폴더만으로 시작할 수 있습니다. 다른 학생이나 mentor의 출력 파일을 복사해 성공 결과로 제출하지 않습니다.

Document로 바꾸어도 기존 검색 조건은 그대로 필요합니다. 이번 변환은 여섯 Metadata 필드만 옮기고, 데이터에 없는 값을 추정하지 않습니다. 기본 실행은 예시를 실제 Document 객체에 담은 결과입니다. --live-db를 선택했을 때만 E5와 PostgreSQL을 사용합니다.
