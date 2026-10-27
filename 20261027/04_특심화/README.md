# 2026-10-27 · Day7 트리·앙상블·교차검증 실습

## 시작 순서
1. 이 역할 폴더 전체를 압축 해제하고 VS Code에서 **폴더 열기**로 엽니다. ZIP 안에서 직접 실행하지 않습니다.
2. 전날 가상환경을 재사용하거나 Python3.13으로 새 가상환경을 만듭니다. 기존 환경을 쓰면 아래 venv생성은 생략합니다.
3. `python check_env.py`로 XGBoost CPU 실행까지 확인합니다.
4. 실습01~06의 기본필수를 먼저 진행합니다. 실습07~08은 같은 프로젝트입니다.

### Windows PowerShell
```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe check_env.py
.venv\Scripts\python.exe "ex01_tree/01_기본필수/main.py"
```
활성화 정책 때문에 Activate.ps1이 막혀도 위처럼 가상환경 Python을 직접 사용하면 됩니다. 시스템 실행정책을 바꾸지 않습니다.
VS Code에서는 Python: Select Interpreter로 `.venv\Scripts\python.exe`를 선택하세요.

### macOS / Linux
```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python check_env.py
.venv/bin/python ex01_tree/01_기본필수/main.py
```
이하 `python`은 선택한 가상환경의 Python을 뜻합니다. Windows/macOS 직접 실행 검증은 하지 않았습니다.

## 환경
검증 조합은 Python3.13.5 + requirements-lock.txt의 고정 버전입니다. 커리큘럼의 다른 패키지 버전을 검증했다고 간주하지 않습니다.
XGBoost는 CPU `hist`, `device=cpu`, `n_jobs=1`을 사용합니다. CUDA/추가 계정/API키/유료서비스가 필요하지 않습니다.
의존 패키지 설치에는 인터넷이 필요합니다. 설치 완료 후 실습 실행은 오프라인으로 가능합니다.
XGBoost import가 실패하면 오류 전문과 Python/OS 버전을 강사에게 전달하세요. 임의로 다른 모델로 바꾸고 같은 점수라고 보고하지 않습니다.

## 8개 실습
|번호|내용|교시 실습시간|
|---|---|---:|
|01|분류·회귀 트리 경로와 잎|20분|
|02|깊이·잎 제약과 과적합 진단|25분|
|03|Forest 분류·회귀·확률 평균|25분|
|04|MDI·순열 중요도와 해석|25분|
|05|XGBoost 손실·지표·설정|20분|
|06|train 내부5-fold·통계감사|25분|
|07|앙상블 비교 프로젝트 통합|25분|
|08|같은 프로젝트 최종검증·보고서|35분|
총 실습·리뷰200분. 매 실습 기본필수/응용/심화3단계, 총24단계이며 당일 모두 수행하라는 뜻은 아닙니다.

## 데이터·평가 계약
원본100건은 수업용 합성자료이며 실제 Agent 성능을 의미하지 않습니다.
Day5/6의 `requests.csv`, `split_manifest.csv`, `split_order.csv`를 그대로 재사용합니다.
분할은 train60/valid20/test20. `split_order.csv`를 무시하거나 CSV 행을 정렬하면 수업 재현값이 달라질 수 있습니다.
입력은 input_chars/allowed_tools/task_type/priority4열. failed는 분류정답, elapsed_ms는 회귀정답입니다. status/retry_count/elapsed_ms/failed/request_id를 입력특성으로 넣지 않습니다.

오늘의 CV는 **train60 내부**의5-fold(학습48/평가12)입니다. Pipeline 전체를 전달해 각 fold 안에서 전처리도 학습합니다.
분류는 StratifiedKFold, 회귀는 KFold, shuffle=True/seed42. 출력 `score`는 fold평가 점수입니다.
`cross_validate`의 반환키 `test_score`는 보관test20이 아닙니다. 보고서에서는 `fold`/`CV`로 표시합니다.
최종 기본비교는 사전 고정 후보를 CV평균으로 선택합니다. 동점은 선언순서. valid는 진단을 위한 별도 열입니다.
이전 날 valid에서 탐색했고 오늘도 여러 결과를 확인하므로 valid는 독립적인 최종 평가가 아닙니다. CV최고점 또한 탐색·선택 편향을 포함합니다.
원본 로더가 파일 전체를 읽더라도 **test의 X/y는 반환하지 않으며**, fit/transform/predict/score/중요도에 넣지 않습니다. test에 대해 확인하는 것은 ID·분할 무결성뿐입니다.

## 과제와 자동 확인
단계별 README의 함수 계약/TODO를 구현합니다. 주요 출력은 `outputs/`, 확인용 기준은 `expected_outputs/`입니다.
```powershell
python tools/check_exercise.py --exercise 1 --level basic
python "ex07_project/01_기본필수/day7_ensemble/main.py"
python "ex08_verify/01_기본필수/verify.py"
```
프로젝트 폴더에서 `python -m unittest -v test_project.py`로12개 계약 테스트를 수행할 수 있습니다.
심화 자동검사는 `tools/test_contracts.py` 및 같은 단계의08 안내를 참고하세요.
완성한 코드 전체 재검사는 `python tools/verify_all.py`입니다. 미완성 단계는 실패합니다. 개별실습 검사를 우선 사용합니다.

## 파일 안내
- `data/`: 원본·분할·순서·새 입력·실패 입력·미전처리 train/valid 체크포인트.
- `course_support.py`, `model_config.py`: 이전 단원 로더/전처리·고정모델설정·출력 도우미. 학습모델/정답 결과를 읽지 않습니다.
- `ex01_...`~`ex06_...`: 단계별 main.py, README, 학습기록, 기준출력.
- `ex07_project/.../day7_ensemble/`: 독립 복사 가능한 최종 프로젝트. 기본필수4개 분류, 응용6개분류+6개회귀, 심화통계/탐색검사.
- `ex08_verify/`: 동일단계07 결과를 검증하고 보고서를 마무리합니다.
- `bonus_early_stopping/`: 선택 확장. 내부42/18 조기종료 후 새 train60 재학습. 기본XGB80과 별도 기록.

## 안전·제출
데이터/기준출력을 직접 수정하지 않습니다. 잘못된 입력 시험은 복사본/임시폴더를 사용합니다.
모델 직렬화(joblib/pickle)는 생성한 본인만 신뢰할 수 있는 로컬 파일만 복원합니다. 본 자료에 사전학습 모델 파일은 넣지 않았습니다.
응용 프로젝트는 자체 생성한 파일을 같은 프로세스에서 확인합니다. 별도 복원은 `python restore_check.py --trust-local-models`로 명시적 확인 후 수행합니다.
비밀키·실제 개인정보·`.venv`·모델 파일을 Git에 올리지 않습니다. 합성 CSV와 보고서·작은결과표는 검토 후 추적할 수 있습니다.
Git의 commit은 원격 업로드가 아닙니다. 제출은 코드·결과표·보고서·검사증거·Git 이력이며, 과목 최종실습평가는10/28입니다.
