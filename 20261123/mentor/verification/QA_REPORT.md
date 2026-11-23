# 제작 검수 기록 · Day26 RAG & LangChain

검수일: 2026-11-20. 범위: 8개 주제 × 3수준 × mentor/mentee 대응.

## 확인 결과

| 항목 | 결과 |
|---|---|
| 강사용 24개 실습 로컬 실행 | 모두 정상 종료. 05·06·08은 명시적 --offline 사용 |
| 강사용 실습 단위 테스트 | 91개 통과 |
| 공통 E5/DB 준비 코드 계약 테스트 | 24개 통과 |
| 실제 LangChain/OpenAI SDK + 모의 HTTP 변환 | completed·incomplete·refusal 3개 통과 |
| 수강생 24개 미완성 실습 | TODO의 NotImplementedError로 실패함을 확인 |
| 두 역할의 Python 문법 | 156개 파일 구문 검사 통과 |
| TODO와 정답 블록 대응 | Basic16 / Intermediate24 / Advanced32, 역할별 ID 일치 |
| 학생 TODO 내부의 답 코드 | raise 뒤 완성 코드 없음; 각 블록 요구사항·힌트 제공 |
| 새 API·DB 실제 ID 보존 | 고정 설명용 201에 의존하지 않는 ID로 검사 |

코드 검사는 총 115개의 단위 테스트와 3개의 SDK 변환 사례입니다. 정상 사례 외에 빈 입력·필수 Metadata 누락·중복·문자 상한 경계·문자열 ID·미제공 ID·미완료 응답·Timeout·HTTP 422/502를 확인했습니다.

실제 SDK 변환 검사는 가짜 API Key와 httpx2.MockTransport를 사용했고 socket 연결을 차단했습니다. 외부 네트워크 시도는 0회였습니다. 실제 Key나 .env 자격 증명은 사용하지 않았습니다.

## 검수 중 보완

- Metadata 보존 판정이 여섯 Key 전체와 값의 일치를 확인하도록 수정했습니다.
- 실습 03의 설명을 실제 구성요소 대응표 입력·출력과 맞췄습니다.
- 문자열 ID의 WireAnswer 파싱 실패와 중복 ID의 업무 규칙 실패를 구분했습니다.
- Context 관찰 중 오류가 실제 API의 502 결과를 가리지 않도록 했습니다.
- 고정 refusal 사례의 parsed/parsing_error를 실제 SDK의 상태와 맞췄습니다.
- 실제 LLM 호출이 필요 없는 01~04·07과 호출 단계 05·06·08의 실행 안내를 구분했습니다.

## 수행하지 않은 범위

제작 환경은 Linux/Python3.12입니다. Windows11에서의 실제 설치, E5 모델 다운로드·임베딩, PostgreSQL 서버 접속·저장, 계정 인증 및 유료 모델 API 호출은 수행하지 않았습니다. 이 성공을 주장하지 않으며, 수업 PC에서 README의 실제 실행 절차로 확인해야 합니다.

Fake Encoder와 Recording Connection 검사는 호출 순서·입력·SQL parameter·transaction 처리 계약을 확인합니다. 실제 PostgreSQL 서버에서 SQL을 실행한 결과와 같다고 부르지 않습니다.

자동 검사는 답변의 모든 주장을 평가하지 않습니다. 실제 출력은 원문의 숫자·예외·날짜 유무·출처를 사람이 대조합니다. 강의의 다섯 질문 검수표를 함께 사용하세요.
