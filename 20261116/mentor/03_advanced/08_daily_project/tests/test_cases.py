"""자신의 심화 구현을 검사합니다. 실제 모델 품질 테스트가 아닙니다."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE))
sys.path.insert(0,str(HERE.parents[1]))
from workflow import choose_bundle, choose_cases, make_report
from coursekit.experiments import prepare_experiment, review_experiment


def test_project_no_fake_observation(tmp_path):
    bundle=choose_bundle()
    cases=choose_cases()
    assert [c["case_id"] for c in cases]==["H01","H02","H03"]
    folder=tmp_path/"holdout"
    prepare_experiment(folder,bundle,cases)
    report=make_report(review_experiment(folder))
    assert report["project"]["first_target"]==6
    assert report["project"]["not_run"]==6
    assert report["project"]["human_pending"]==6
    assert not list(folder.rglob("raw.txt"))
