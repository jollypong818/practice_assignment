# 다섯 질문으로 실제 답변 확인

강의 78페이지의 질문 세트입니다. 실습 08의 기본 smoke는 출석·마감일·입력 오류를 확인하고, 아래 표는 다른 질문으로도 같은 흐름을 확인하는 최종 대조입니다.

1. 선택한 실습 08의 TODO를 마칩니다.
2. 해당 폴더에서 `python main.py --serve`로 실제 서버를 시작합니다.
3. `http://127.0.0.1:8000/docs`의 `POST /rag/answer`에서 질문을 하나씩 보냅니다.
4. `data/api_requests.json`에는 요청 Body 다섯 개만 모았습니다. 배열 전체가 아니라 **그중 한 객체씩** 붙여 넣습니다.
5. HTTP 상태, result.status, result.answer, source_ids와 sources를 기록하고 원문을 대조합니다.

다섯 질문을 모두 보내면 최대 다섯 번의 모델 invoke가 발생합니다(빈 Context의 생략과 SDK 재시도는 별도). 이 표의 기대 판단은 실제 모델의 측정 결과가 아닙니다. 예상과 다르면 검색 후보·Context·생성·검증 중 어느 단계가 원인인지 확인합니다.

| 질문 | Category | 기대 판단과 원문 대조 |
|---|---|---|
| 15분 늦으면 어떻게 기록되나요? | 학사 | `answered` · 현재 출석 v2: 일반 기준 15분까지 지각, 사전 승인 예외 확인 |
| 과제 파일은 어디에 보관하나요? | 학사 | `answered` · DOC-ASSIGN의 개인 폴더 |
| 내 과제의 정확한 마감 날짜는? | 학사 | `insufficient_context` · insufficient_context. 원문에는 날짜가 없음 |
| 회의실을 이용하려면 무엇이 필요한가요? | 시설 | `answered` · DOC-FACILITY의 예약 승인 |
| 이번 주말 날씨는 어떤가요? | 학사 | `insufficient_context` · 제공 문서에 근거가 없으므로 정보 부족 |

## 기록할 항목

- 실행 모드와 사용한 문서 버전
- HTTP 상태와 result.status
- 답변이 인용한 실제 ID, sources의 doc_id·source_version·source_locator
- 원문에서 답변을 지지하는 문장 또는 정확한 정보가 없다는 근거
- 기대와 다른 경우 어느 단계부터 다시 확인할지

실제 DB의 ID를 201·202·203으로 고치지 않습니다. 이 ID는 고정 예시의 번호입니다. 원문은 doc_id와 source_locator로 찾습니다. 문서가 검색됐다는 사실만으로 정확한 마감 날짜나 날씨를 답할 수 있는 것은 아닙니다.
