"""실습 05 기본필수: train에서 정한 기준을 새 입력에도 적용합니다."""
# scikit-learn의 preprocessing 모듈에서 StandardScaler를 가져온다.
#
# preprocessing은 머신러닝 모델에 데이터를 입력하기 전에 데이터를 가공하는 전처리 작업을 의미한다.
#
# StandardScaler는 데이터의 평균과 표준편차를 이용해 숫자의 크기를 표준화하는 도구이다.
#
# 표준화하는 이유:
# 서로 다른 크기를 가진 숫자들이 거리 계산이나 모델 학습에 불균형한 영향을 주는 문제를 줄이기 위해서이다.
#
# 주의:
# StandardScaler는 성공/실패 등을 예측하는 모델이 아니다.
# 머신러닝에 사용할 데이터를 변환하는 도구이다.
from sklearn.preprocessing import StandardScaler

# train은 학습 데이터이다.
#
# 이 데이터로 평균과 표준편차를 계산하고 앞으로 사용할 표준화 기준을 정한다.
#
# 학습 데이터: 100, 200, 300
#
# 평균 = (100 + 200 + 300) / 3 = 200
# 표준편차 ≈ 81.65
#
# 입력 데이터가 3개이고 특징이 1개이므로 3행 × 1열의 2차원 리스트로 작성한다.
train = [[100], [200], [300]]


# valid는 검증 데이터이다.
#
# 학습 데이터와 분리된 새로운 데이터라고 생각하면 된다.
#
# 중요한 점:
# valid의 평균과 표준편차를 새로 계산하는 것이 아니라 train에서 계산한 기준을 그대로 적용해야 한다.
#
# 이렇게 해야 학습 데이터와 검증 데이터를 동일한 기준으로 비교할 수 있다.
valid = [[400]]

# StandardScaler 객체를 생성한다.
#
# 아직 데이터의 평균이나 표준편차를 계산하지 않았다.
# 표준화에 사용할 도구만 준비한 상태이다.
scaler = StandardScaler()

# fit()은 train 데이터를 분석해서 표준화에 필요한 평균과 표준편차를 계산한다.
#
# 이 문제에서는
# 평균(mean_) = 200
# 표준편차(scale_) ≈ 81.65
#
# 여기서 fit()은 분류나 회귀 모델의 학습과 다르다.
#
# 머신러닝 모델의 fit():
#   예측에 필요한 데이터의 관계나 패턴을 학습한다.
#
# StandardScaler의 fit():
#   데이터를 변환할 때 사용할 통계적 기준을 계산한다.
#
# fit()은 기준을 계산할 뿐, train 데이터 자체를 변환해서 반환하지는 않는다.
scaler.fit(train)  # 제공: 평균과 크기 기준은 train에서만 구합니다.

# transform()은 fit()에서 계산한 기준을 이용해 실제 데이터를 표준화하는 메서드이다.
#
# 이미 train으로 fit()을 수행했으므로 valid에 대해서는 transform()만 사용한다.
#
# valid = 400
# train 평균 = 200
# train 표준편차 ≈ 81.65
#
# 변환 결과 = (400 - 200) / 81.65
#          ≈ 2.449
#
# fit_transform()을 사용하면 valid로 기준을 다시 계산하게 되므로 여기서는 사용하지 않는다.
# 완료 B05: valid를 transform하여 converted에 넣으세요.
# 힌트: 학습은 이미 끝났으므로 fit_transform이 아니라 transform을 씁니다.
converted = scaler.transform(valid)

# scaler.mean_은 fit()으로 계산한 평균을 보여준다.
#
# 학습 데이터의 평균은 200이므로 [200.]이 출력된다.
#
# 배열로 반환하는 이유는 실제 머신러닝에서는
# 여러 특징 각각의 평균을 계산할 수 있기 때문이다.
print("train 기준 평균:", scaler.mean_)
# train 데이터를 표준화해서 출력한다.
#
# 100 → (100 - 200) / 81.65 ≈ -1.225
# 200 → (200 - 200) / 81.65 = 0
# 300 → (300 - 200) / 81.65 ≈ 1.225
#
# round(3)은 소수점 셋째 자리까지 반올림한다.
#
# transform()은 전달받은 데이터의 변환 결과를 반환하며 기존 train 리스트 자체를 수정하지 않는다.
print("train 변환:", scaler.transform(train).round(3))

# valid 데이터의 표준화 결과를 출력한다.
#
# converted에는 scaler.transform(valid)의 결과가 저장되어 있다.
#
# valid 값 400을 train 기준으로 변환하면 약 2.449이다.
print("valid 변환:", converted.round(3))

# valid를 변환한 후에도 scaler의 평균이
# 기존 train 평균인 200으로 유지되는지 확인한다.
#
# transform()은 이미 학습한 기준을 사용하기만 하므로
# scaler.mean_이 변경되지 않는다.
#
# 따라서 여전히 [200.]이 출력된다.
print("변환 후 기준 평균:", scaler.mean_)

# 주의사항:
#
# 1. 검증 데이터에 다시 fit()하지 않는다.
#    학습 데이터에서 정한 기준을 유지해야 하기 때문이다.
#
# 2. StandardScaler는 데이터를 정규분포로 만드는 것이 아니다.
#    평균과 표준편차를 기준으로 숫자를 변환하는 것이다.
#
# 3. 실제 머신러닝에서는 모델 학습 전에
#    train을 fit_transform()으로 변환하고,
#    valid와 test는 transform()으로만 변환한다.