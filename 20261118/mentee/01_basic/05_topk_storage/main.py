"""Day23 실습 05 · 원문·벡터 저장과 Top-k (기본필수, mentee).

실행: python main.py --mode fixture
실제 E5/DB: python main.py --mode live  (필요한 선행 설치 후)
수강생 TODO: 3개 / 상세 요구사항은 각 함수의 주석 및 README.md.
fixture는 모의 시연이지 모델·PostgreSQL 실측 결과가 아닙니다.
"""
import argparse
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2] / 'common'))
from day23kit.data import load_knowledge, passage_text, E5_MODEL_ID, TABLE_NAME
from day23kit.fixtures import fixture_search
from day23kit.embedding import get_encoder, encode_passages, encode_question, validate_vectors
from day23kit.db import connect_db, ensure_table, upsert_rows, exact_topk, TABLE_SQL, SQL_TOPK
from day23kit.io import save_result


# BEGIN D23-05-B01
def schema_sql():
    """
    TODO D23-05-B01 · schema_sql
        기존 knowledge 테이블을 건드리지 않는 day23_search_docs의 CREATE TABLE SQL을 작성하세요.
        필드: id(PK),title,content,category,source_version,embedding_model,embedding vector(384).
        DROP/TRUNCATE를 사용하지 않습니다.
    """
    # TODO D23-05-B01: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-05-B01: 직접 구현하세요")
    return "CREATE TABLE IF NOT EXISTS day23_search_docs ( ... );"
# END D23-05-B01

# BEGIN D23-05-B02
def prepare_document_rows(rows):
    """
    TODO D23-05-B02 · prepare_document_rows
        지식 101~109의 ID/제목/본문/분류/버전 및 passage 입력을 순서대로 묶으세요.
        반환: [{'id', 'passage_input', ...}, ...]. 같은 ID를 새로 만들지 않습니다.
    """
    # TODO D23-05-B02: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-05-B02: 직접 구현하세요")
    return [{'id': r[''], 'passage_input': passage_text()} for r in rows]
# END D23-05-B02

# BEGIN D23-05-B03
def topk_sql():
    """
    TODO D23-05-B03 · topk_sql
        Cosine distance(<=>) 오름차순, k개 제한 SQL을 작성하세요.
        SELECT에 id,title,content,category,source_version,embedding_model,distance 포함.
        E5 외 다른 공간 혼합을 막도록 embedding_model을 필터합니다.
    """
    # TODO D23-05-B03: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-05-B03: 직접 구현하세요")
    return "SELECT id, title, content, ... FROM day23_search_docs WHERE ... ORDER BY embedding <=> %s ASC LIMIT %s"
# END D23-05-B03


def run(mode,level,args):
    rows=load_knowledge()
    sql_schema=schema_sql()
    inputs=prepare_document_rows(rows)
    sql_query=topk_sql()
    question='서버는 어디에서 실행하나요?'
    result=dict(exercise=5,level=level,source_mode='simulated' if mode=='fixture' else 'pgvector_exact',
                table=TABLE_NAME,model=E5_MODEL_ID,prepared_count=len(inputs),
                first_passage=inputs[0]['passage_input'],
                sql_schema=sql_schema,sql_topk=sql_query)
    category=None if level==1 else 'development'
    if level>=2:
        result['sql_filtered']=filtered_sql()
        result['options']=check_search_options(3,category)
    if mode=='fixture':
        hits=fixture_search(question,3,category=category)
    else:
        encoder=get_encoder('live')
        vectors=encode_passages(encoder,rows)
        if level>=3:check_id_vector_integrity(rows,vectors)
        else:validate_vectors(vectors,len(rows))
        qvec=encode_question(encoder,question)
        with connect_db(Path(__file__).with_name('.env')) as conn:
            ensure_table(conn)
            upsert_rows(conn,rows,vectors,E5_MODEL_ID)
            hits=exact_topk(conn,qvec,k=3,category=category)
    result['hits']=[{'id':h['id'],'content':h['content'],'distance':round(h['distance'],6)} for h in hits]
    if level>=3:
        # 이전 단계의 벡터를 재사용합니다. live에서는 같은 모델을 다시 다운로드/로드하지 않습니다.
        if mode=='fixture':
            encoder=get_encoder('fixture')
            vectors=encode_passages(encoder,rows)
        result['id_vector_integrity']=check_id_vector_integrity(rows,vectors)
    return result


def main():
    parser=argparse.ArgumentParser(description='Day23 실습 05 · 원문·벡터 저장과 Top-k')
    parser.add_argument('--mode',choices=['fixture','live'],default='fixture',
        help='fixture=모의 벡터/오프라인, live=실제 E5/DB가 필요한 단계')
    args=parser.parse_args()
    result=run(args.mode,1,args)
    path=save_result(Path(__file__).resolve().parent,'exercise_05.json',result)
    import json
    print(json.dumps(result,ensure_ascii=False,indent=2,default=str))
    print('결과 저장:',path)

if __name__=='__main__':
    main()
