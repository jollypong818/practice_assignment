"""Day23 실습 04 · 서버 확장과 Python 연결 (기본필수, mentor).

실행: python main.py --mode fixture
실제 E5/DB: python main.py --mode live  (필요한 선행 설치 후)
수강생 TODO: 3개 / 상세 요구사항은 각 함수의 주석 및 README.md.
fixture는 모의 시연이지 모델·PostgreSQL 실측 결과가 아닙니다.
"""
import argparse
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2] / 'common'))
from day23kit.mathops import cosine_distance
from day23kit.db import connect_db
from day23kit.io import save_result


# BEGIN D23-04-B01
def sql_server_info():
    """
    [강사용 정답] D23-04-B01 · sql_server_info
        pgAdmin에서 실행할 서버 버전·현재 DB 조회 SQL을 작성하세요.
        반드시 SELECT version()과 current_database()를 포함하세요.
        DB 변경이나 DROP/CREATE DATABASE는 하지 않습니다.
    """
    # 해설 D23-04-B01: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    # 조회만 하므로 기존 DB 내용을 변경하지 않습니다.
    return 'SELECT version(); SELECT current_database(), current_user;'
# END D23-04-B01

# BEGIN D23-04-B02
def sql_extension_state():
    """
    [강사용 정답] D23-04-B02 · sql_extension_state
        vector 확장의 제공 여부와 설치 여부를 확인하는 SQL 문자열을 작성하세요.
        pg_available_extensions, installed_version, WHERE name='vector' 사용.
    """
    # 해설 D23-04-B02: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    return "SELECT name, default_version, installed_version FROM pg_available_extensions WHERE name='vector';"
# END D23-04-B02

# BEGIN D23-04-B03
def sql_distance_probe():
    """
    [강사용 정답] D23-04-B03 · sql_distance_probe
        SQL에서 3차원 벡터 [1,0,0]과 [0,1,0]의 Cosine distance를 계산하세요.
        문자열 반환. CAST는 ::vector, 연산자는 <=>를 사용합니다.
        예상값 1.0이며 384차원 E5 출력이 아닙니다.
    """
    # 해설 D23-04-B03: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    return "SELECT '[1,0,0]'::vector <=> '[0,1,0]'::vector AS cosine_distance;"
# END D23-04-B03


def run(mode,level,args):
    sqls={'server':sql_server_info(),'extension':sql_extension_state(),'distance':sql_distance_probe()}
    result=dict(exercise=4,level=level,source_mode='not_run' if mode=='fixture' else 'pgvector_live',
                sql_for_pgadmin=sqls,db_check='not_run')
    if level>=2:
        result['illustrated_extension_state']=check_extension_row(('vector','0.8.7',None))
        result['example_error_stage']=classify_install_error('postgres.h not found')
    if level>=3:
        result['manual_pending']=audit_install_steps({})
    if mode=='live':
        # live만 실제 DB 연결. Windows 빌드 및 CREATE EXTENSION은 사전 수동 절차.
        with connect_db(Path(__file__).with_name('.env')) as conn:
            ver=conn.execute('SELECT version()').fetchone()[0]
            dbname=conn.execute('SELECT current_database()').fetchone()[0]
            ext=conn.execute("SELECT name, default_version, installed_version FROM pg_available_extensions WHERE name='vector'").fetchone()
            result['db_check']={'server_version':ver,'database':dbname,'extension':check_extension_row(ext)} if level>=2 else {'server_version':ver,'database':dbname,'extension_provided':ext is not None}
            if ext is not None and ext[2]:
                result['db_check']['distance_probe']=float(conn.execute(sql_distance_probe()).fetchone()[0])
            else:
                result['db_check']['distance_probe']='not_run_extension_not_activated'
    return result


def main():
    parser=argparse.ArgumentParser(description='Day23 실습 04 · 서버 확장과 Python 연결')
    parser.add_argument('--mode',choices=['fixture','live'],default='fixture',
        help='fixture=모의 벡터/오프라인, live=실제 E5/DB가 필요한 단계')
    args=parser.parse_args()
    result=run(args.mode,1,args)
    path=save_result(Path(__file__).resolve().parent,'exercise_04.json',result)
    import json
    print(json.dumps(result,ensure_ascii=False,indent=2,default=str))
    print('결과 저장:',path)

if __name__=='__main__':
    main()
