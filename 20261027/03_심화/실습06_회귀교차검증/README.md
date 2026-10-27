# 실습 06 · 회귀 5-fold

**목표:** 음수 scorer, 양의 오차, fold 평균을 구분합니다.

이 README가 있는 폴더를 VS Code로 엽니다. 입력·예상 결과·출력은 이 실습 안에 있어 다른 실습 완료 여부에 의존하지 않습니다.

**열 파일:** `main.py`  
**완성할 위치:** `C06a`, `C06b`

- **C06a**: 회귀 정답으로 neg_root_mean_squared_error 점수를 구하세요.
- **C06b**: 음수 scorer 값을 양수 RMSE로 되돌리세요.

**힌트:** negative는 NumPy 배열이므로 -negative로 전체 원소의 부호를 바꿀 수 있습니다.

```powershell
python main.py
```

**실제 정답 실행으로 확인한 출력**

```text
model  CV_RMSE_ms  CV_std_ms
  Tree     599.635     96.116
Forest     624.011     96.974
   XGB     655.793     92.170
CV_RMSE는 fold별 RMSE의 단순 평균입니다. 전체 예측을 합친 RMSE와 다를 수 있습니다.
```

**생성 파일:** `outputs/regression_cv.csv`, `outputs/cv_scores.csv`

**완료 기준:** TODO가 실제 계산·모델 호출에 사용되고, 위 출력 및 단위·행 수가 일치하며 다음 질문에 답할 수 있어야 합니다. 반올림 끝자리 차이만 있다면 검증 버전부터 확인합니다.

- 분류에서 쓰던 StratifiedKFold가 아니라 KFold를 쓰는 이유는 무엇인가요?
- 단위 ms를 표에 남겨야 하는 이유는 무엇인가요?

`expected/`는 비교 자료, `outputs/`는 직접 생성하는 결과입니다. expected를 입력으로 읽지 않습니다. test20은 모델에 넣지 않습니다.

## 구조와 재사용 코드

`preprocessing.py`의 `build_model`은 제공 함수입니다. 각 호출마다 새 전처리기와 모델을 만들며, 호출만으로 학습하지 않습니다. `main.py`의 fit 또는 CV 내부에서만 학습합니다.

**이 단계의 코딩 수준은 이전 자료의 응용 수준입니다.** 폴더 구조를 익히기 위해 역할을 나누었을 뿐 복잡한 예외처리·검사 코드를 구현하지 않습니다.
