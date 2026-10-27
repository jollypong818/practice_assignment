# 실습 05 · 학습률·회차 조합 통제 · 심화

PPT 44~50 | 교시 실습 20분 | 기본필수 후 선택 확장

## 목표
2개 사전 조합 외에는 탐색하지 않고 진단으로 기록한다.

## 구현 위치와 계약
### `main.py` → `compare_schedules` · D7-05-H1
learning_rate, n_estimators, train_F1, valid_F1, valid_logloss의 표 반환.

## 실행
역할 폴더 루트에서 실행하거나 이 폴더로 이동해 `python main.py`를 실행합니다.
```powershell
python "ex05_xgboost/03_심화/main.py"
```

## 입력과 파일 위치
역할 폴더의 data/ 원본·split_manifest·split_order를 사용합니다. 실습01은 코드에 있는6행 원리 입력입니다. 실습08은 동일 단계의07 결과를 읽습니다.
앞 단원 완료 파일을 필수 입력으로 요구하지 않습니다. 공통 로더/전처리는 Day5~6 재사용 코드로 제공합니다.

## 결과와 완료 기준
실제 계산 결과는 `outputs/`, 기준 출력은 `expected_output.txt`와 `expected_outputs/`에 있습니다.
`result.json`, `schedule_diagnostics.csv`
숫자는 결과 파일에서 계산해야 합니다. 기준 파일을 읽어 정답을 반환하거나 숫자를 하드코딩하지 않습니다.
수치 허용오차는 일반적으로0.001(ms 포함), 비율은 상대오차1e-6도 함께 사용합니다. 다른 라이브러리/운영체제에서 순위가 다르면 설정과 버전을 먼저 기록합니다.

## 구현 힌트
원본 categorical DataFrame을 바로 XGBoost에 넘기지 말고 제공 전처리를 통과시킵니다. CPU hist, n_jobs1을 유지합니다. binary:logistic 학습과 logloss 진단, F1 선택은 서로 다릅니다.

## 3단계 선택 원칙
8개 실습마다 기본필수1개를 먼저 수행합니다. 응용·심화를 모두 당일 완료할 필요는 없습니다.
실습07~08은 같은 프로젝트를 이어 씁니다. 프로젝트를 두 번 새로 만들지 않습니다.

## 학습기록
`학습기록.md`에 실제 결과와 판단 근거를 적습니다. 자동검사는 계산을 확인할 뿐 해석을 대신하지 않습니다.

완료 확인: 역할 루트에서 `python tools/check_exercise.py --exercise 5 --level advanced`

`NotImplementedError`는 미완성 TODO의 표시입니다. 함수를 완성한 후 다시 실행하세요.
