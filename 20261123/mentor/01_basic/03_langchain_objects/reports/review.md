# 실습 03 확인 기록

- 선택한 수준: 01_basic
- 실행일: 
- 실행 명령: 
- 결과 파일: outputs/object_contracts.json
- 입력 출처와 실행한 구성요소: 

## 1. 같은 invoke인데 Prompt와 Chat Model은 무엇이 다른가요?

Prompt는 메시지를 구성하고 Chat Model은 모델에 답변을 요청합니다.

## 2. Document에서 본문을 읽는 표현은 무엇인가요?

doc.page_content입니다. metadata에서는 출처를 읽습니다.

## 3. Document 목록을 question·context가 필요한 Prompt에 그대로 전달해도 되나요?

이 예제의 입력 계약과 다릅니다. 선택한 문서를 문자열 Context로 만들고 질문과 함께 dict에 담아야 합니다.

