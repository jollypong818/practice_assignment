# 실습 08 · 최종 검증·보고서·시연 · 심화

PPT 73~79 | 교시 실습 35분 | 기본필수 후 선택 확장

## 목표
같은 실습07 결과를 검증하고 선택 근거와 한계를 본인 말로 작성한다.

## 구현 위치와 계약
### `verify.py` → `verify_cv_table` · D7-08-V1
모델·task마다 fold1~5,48/12,유한점수, 분류F1[0,1]/회귀RMSE>=0 검사.

### `verify.py` → `verify_predictions` · D7-08-V2
각 모델/task당 valid20개 순서, 실제 정답 일치, test ID 미포함 검사.

## 실행
먼저 실습07을 실행합니다.
```powershell
python "ex07_project/03_심화/day7_ensemble/main.py"
python "ex08_verify/03_심화/verify.py"
```

## 입력과 파일 위치
역할 폴더의 data/ 원본·split_manifest·split_order를 사용합니다. 실습01은 코드에 있는6행 원리 입력입니다. 실습08은 동일 단계의07 결과를 읽습니다.
앞 단원 완료 파일을 필수 입력으로 요구하지 않습니다. 공통 로더/전처리는 Day5~6 재사용 코드로 제공합니다.

## 결과와 완료 기준
실제 계산 결과는 `outputs/`, 기준 출력은 `expected_output.txt`와 `expected_outputs/`에 있습니다.
`classification_comparison.csv`, `cv_scores.csv`, `feature_importance.csv`, `fold_manifest.csv`, `fresh_process_restore.json`, `persistence_check.json`, `regression_comparison.csv`, `run_summary.json`, `separate_tree_grid.csv`, `separate_tree_grid.json`, `submission_check.json`, `validation_predictions.csv`
숫자는 결과 파일에서 계산해야 합니다. 기준 파일을 읽어 정답을 반환하거나 숫자를 하드코딩하지 않습니다.
수치 허용오차는 일반적으로0.001(ms 포함), 비율은 상대오차1e-6도 함께 사용합니다. 다른 라이브러리/운영체제에서 순위가 다르면 설정과 버전을 먼저 기록합니다.

## 구현 힌트
07의 outputs를 그대로 검증합니다. CV평균만 보고 선택하며 valid 최고 모델로 결론을 바꾸지 않습니다. 보고서는 숫자뿐 아니라 FP/FN 사례의 request_id와 예상 업무 비용을 적습니다.

## 3단계 선택 원칙
8개 실습마다 기본필수1개를 먼저 수행합니다. 응용·심화를 모두 당일 완료할 필요는 없습니다.
실습07~08은 같은 프로젝트를 이어 씁니다. 프로젝트를 두 번 새로 만들지 않습니다.

## 학습기록
`학습기록.md`에 실제 결과와 판단 근거를 적습니다. 자동검사는 계산을 확인할 뿐 해석을 대신하지 않습니다.

`NotImplementedError`는 미완성 TODO의 표시입니다. 함수를 완성한 후 다시 실행하세요.

## 새 프로세스 복원 확인
역할 폴더 루트에서, 본인이 방금 생성한 모델임을 확인한 뒤 실행합니다.
```powershell
python "ex07_project/03_심화/day7_ensemble/restore_check.py" --trust-local-models
```
동료에게 모델 파일을 받아 실행하기보다 동료의 소스로 직접 모델을 재생성한 뒤 비교하세요.
