"""고정 데이터·필터·Rerank·API 계약. 수강생 TODO를 호출하지 않습니다."""
from pathlib import Path
import sys
import pytest
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))

def test_access_and_current_filter():
    from coursekit.fixtures import fixture_hits
    visible=fixture_hits('시설',role='learner')
    ids={r['chunk_id'] for r in visible}
    assert 'FAC-102-C1' in ids
    assert 'FAC-110-C1' not in ids  # staff only
    assert 'FAC-111-C1' not in ids  # old version
    assert 'FAC-112-C1' not in ids  # not ready

def test_question_gold_separate():
    from coursekit.io import load_json
    docids={r['chunk_id'] for r in load_json('corpus.json')}
    assert all(set(gold)<=docids for gold in load_json('gold_labels.json').values())

def test_request_role_cannot_be_claimed():
    from pydantic import ValidationError
    from coursekit.api import RagRequest
    with pytest.raises(ValidationError):
        RagRequest.model_validate({'query':'확인','role':'staff'})

def test_ranking_rejects_mismatched_and_nan():
    pytest.importorskip('langchain_core')
    from coursekit.documents import hit_to_document
    from coursekit.fixtures import fixture_hits
    from coursekit.reranking import rerank_documents
    docs=[hit_to_document(row) for row in fixture_hits('시설')[:2]]
    with pytest.raises(ValueError):
        rerank_documents('취소',docs,lambda pairs:[0.1],top_n=2)
    with pytest.raises(ValueError):
        rerank_documents('취소',docs,lambda pairs:[float('nan'),1.0],top_n=2)

def test_dedupe_keeps_source_and_query_names():
    pytest.importorskip('langchain_core')
    from coursekit.documents import hit_to_document
    from coursekit.fixtures import fixture_hits
    from coursekit.multi_query import merge_found
    doc=hit_to_document(fixture_hits('시설')[0])
    out=merge_found([('질문1',[doc]),('질문2',[doc])])
    assert len(out)==1
    assert out[0].metadata['found_by_query']==['질문1','질문2']
    assert out[0].metadata['source_locator']

def test_citation_must_be_in_actual_context():
    from coursekit.llm import WireAnswer,validate_generation
    from types import SimpleNamespace
    item=WireAnswer(status='answered',answer='설명',source_ids=[987654],missing_information='')
    raw=SimpleNamespace(content='완료',response_metadata={'status':'completed'})
    with pytest.raises(ValueError,match='source_not_in_context'):
        validate_generation({'raw':raw,'parsed':item,'parsing_error':None},{42})
