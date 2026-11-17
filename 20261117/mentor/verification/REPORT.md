# Day22 제작 검수 결과

작성 기준: `Day22_Lecture_20261117.pptx` 86장 · 2026-11-17 수업. PPT는 변경하지 않았습니다.
PPT SHA-256: `23413984cb4e52588859069efbe005f150642d346b0221b8edd8e2ff600545b5`

## 실제 확인한 범위

| 항목 | 확인 결과 |
|---|---|
| 실행 환경 | Linux · Python 3.13.5 · Pydantic 2.13.5 · pytest 9.0.2 · python-dotenv 1.2.2 |
| Python 구문 | 배포 Python 157개 파일 컴파일 확인 |
| TODO·정답 대응 | 24개 구현 파일, 기본26·응용38·심화50 = 총114개 블록. 정답 대입 후 mentor와 AST가 동일 |
| 강사용 실행 | 3단계 × 8교시 = 24개 진입점을 별도 프로세스로 실행, simulated 정상 종료 |
| 정답을 대입한 수강생용 | 3단계 × 8교시 = 24개 진입점을 별도 프로세스로 실행, simulated 정상 종료 |
| 미완성 수강생용 | 24개 진입점이 미완성 TODO를 알리고 exit 2. 키 조회·전송·결과 생성 전에 중단 |
| 단위/정책 테스트 | 131개 통과. 네트워크 차단 상태의 로컬 검사이며 실제 SDK 테스트가 아님 |
| 순차 운영 시나리오 | mentor 3단계와 정답 대입본 3단계, 총6개 경로에서 H3개→사람검토 기록→캐시hit→본문변경miss→사용량분석→표생성 확인 |
| 전날 자료 일치 | contracts.py·knowledge_v1.json·dev_v1.json·holdout_v1.json은 Day21 mentor 원문과 byte 일치 |
| 시작 화면 | HTML 내용을 Chromium에서 렌더링, 폭1280·640에서 가로 넘침 없음. 로컬 링크18개 대상 존재 |
| 경로 | 모든 배포 파일·폴더 경로에 영문·숫자·기호만 사용 |

`final_process_results.json`, `staged_results.json`, `all_tests.log`에 실제 로컬 검수 결과가 있습니다.
단위 테스트 중 source='live' 분기는 **가짜 client와 임시 장부**를 주입하여 계산 분기만 확인합니다.
이것은 공급자 API를 호출했다는 의미가 아니며, 가짜 응답을 실측 결과 파일로 배포하지 않습니다.

## 아직 확인하지 못한 범위

- **OpenAI SDK 설치·실제 SDK 객체와의 실행**: 이 환경에서 pip의 PyPI 접속이 DNS 오류로 실패했습니다. 설치 범위를 requirements에 제공했으나 검증된 lock 파일이라고 주장하지 않습니다.
- **실제 OpenAI 인증·모델 접근권·유료 생성·실제 SSE 스트리밍·과금**: 사용자 API 키를 받거나 호출하지 않았습니다. 실제 모델의 답변·속도·비용을 측정했다고 표시하지 않습니다.
- **Windows 11 / PowerShell / VS Code 직접 실행**: Linux에서 Python 실행 및 다른 작업 폴더의 경로 참조만 확인했습니다.
- Markdown 링크를 Windows 브라우저에서 클릭하는 동작: 로컬 링크 대상은 확인했으나 해당 UI는 미검증입니다. HTML 렌더는 환경의 file:// 제한 때문에 내용을 주입하여 배치를 검사했습니다.

## 사전 실행 안내

수업 전 강사 PC에서 `PREFLIGHT_LIVE.md`를 따라 실제 호출 1건, 구조화 출력, Streaming, 승인 후 캐시를 확인하세요.
추가 호출·과금은 강사가 명시적으로 결정하며, 이미 보유한 키는 본인 PC의 `.env`에만 둡니다.
오류 재현은 실제 서버에 부하를 만들지 않고 `04_errors_retry`의 모의 사례를 사용합니다.

## 재현 명령

mentor 폴더에서:
```powershell
python tools/selfcheck.py
python -m pytest -q tests
python verification/check_pairing.py --mentee ../mentee
python 01_basic/08_daily_project/main.py --source simulated
```
마지막 명령은 코드·연결 확인이며 실제 API 프로젝트 완료를 의미하지 않습니다.
모의 출력 숫자는 모델 성능·청구액으로 비교하지 않습니다. 실제/모의/캐시/미실행을 분리합니다.
