# 실행 준비 — Windows 11 · VS Code

## 1. 압축을 풀고 폴더 열기
ZIP 안에서 실행하지 않습니다. `mentee` 또는 `mentor` 폴더 하나를 VS Code에서 엽니다. 폴더·소스 파일명은 영문입니다. 공백이 있는 경로는 따옴표로 감싸세요.
기존 수업 가상환경에 설치해도 됩니다. PostgreSQL 서버, GPU, PyTorch, 벡터 DB는 이날 새로 설치하지 않습니다.

## 2. 같은 Python으로 설치·실행
Python 3.11 이상을 사용합니다. 제작 검수는 Python 3.13.5에서 수행했습니다.
아래 명령은 선택한 role 폴더에서 실행합니다. 이미 쓰는 가상환경이 있으면 같은 interpreter를 사용합니다.
```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip show openai pydantic python-dotenv
```
활성화가 막혀도 보안 정책을 임의 해제하지 말고 위처럼 Python 전체 경로를 사용합니다. VS Code의 Python interpreter도 이 환경으로 선택합니다.

이 제작 환경에서는 OpenAI SDK를 내려받지 못했습니다. `requirements.txt`는 설치 범위이며 전체 검증 잠금파일이 아닙니다. 강의 PC에서 실제 연결·Streaming까지 확인한 뒤 `python -m pip freeze` 결과를 비밀 없는 파일로 보관하세요. 오프라인 정책 검사는 `requirements-offline.txt`의 Pydantic만 있으면 됩니다.

## 3. 키는 본인 PC의 .env에만
`.env.example`을 **같은 폴더의 `.env`**로 복사합니다. `YOUR_API_KEY`만 본인 키로 바꿉니다. 키를 채팅·코드·스크린샷·제출물에 넣지 않습니다. 실제 키를 강사에게 보내지 않습니다.

```powershell
Copy-Item .env.example .env
.\.venv\Scripts\python.exe tools/preflight.py
```
preflight는 외부로 요청을 보내지 않습니다. 키가 설정됐다는 것과 실제 인증·잔액·모델 권한이 확인됐다는 것은 다릅니다. OS 환경변수가 `.env`보다 우선하므로 이전 설정 충돌도 확인합니다.

- 기본 후보: `gpt-5.4-mini-2026-03-17`.
- 비교 후보: `gpt-5.4-2026-03-05`. 승인된 경우에만 `OPENAI_MODEL_QUALITY`를 설정합니다. 미설정이면 실제 비교는 `not_run`입니다.
- 모델명·기능·단가는 PPT의 후보를 유지했습니다. 계정 접근권은 사전 확인 대상입니다. 모델 교체는 `config/models.json`·요청 인자·`config/prices.json`을 함께 검토해야 합니다.

## 4. 기본필수 첫 실행
TODO를 먼저 완성합니다. 미완성 `raise NotImplementedError(...)`가 있으면 **키 조회·실제 전송 전에 중단**합니다. raise 한 줄만 지우고 빈 값을 그대로 두는 것은 완료가 아닙니다.
```powershell
.\.venv\Scripts\python.exe 01_basic/01_first_call/main.py --source simulated
.\.venv\Scripts\python.exe 01_basic/01_first_call/main.py --source live --allow-paid
```
첫 명령은 모의 코드 확인이며 인증 성공이 아닙니다. 두 번째가 실제 호출·과금 가능 경로입니다. 기본 실행 source는 live지만 `--allow-paid`가 없으면 보내지 않습니다.

## 5. 개인 전송 장부
같은 PC의 교시·수준·role에서 실제 호출 수를 공유합니다. 기본 위치는 사용자 홈의 `.day22_llm_lab/send_ledger_20261117.json`입니다. 설정 기본 한도는20회입니다. 캐시 히트·모의 실행은 실제 전송 수에 더하지 않습니다. 재시도·형식 수정은 더합니다.

전송 직전에 예약하므로 예외·프로세스 종료 후에도 이미 사용한 수가 사라지지 않습니다. 장부가 손상되면 자동0으로 초기화하지 않습니다. 한도 도달이나 남은 `.lock`은 강사와 원인을 확인하고, 다른 터미널을 닫은 뒤 처리하세요. 자동 초기화 스크립트는 제공하지 않습니다. 이 장부는 순차 로컬 실습용이며 분산 과금 차단기나 공급자 한도를 대신하지 않습니다.

## 6. 실제 실행 결과가 없을 때
미실행은 `not_run`으로 이유만 남깁니다. 실제 실패를 겪었다면 `api_live`의 실패 상태를 보존합니다. 네트워크·권한 때문에 모의 경로를 사용한 경우 실제 응답·시간·비용을 얻었다고 기록하지 않습니다.
