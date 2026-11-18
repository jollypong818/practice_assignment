from __future__ import annotations
import json, sys, hashlib, subprocess
from pathlib import Path
import numpy as np
import pytest

MENTOR=Path(__file__).resolve().parents[1]
ROOT=MENTOR.parent
sys.path.insert(0,str(MENTOR/'common'))
from day23kit.data import (load_knowledge, validate_snapshot, passage_text, query_text,
   E5_MODEL_ID,DIMS, TABLE_NAME)
from day23kit.embedding import (get_encoder,encode_question,encode_passages,validate_vectors)
from day23kit.fixtures import fixture_search, SimulatedEncoder
from day23kit.mathops import cosine_distance
from day23kit import db


def test_html_knowledge_sha256():
    rows=load_knowledge()
    canon=json.dumps(rows,ensure_ascii=False,sort_keys=True,separators=(',',':'))
    sha=hashlib.sha256(canon.encode('utf-8')).hexdigest()
    assert sha==(MENTOR/'verification/HTML_KNOWLEDGE_SHA256.txt').read_text().strip()


def test_frozen_original_knowledge_and_versions():
    a=load_knowledge()
    assert [x['id'] for x in a]==list(range(101,110))
    assert [x['content'] for x in a[:3]]==[
       '실습 파일은 개인 폴더에 보관합니다.',
       '프로젝트 폴더에서 서버를 실행합니다.',
       '오류 메시지와 시도한 작업을 함께 적습니다.']
    assert all(x['source_version']=='knowledge_v1' for x in a[:3])
    assert all(x['source_version']=='knowledge_search_v2' for x in a[3:])
    assert validate_snapshot(a)


def test_duplicate_id_rejected():
    a=load_knowledge();a.append(dict(a[0]))
    with pytest.raises(ValueError,match='중복'):validate_snapshot(a)


def test_missing_field_rejected():
    a=load_knowledge();a[0]['content']=''
    with pytest.raises(ValueError,match='누락'):validate_snapshot(a)


def test_e5_contract():
    r=load_knowledge()[1]
    assert passage_text(r)=='passage: 서버 실행 프로젝트 폴더에서 서버를 실행합니다.'
    assert query_text('어디?')=='query: 어디?'
    assert E5_MODEL_ID=='intfloat/multilingual-e5-small'
    assert DIMS==384


def test_math_known_vector():
    assert cosine_distance([1,0],[0.8,0.6])==pytest.approx(0.2,abs=1e-7)
    assert cosine_distance([1,0],[-1,0])==pytest.approx(2)
    with pytest.raises(ValueError):cosine_distance([0,0],[1,0])


def test_simulated_encoder_labels():
    enc=get_encoder('fixture')
    assert enc.source_mode=='simulated'
    assert 'NOT_E5' in enc.model_id
    assert enc.get_sentence_embedding_dimension()==384
    docs=encode_passages(enc,load_knowledge())
    query=encode_question(enc,'서버는 어디에서 실행하나요?')
    assert docs.shape==(9,384) and query.shape==(384,)
    assert validate_vectors(docs,9).shape==(9,384)
    assert np.linalg.norm(query)==pytest.approx(1,abs=1e-6)


@pytest.mark.parametrize('bad',[
    np.zeros((1,384),dtype=np.float32),
    np.ones((1,128),dtype=np.float32),
    np.full((1,384),np.nan,dtype=np.float32),
    np.ones((1,384),dtype=np.float32)
])
def test_bad_vectors_rejected(bad):
    with pytest.raises(ValueError):validate_vectors(bad,1)


def test_fixture_retrieval_preserves_raw_content():
    result=fixture_search('서버는 어디에서 실행하나요?',3)
    assert result[0]['id']==102
    assert result[0]['content']=='프로젝트 폴더에서 서버를 실행합니다.'
    assert result[0]['source_mode']=='simulated'
    assert all('title' in x and 'source_version' in x for x in result)


def test_fixture_category_empty_and_k():
    r=fixture_search('서버는 어디에서 실행하나요?',9,category='course')
    assert len(r)==3 and all(x['category']=='course' for x in r)
    with pytest.raises(ValueError):fixture_search('서버',True)
    with pytest.raises(ValueError):fixture_search('서버',0)


def test_db_schema_and_sql():
    assert 'vector(384)' in db.TABLE_SQL
    assert 'day23_search_docs' in db.TABLE_SQL
    assert '<=>' in db.SQL_TOPK and ' ASC ' in db.SQL_TOPK
    assert 'category=%s' in db.SQL_CATEGORY
    assert 'vector_cosine_ops' in db.HNSW_SQL
    assert 'DROP TABLE' not in db.TABLE_SQL
    assert 'UPDATE knowledge ' not in db.UPSERT_SQL


class FakeConn:
    def __init__(self,rows):self.calls=[];self.rows=rows
    def execute(self,sql,params=None):
        self.calls.append((sql,params));return self
    def fetchall(self):return self.rows


def test_topk_sql_bindings_and_rows():
    conn=FakeConn([(102,'서버 실행','프로젝트 폴더에서 서버를 실행합니다.',
                    'development','knowledge_v1',E5_MODEL_ID,0.001)])
    q=np.zeros(384,dtype=np.float32);q[0]=1
    r=db.exact_topk(conn,q,3,category='development')
    sql,params=conn.calls[-1]
    assert len(params)==5
    assert params[1]==E5_MODEL_ID and params[2]=='development' and params[4]==3
    assert 'category=%s' in sql and r[0]['id']==102
    assert r[0]['source_mode']=='pgvector_exact'


def test_protect_live_database_from_synthetic_vectors():
    conn=FakeConn([])
    with pytest.raises(ValueError,match='모의'):db.upsert_rows(conn,load_knowledge(),np.ones((9,384)),model_id='SIMULATED_2D')
    assert conn.calls==[]


@pytest.mark.parametrize('n',list(range(1,9)))
@pytest.mark.parametrize('level',('01_basic','02_intermediate','03_advanced'))
def test_mentor_exercise_fixture(n,level):
    name=[p for p in (MENTOR/level).iterdir() if p.is_dir() and p.name.startswith(f'{n:02}_')][0]
    entry=name/'main.py'
    cp=subprocess.run([sys.executable,str(entry),'--mode','fixture'],capture_output=True,text=True,timeout=30)
    assert cp.returncode==0,(entry,cp.stderr[-3000:])
    data=json.loads((name/'outputs'/f'exercise_{n:02}.json').read_text(encoding='utf-8'))
    assert data['exercise']==n and data['level']=={'01_basic':1,'02_intermediate':2,'03_advanced':3}[level]
    assert data['source_mode'] not in ('e5_live','pgvector_live','pgvector_exact')
    if n==3:
        assert data['document_shape'][1]==384 and data['query_shape']==[1,384]
    if n==5:assert data['prepared_count']==9 and data['hits']
    if n==8:assert data['retrieved_count']>=1 and data['retrieved'][0]['content']


def test_no_mentee_mentor_todo_crossing():
    student=ROOT/'mentee'
    if not student.exists():pytest.skip('강사용 단독 배포본에는 mentee 폴더가 없습니다')
    for code,todos in [('01_basic',3),('02_intermediate',5),('03_advanced',6)]:
        a=list((student/code).rglob('*.py'))
        starts=sum(x.read_text(encoding='utf-8').count('# BEGIN D23-') for x in a)
        assert starts==8*todos
        assert sum(x.read_text(encoding='utf-8').count('NotImplementedError(') for x in a)==starts
        assert sum(x.read_text(encoding='utf-8').count('# BEGIN D23-') for x in (MENTOR/code).rglob('*.py'))==starts
        assert not any('강사용 정답' in x.read_text(encoding='utf-8') for x in a)
