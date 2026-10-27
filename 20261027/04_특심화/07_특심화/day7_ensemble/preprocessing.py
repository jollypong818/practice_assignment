"""특성 선택·전처리·모델 생성. 아직 학습하지 않은 Pipeline을 만듭니다."""
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from course_support import NUM, CAT, FEATURES
from model_config import new_classifier, new_regressor

def make_preprocessor(scale='none'):
    """num: median (+standard 선택), cat: 최빈값 -> dense OneHot(ignore)."""
    # TODO D7-07-P1: 위 계약과 README를 읽고 구현하세요.
    raise NotImplementedError("TODO D7-07-P1")

def candidates(include_previous=False, task='classification'):
    """기본 분류 Dummy/Tree/Forest/XGB. 응용에 Logistic/KNN3, 회귀는 6후보.
    Dummy와 전날 모델만 scale=standard. 각 후보는 서로 다른 새 객체여야 합니다.
    """
    # TODO D7-07-P2: 위 계약과 README를 읽고 구현하세요.
    raise NotImplementedError("TODO D7-07-P2")
