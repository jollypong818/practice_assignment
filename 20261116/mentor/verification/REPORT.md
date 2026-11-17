# 제작 검수 결과

## 기준과 범위
`Day21_Lecture_20261116.pptx` 86장에 맞춘 8개 실습입니다. 원본 PPT는 변경하지 않았습니다.
Python 3.13.5 / Pydantic 2.13.5 / pytest 9.0.2 / Linux에서 검수했습니다.
공통 런타임은 Pydantic v2와 표준 라이브러리입니다. requirements는 설치 범위이며 검증한 정확한 버전은 environment.json에 기록했습니다.

## 수행한 검사
| 구분 | 실제 결과 |
|---|---|
| Python 구문 | 116개 파일 컴파일 통과 |
| 구현 TODO | basic 25 / intermediate 39 / advanced 50 = 114개, 고유 ID와 정답 대응 확인 |
| 기본필수 골격 | 모든 블록에 raise만 있는 형태가 아닌 변수·자료구조·호출·제어문 골격 존재 |
| 정답 복원 | 모든 114개 블록을 대입한 뒤 해당 강사용 파일과 Python AST 일치 |
| 미완성 과제 | mentee 24개 진입점이 의도한 TODO 메시지와 종료코드 2로 중단 |
| 완성 코드 실행 | mentor 24개 + 정답 복원 mentee 24개 실습 경로 통과 |
| 전체 명령 검사 | 위 경로의 prepare/review/fixtures 포함 72개 명령 실행 통과 |
| 공통 자동 테스트 | test_coursekit.py 76개 통과 |
| 심화 실습별 테스트 | Context·Validation·Retry·Project 4개 묶음(20개 테스트)을 mentor·정답 복원본 각각 통과 |
| 전체 점검 기록 | 예상 TODO 중단 24 + 완성 명령 72 + 심화 pytest 실행 8 = 104개 점검 항목 |
| 선택 지식 내보내기 | 시험용 localhost HTTP 서버에서 6개 확인. 기존 강의 FastAPI 서비스는 직접 호출하지 않음 |
| 안내 HTML | mentee·mentor 2개 문서 내용을 Chromium에 렌더링, 가로 영역 초과 없음·링크 대상 존재 확인 |

수치는 검사 종류가 다른 단위이므로 합쳐서 ‘모델 정확도’처럼 사용하지 않습니다.

## 핵심 검증 내용
JSON·Schema·출처/상태의 26개 작성 샘플, 엄격한 정수·중복 키·크기 제한,
문맥 ID·순서·가상 token 예산, 예제901의 평가 데이터 분리, 최대 2회/형식오류만 재시도,
최초·수정 응답 분리, 원문 보존, 미실행·미평가 유지, freeze 이후 해시 변조 감지를 검사했습니다.
수동 응답 등록 테스트에는 시험용으로 작성한 문자열만 사용했습니다. 임시 시험 디렉터리에서 실행하고 배포에 포함하지 않습니다.

## 미검증·해석 한계
- 실제 ChatGPT 화면에서 질문을 실행하지 않았고 LLM API도 호출하지 않았습니다. A/B 승률·근거 품질 향상 수치는 없습니다.
- Windows 11, PowerShell, VS Code 버튼 조작, 신규 패키지 다운로드·설치를 직접 검증하지 못했습니다.
- HTML의 file:// 이동은 제작 환경 정책으로 차단되어 내용 주입 렌더링으로 확인했습니다. 로컬 파일 더블클릭·클릭 이동의 브라우저 검증과 구분합니다.
- 기본 경로는 고정 JSON 데이터이며 DB·API 서버가 필요 없습니다. 선택 export 도구는 실제 기존 서비스가 아닌 시험용 로컬 서버에서 확인했습니다.
- 응답 규칙 통과는 사실성·근거 정확성 판정이 아닙니다. 사람 평가를 별도로 수행해야 합니다.

## 재현
통합본에서 `python mentor/verification/verify_package.py --output verification_result.json`을 실행하세요.
통합 점검은 임시 디렉터리에 복사하여 수행하며 학생 작업 outputs를 덮어쓰지 않습니다.
공통 테스트만 실행: `python -m pytest -q mentor/verification/test_coursekit.py`
심화 문제 테스트는 **각 교시 폴더**에서 `python -m pytest -q tests`로 실행하세요.
분리된 mentor ZIP만으로는 정답 대응 검사를 할 수 없으며, 통합본의 mentee가 필요합니다.

## 수업 전
강사는 실제 강의 PC에서 환경 검사·mentor 기본필수 01/06/07 및 수동 응답 1건 등록을 확인하세요.
수강생에게는 mentee ZIP만 배포합니다. 답변을 실제로 실행하지 못한 학생에게 샘플을 실측으로 제출하게 하지 않습니다.
