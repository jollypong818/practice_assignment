# 선택 심화 · 조기 종료를 안전하게 적용하기
PPT 82~84쪽 / E11·E12·E21. 8교시 필수 과제와 별개인 확장입니다.

`python bonus_early_stopping/main.py`

1. `inner_preprocess`를 완성합니다. train60만 42/18로 분리하며 valid20/test20을 넣지 않습니다.
2. 전처리는 inner42에서 fit하고 stop18은 transform만 합니다.
3. `fit_early_stop`를 완성합니다. raw DataFrame eval_set이 Pipeline을 자동 통과한다고 가정하지 않습니다.
4. best_iteration+1회차를 고정하고 새 전처리기·새 모델을 train60으로 학습합니다.

예상: inner42/stop18, 중앙값 [1338,3], best_iteration63 → 64회차, 실행79회차.
stop logloss 약0.4171은 F1 최적값과 같다는 뜻이 아닙니다. 코드/버전이 달라지면 회차는 달라질 수 있습니다.
outputs/result.json과 learning_curve.csv, inner/stop ID를 남깁니다. 기본 XGB80 결과를 덮어쓰지 않습니다.

질문: 외부 교차검증과 결합한다면 각 outer-fold 학습 부분에서 다시 inner/stop을 나눠야 하는 이유는 무엇인가요?
