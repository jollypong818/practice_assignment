"""제공 데이터·분할·전처리 계약 테스트. 역할 폴더에서 python tools/test_contracts.py"""
from pathlib import Path
import sys,unittest,tempfile,shutil
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.model_selection import cross_validate
from course_support import load_data,check_features,build,snapshot,FEATURES,NUM
from model_config import make_folds,new_classifier,fold_table

class ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=load_data()
        cls.model=build(new_classifier('Tree')).fit(cls.d.X_train,cls.d.yc_train)
    def test_lengths(self):
        self.assertEqual([len(self.d.X_train),len(self.d.X_valid),len(self.d.test_ids)],[60,20,20])
    def test_features(self): self.assertEqual(list(self.d.X_train.columns),FEATURES)
    def test_class_counts(self): self.assertEqual(self.d.yc_train.value_counts().sort_index().tolist(),[42,18])
    def test_no_heldout_X_y(self):
        self.assertFalse(hasattr(self.d,'X_test'));self.assertFalse(hasattr(self.d,'yc_test'))
    def test_no_id_overlap(self):
        a=set(self.d.X_train.index);b=set(self.d.X_valid.index);c=set(self.d.test_ids)
        self.assertEqual(len(a|b|c),100);self.assertFalse(a&b or a&c or b&c)
    def test_xy_alignment(self):
        self.assertTrue(self.d.X_train.index.equals(self.d.yc_train.index));self.assertTrue(self.d.X_train.index.equals(self.d.yr_train.index))
    def test_missing_feature(self):
        with self.assertRaises(ValueError):check_features(self.d.X_valid.drop(columns=['priority']))
    def test_forbidden_feature(self):
        with self.assertRaises(ValueError):check_features(self.d.X_valid.assign(status='ok'))
    def test_empty(self):
        with self.assertRaises(ValueError):check_features(self.d.X_valid.iloc[:0])
    def test_duplicate_id(self):
        with self.assertRaises(ValueError):check_features(pd.concat([self.d.X_valid,self.d.X_valid]))
    def test_infinity(self):
        bad=self.d.X_valid.copy();bad.iloc[0,0]=np.inf
        with self.assertRaises(ValueError):check_features(bad)
    def test_negative(self):
        bad=self.d.X_valid.copy();bad.iloc[0,0]=-1
        with self.assertRaises(ValueError):check_features(bad)
    def test_empty_category_string(self):
        bad=self.d.X_valid.copy();bad.iloc[0,2]=' '
        with self.assertRaises(ValueError):check_features(bad)
    def test_train_all_missing(self):
        bad=self.d.X_train.copy();bad['input_chars']=np.nan
        with self.assertRaises(ValueError):check_features(bad,training=True)
    def test_inference_missing_allowed(self):
        new=self.d.X_valid.iloc[:2].copy();new[NUM]=np.nan
        z=self.model['pre'].transform(check_features(new))
        self.assertEqual(z.shape,(2,8));self.assertTrue(np.isfinite(z).all())
    def test_unknown_category(self):
        new=self.d.X_valid.iloc[:2].copy();new['task_type']='translation';new['priority']='urgent'
        before=snapshot(self.model['pre']);z=self.model['pre'].transform(check_features(new))
        self.assertEqual(z.shape,(2,8));np.testing.assert_array_equal(z[:,2:],0)
        self.assertEqual(snapshot(self.model['pre']),before)
    def test_train_median(self):np.testing.assert_allclose(self.model['pre'].named_transformers_['num']['imputer'].statistics_,[1315,3])
    def test_cv_ids(self):
        folds=make_folds(self.d.X_train,self.d.yc_train)
        seen=[]
        for a,b in folds:
            self.assertEqual((len(a),len(b)),(48,12));self.assertFalse(set(a)&set(b));seen.extend(b)
        self.assertEqual(sorted(seen),list(range(60)))
    def test_cv_label_minimum(self):
        y=self.d.yc_train.copy();y[:]=0;y.iloc[:4]=1
        with self.assertRaises(ValueError):make_folds(self.d.X_train,y)
    def test_cv_single_class(self):
        y=self.d.yc_train.copy();y[:]=0
        with self.assertRaises(ValueError):make_folds(self.d.X_train,y)
    def test_cv_alignment_failure(self):
        with self.assertRaises(ValueError):make_folds(self.d.X_train,self.d.yc_train.iloc[::-1])
    def test_each_fold_statistics(self):
        folds=make_folds(self.d.X_train,self.d.yc_train)
        result=cross_validate(build(new_classifier('Tree')),self.d.X_train,self.d.yc_train,
            cv=folds,scoring='f1',return_estimator=True,n_jobs=1,error_score='raise')
        for (a,b),m in zip(folds,result['estimator']):
            np.testing.assert_allclose(m['pre'].named_transformers_['num']['imputer'].statistics_,
                self.d.X_train.iloc[a][NUM].median().to_numpy())
    def test_split_duplicate_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            d=Path(tmp);shutil.copytree(ROOT/'data',d,dirs_exist_ok=True)
            m=pd.read_csv(d/'split_manifest.csv');m.loc[1,'request_id']=m.loc[0,'request_id'];m.to_csv(d/'split_manifest.csv',index=False)
            with self.assertRaises(ValueError):load_data(d)
    def test_order_mismatch_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            d=Path(tmp);shutil.copytree(ROOT/'data',d,dirs_exist_ok=True)
            m=pd.read_csv(d/'split_order.csv');m.loc[0,'position']=999;m.to_csv(d/'split_order.csv',index=False)
            with self.assertRaises(ValueError):load_data(d)
    def test_heldout_poison_no_effect(self):
        # 보관test의 feature/target를 읽고 검증·학습하지 않는지 직접 확인합니다.
        with tempfile.TemporaryDirectory() as tmp:
            d=Path(tmp);shutil.copytree(ROOT/'data',d,dirs_exist_ok=True)
            raw=pd.read_csv(d/'requests.csv');mask=raw['request_id'].isin(self.d.test_ids)
            raw.loc[mask,['input_chars','allowed_tools','elapsed_ms','failed']]=np.nan
            raw.loc[mask,['task_type','priority','status']]='HELDOUT_POISON'
            raw.to_csv(d/'requests.csv',index=False)
            other=load_data(d)
            pd.testing.assert_frame_equal(other.X_train,self.d.X_train)
            pd.testing.assert_series_equal(other.yc_train,self.d.yc_train)
            fresh=build(new_classifier('Tree')).fit(other.X_train,other.yc_train)
            np.testing.assert_array_equal(fresh.predict(other.X_valid),self.model.predict(self.d.X_valid))

if __name__=='__main__':unittest.main(verbosity=2)
