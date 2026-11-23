# 실습 07 · 원문 대조 기록

- 선택한 수준:
- 실행한 파일:
- 실제 실행한 범위: 고정 입력 Validation / DB·Embedding·LLM 미실행

## 공통 확인

1. Context에 들어간 ID와 허용 ID는 각각 무엇인가요?
2. normal 답변의 숫자·조건·예외를 지지하는 원문 문장을 그대로 적고 위치를 밝히세요.
3. unknown_source는 어떤 단계에서 거절됐나요? 검색 후보에만 있던 ID도 허용해도 되나요?
4. insufficient_context가 시스템 오류와 다른 이유를 적으세요.

## 선택한 수준의 추가 확인

- 응용: 문자열 ID와 중복 ID의 실패 지점은 어떻게 다른가요?
- 심화: incomplete와 insufficient_context를 비교하세요. wrong_claim이 기계 검사를 통과해도 원문과 맞지 않는 부분을 적으세요.

자동 검사 통과 여부와 원문 대조 결과를 별도로 기록합니다.
