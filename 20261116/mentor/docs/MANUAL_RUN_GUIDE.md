# 실제 A/B 응답 등록 — 05와 08 공통

## 1. 먼저 Prompt를 준비합니다
선택 수준의 05 폴더에서 TODO를 완성한 뒤 실행합니다.
```powershell
python main.py prepare --run dev_01
```
`outputs/dev_01/prompts/D01_A_r1.txt` 등 6개(응용·심화 12개)가 생깁니다.
아직 `raw.txt`는 없습니다. 이는 정상적인 **미실행 상태**입니다.
재실행은 `--run dev_02`처럼 새 이름을 사용합니다. 기존 폴더 삭제로 실패 이력을 없애지 않습니다.

## 2. 새 대화마다 한 입력만 실행합니다
A와 B의 Prompt를 각각 새 대화에 그대로 입력합니다. A 대화에 B를 이어 묻지 않습니다.
같은 표시 모델과 가능한 동일 조건을 사용합니다. 실제 표시 이름·날짜·도구·개인화 여부를 기록합니다.
UI에서 제어할 수 없는 값은 **미확인**입니다. 화면 결과를 동일 API 모델의 결과로 단정하지 않습니다.
모델의 **첫 응답**을 고치거나 JSON 부분만 잘라내지 말고 UTF-8 txt로 보존합니다.
코드 블록이 붙었으면 코드 블록까지 포함해 저장합니다. 검사기가 json_error로 판단해도 원문을 먼저 보존합니다.

## 3. 첫 응답 등록
05 폴더에서 `incoming` 폴더를 만들고 `D01_A_r1.txt`에 응답을 저장합니다.
```powershell
python ../../tools/record_manual.py --run-dir outputs/dev_01 --slot D01_A_r1 --raw-file incoming/D01_A_r1.txt --model-label "화면의 실제 표시 이름" --conditions "새 대화, 도구 미사용, 개인화 미확인"
```
관찰 시각을 알고 있다면 `--observed-at "2026-11-16T14:35:00+09:00"`을 추가합니다.
모르면 observed_at은 null로 두고 **파일 등록 시각(recorded_at)**만 자동 기록됩니다.
원문과 메타데이터는 `responses/D01_A_r1/`에 저장됩니다. 이미 기록한 원문은 덮어쓸 수 없습니다.
다른 슬롯도 같은 방식으로 저장합니다. run·slot·원문 파일을 서로 맞추세요.

## 4. 거절·중단·실행 실패도 남깁니다
모델의 별도 거절을 `insufficient_context`로 꾸며 넣지 않습니다.
```powershell
python ../../tools/record_manual.py --run-dir outputs/dev_01 --slot D03_A_r1 --state refused --raw-file incoming/D03_A_r1.txt --reason "실제 화면에서 거절을 관찰" --model-label "실제 표시 이름"
```
`--state incomplete`는 출력 중단, `--state failed`는 실행 실패 기록입니다. 실패 사유는 비밀 값 없이 적습니다.
아예 실행하지 못했다면 raw를 만들지 않습니다. `meta.json`의 not_run을 유지하고 reason에 이유만 씁니다.

## 5. 로컬 검증과 사람 평가
```powershell
python main.py review --run dev_01
```
`first_response.csv`, `all_attempts.json`, `summary.json`, `summary.md`가 만들어집니다.
최초 응답의 문법·Schema·참조/상태를 검사하지만 **답변 내용의 사실성을 자동 판정하지 않습니다.**
`responses/<slot>/human_review.json`을 열고 실제로 확인한 항목만 채웁니다.
```json
{
  "evidence_ok": null,
  "task_ok": null,
  "insufficiency_ok": null,
  "reviewer": "",
  "note": "미평가"
}
```
`true`=기준을 충족, `false`=충족하지 못함, `null`=아직 평가하지 않음입니다.
평가할 때 reviewer와 **실제 인용 본문을 읽은 근거**를 note에 적고 review를 다시 실행합니다.
예: 출처101은 파일 보관 위치만 설명하므로 서버 실행 위치의 주장을 뒷받침하지 못합니다.
정보가 없을 때 멈추는 것은 적절하지만 답할 자료가 있는데 무조건 부족이라고 하면 질문 대응 실패입니다.
재시도 응답에는 첫 응답의 사람 평가를 복사하지 않습니다. 별도 검토가 필요하다고 결과에 표시됩니다.

## 6. 형식 오류일 때만 수정 응답 한 번
review가 json_error 또는 schema_error를 확인하면 `responses/<slot>/repair_prompt.txt`를 만듭니다.
**같은 질문·지식·계약과 안전한 오류 요약**만 들어 있으며 이전 응답·예외 전문을 붙이지 않습니다.
이 문구를 다시 모델에 보내 실제 수정 응답을 받으면 `incoming/..._attempt2.txt`에 보존합니다.
```powershell
python ../../tools/record_manual.py --run-dir outputs/dev_01 --slot D01_A_r1 --raw-file incoming/D01_A_r1_attempt2.txt --attempt 2 --model-label "같은 실제 표시 이름"
python main.py review --run dev_01
```
unknown_source·duplicate_source·status_rule·정상 정보 부족·거절은 자동 형식 재시도 대상이 아닙니다.
두 번째도 실패하면 중단합니다. 성공할 때까지 반복하지 않습니다.
**첫 응답 점수와 수정 후 회복을 합쳐서 발표하지 않습니다.**

## 7. 최종 프로젝트로 이어가기
08 폴더에서 05의 고정 입력을 사용합니다. 아래 경로는 **08 폴더에서 실행할 때**의 상대 경로입니다.
```powershell
python main.py prepare --run holdout_01 --bundle ../05_ab_evaluation/outputs/dev_01/frozen_bundle.json
```
H01~H03을 같은 방식으로 실행·등록합니다. 위 명령들의 `dev_01`을 `holdout_01`, D 슬롯을 H 슬롯으로 바꿉니다.
05가 미완성이면 `--bundle`을 생략해 제공 체크포인트로 시작합니다. 이때 D에서 개선했다고 주장하지 않습니다.
H를 보고 수정하고 싶다면 새 버전으로 분리하고 **새 확인 질문 세트가 필요**하다는 한계를 기록합니다.
