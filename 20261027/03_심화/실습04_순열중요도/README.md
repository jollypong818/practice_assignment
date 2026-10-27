# 실습 04 · 순열 중요도

**목표:** 8개 MDI 값과 4개 순열 값을 같은 단위로 혼동하지 않습니다.

이 README가 있는 폴더를 VS Code로 엽니다. 입력·예상 결과·출력은 이 실습 안에 있어 다른 실습 완료 여부에 의존하지 않습니다.

**열 파일:** `main.py`  
**완성할 위치:** `C04`

- **C04**: 학습한 Pipeline의 valid 순열 중요도를 F1 기준으로 구하세요.

**힌트:** permutation_importance에는 이미 학습한 model과 원본 X_valid를 넣습니다.

```powershell
python main.py
```

**실제 정답 실행으로 확인한 출력**

```text
MDI: 변환 후 8 열 / 순열: 원본 4 열
      feature  mean_F1_drop  repeat_std
  input_chars        0.0678      0.1361
allowed_tools        0.0542      0.1185
    task_type        0.1737      0.0990
     priority       -0.0206      0.1801
음수는 이 valid 표본에서 섞었을 때 점수가 높아졌다는 뜻입니다. 인과관계는 아닙니다.
```

**생성 파일:** `outputs/mdi_importance.csv`, `outputs/permutation_importance.csv`

**완료 기준:** TODO가 실제 계산·모델 호출에 사용되고, 위 출력 및 단위·행 수가 일치하며 다음 질문에 답할 수 있어야 합니다. 반올림 끝자리 차이만 있다면 검증 버전부터 확인합니다.

- 평균 감소량이 음수인 열은 어떻게 설명하나요?
- 이 결과로 특성을 골라버리면 valid를 선택에 사용한 것인가요?

`expected/`는 비교 자료, `outputs/`는 직접 생성하는 결과입니다. expected를 입력으로 읽지 않습니다. test20은 모델에 넣지 않습니다.

## 구조와 재사용 코드

`preprocessing.py`의 `build_model`은 제공 함수입니다. 각 호출마다 새 전처리기와 모델을 만들며, 호출만으로 학습하지 않습니다. `main.py`의 fit 또는 CV 내부에서만 학습합니다.

**이 단계의 코딩 수준은 이전 자료의 응용 수준입니다.** 폴더 구조를 익히기 위해 역할을 나누었을 뿐 복잡한 예외처리·검사 코드를 구현하지 않습니다.
