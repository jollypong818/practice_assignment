"""Day27 05_cross_encoder_reranking 실행과 핵심 결과 확인 (네트워크 없이 --offline 테스트)."""
from pathlib import Path
import subprocess,sys,json
import pytest

HERE=Path(__file__).resolve().parents[1]
ROLE_ROOT=next(p for p in HERE.parents if (p/'coursekit').is_dir())

@pytest.mark.parametrize('run_idx',[1])
def test_offline_contract(run_idx):
    # LangChain이 필요한 테스트는 role requirements 설치 후 실행합니다.
    pytest.importorskip("langchain_core")
    res=subprocess.run([sys.executable,str(HERE/'main.py'),'--offline'],
                       cwd=ROLE_ROOT,capture_output=True,text=True,encoding='utf-8')
    assert res.returncode==0,res.stdout+'\n'+res.stderr
    path=HERE/'outputs'/'day27_05_fixture.json'
    assert path.exists(),path
    data=json.loads(path.read_text(encoding='utf-8'))
    assert 'row' in data
    assert data['execution_mode'] in ('fixed_diagnostic_cases','offline_fixture')
    assert set(data['row']['after_ids']).issubset(data['row']['before_ids'])
