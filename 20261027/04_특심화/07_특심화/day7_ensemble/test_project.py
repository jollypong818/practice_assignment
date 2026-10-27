"""제공 회귀방지 테스트. 완료 후 python -m unittest -v test_project.py"""
import unittest
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from course_support import load_data, check_features, snapshot, FEATURES
from preprocessing import candidates
from evaluate import choose_by_cv
from checks import verify_development_data, boundary_checks
from model_config import make_folds
import pandas as pd

class ProjectTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=load_data()
        cls.m=candidates()['Tree'].fit(cls.d.X_train,cls.d.yc_train)
    def test_split(self):
        self.assertTrue(verify_development_data(self.d)['disjoint'])
    def test_feature_count(self):
        self.assertEqual(self.m['pre'].transform(self.d.X_valid).shape,(20,8))
    def test_no_test_returned(self):
        self.assertFalse(hasattr(self.d,'X_test'));self.assertFalse(hasattr(self.d,'y_test'))
    def test_medians(self):
        np.testing.assert_allclose(self.m['pre'].named_transformers_['num']['imputer'].statistics_,[1315,3])
    def test_boundary(self):
        self.assertTrue(boundary_checks(self.m,self.d)['missing_column_blocked'])
    def test_extra_column(self):
        with self.assertRaises(ValueError): check_features(self.d.X_valid.assign(status='ok'))
    def test_empty(self):
        with self.assertRaises(ValueError): check_features(self.d.X_valid.iloc[:0])
    def test_statistics(self):
        before=snapshot(self.m['pre']);self.m.predict(self.d.X_valid)
        self.assertEqual(before,snapshot(self.m['pre']))
    def test_cv(self):
        folds=make_folds(self.d.X_train,self.d.yc_train)
        self.assertEqual(len(folds),5)
        self.assertTrue(all(len(a)==48 and len(b)==12 and not set(a)&set(b) for a,b in folds))
    def test_choice_ignores_valid(self):
        t=pd.DataFrame({'model':['A','B'],'CV_mean':[0.6,0.5],'valid_F1':[0.1,1.0]})
        self.assertEqual(choose_by_cv(t),'A')
    def test_candidate_freshness(self):
        a=candidates();self.assertIsNot(a['Tree']['pre'],a['Forest']['pre'])
    def test_training_missing_column(self):
        bad=self.d.X_train.copy();bad['input_chars']=np.nan
        with self.assertRaises(ValueError): check_features(bad,training=True)

if __name__=='__main__': unittest.main()
