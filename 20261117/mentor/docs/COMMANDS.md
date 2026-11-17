# 실행 메뉴

명령은 `mentee` 또는 `mentor`를 작업 폴더로 한 예입니다. `.venv`를 활성화하지 않았다면 `python`을 `.\.venv\Scripts\python.exe`로 바꾸세요. 수준은 하나만 선택합니다.

## 실제 호출과 모의
```powershell
python 01_basic/01_first_call/main.py --source live --allow-paid
python 01_basic/02_structured_output/main.py --source live --allow-paid
python 01_basic/03_streaming/main.py --source live --allow-paid
python 01_basic/04_errors_retry/main.py --source simulated
```
04는 어떤 옵션을 주어도 제공 모의 사례만 검사합니다. 실제401·429를 유발하지 않습니다.

## 이미 받은 응답의 사용량 분석 — 재호출0회
```powershell
python 01_basic/05_usage_cost/main.py --run-file "01_basic/02_structured_output/outputs/runs/실제_run_id/run.json"
```
`실제_run_id`는 앞 실행에서 출력된 폴더명으로 바꿉니다. 계산 연습만 할 때는 `--source simulated`를 사용합니다. 경로가 존재하지 않으면 자동으로 답변을 새로 생성하지 않습니다.

## 캐시: 생성 → 사람 검토 → 재사용 → 변경
```powershell
python 01_basic/06_response_cache/main.py --source live --allow-paid
python tools/review.py --run-file "실제_run.json_경로" --decision approve --note "질문의 요구와 출처103의 오류메시지·시도한작업을 직접 대조함"
python 01_basic/06_response_cache/main.py --source live --action reuse --run-file "실제_run.json_경로"
python 01_basic/06_response_cache/main.py --source live --allow-paid --action changed --run-file "실제_run.json_경로"
```
위 검토 메모는 형식 예시입니다. 실제 답을 확인하지 않고 그대로 승인하지 않습니다. 잘못된 답은 `--decision reject`와 실제 이유를 적습니다. `reuse`는 키 없이도 가능한 로컬 조회이며 유료 호출을 하지 않습니다. `changed`는 승인한 원문이 있어야 본문 변경의 미스를 관찰하고 **별도의 새 호출**을 합니다. `--allow-paid`가 없으면 새 호출은 미실행입니다.

TTL은 승인 시각부터600초입니다. 만료를 무시하거나 자동 연장하지 않습니다. 다른 mode·scope·prompt-file을 쓰면 키가 달라져 미스가 정상입니다. `simulated`에서 승인한 답을 `live` 실행의 실측답으로 승격하지 않습니다.

## 모델 선택
```powershell
python 01_basic/07_model_routing/main.py --source live --allow-paid --mode fast
# 두 모델 접근권과 예산을 확인한 뒤 응용·심화에서 선택 실행
python 02_intermediate/07_model_routing/main.py --source live --allow-paid --action compare
```
quality 미설정은 `not_run`입니다. fast로 자동 대체하지 않습니다. 모델 응답비교에서는 앱 응답캐시를 사용하지 않습니다.

## 일일프로젝트
```powershell
python 01_basic/08_daily_project/main.py --source live --allow-paid
```
H01은Streaming, H02·H03은완료형 호출입니다. 처음3개를기록하며실패시모든후속응답을조작하지않습니다. 인증·할당량같은실패는나머지호출을중단합니다.

출력된 H01 run.json을검토한뒤같은08 경로에서 `--action reuse`, `--action changed`를사용합니다. 04에서실패사례한건의분류·전송수를설명하면완료입니다. 키가없을때는 `--source simulated`로코드분기를확인하되실제실습완료와구분합니다.

## 사람 검토 반영 최종 표
```powershell
python tools/summarize.py --outputs "01_basic/08_daily_project/outputs"
```
기존 CSV는 최초 관찰표이므로 사람이검토한뒤에는위명령으로새표를만듭니다. 이명령도 API를호출하지않습니다. 원래표를덮어쓰지않습니다.

## 본인 Day21 Prompt 재사용
`--prompt-file "고정한_instructions.txt"`를실제생성·캐시재조회에동일하게사용합니다. `tools/import_day21_prompt.py`로Day21의 frozen_bundle.json을 변환할수있습니다. 개인수정Prompt를사용하면기준본과다른실험이며해시로구분합니다.


### 고정 Prompt 가져오기 명령
```powershell
python tools/import_day21_prompt.py --bundle "Day21에서_고정한_frozen_bundle.json" --variant B --out "data/my_instructions.txt"
python 01_basic/02_structured_output/main.py --source live --allow-paid --prompt-file "data/my_instructions.txt"
```
A를 최종 선택했다면 `--variant A`로 바꿉니다. 변환기는 질문·문맥만 user input으로 이동하고 선택한 예제·규칙·출력 계약을 보존합니다.
사용자 변경 템플릿을 안전하게 구분할 수 없으면 중단하므로, 원본을 보존하고 강사와 직접 분리합니다.

### 설치 후 오프라인 점검
```powershell
python tools/selfcheck.py
python -m pip install -r requirements-test.txt
python -m pytest -q tests
```
위 검사는 네트워크를 사용하지 않으며 실제 인증을 확인하지 않습니다.
공통 제공 체크포인트를 검사하므로 TODO가 미완성인 수강생도 테스트가 통과할 수 있습니다. **교시 완료는 해당 main.py의 실행 결과로 별도 확인**합니다.
