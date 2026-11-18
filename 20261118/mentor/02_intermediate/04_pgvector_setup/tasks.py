# Day23 / 실습 04 / 응용 / mentor
from day23kit.mathops import cosine_distance

# BEGIN D23-04-I01
def sql_server_info():
    """
    [강사용 정답] D23-04-I01 · sql_server_info
        pgAdmin에서 실행할 서버 버전·현재 DB 조회 SQL을 작성하세요.
        반드시 SELECT version()과 current_database()를 포함하세요.
        DB 변경이나 DROP/CREATE DATABASE는 하지 않습니다.
    """
    # 해설 D23-04-I01: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    # 조회만 하므로 기존 DB 내용을 변경하지 않습니다.
    return 'SELECT version(); SELECT current_database(), current_user;'
# END D23-04-I01

# BEGIN D23-04-I02
def sql_extension_state():
    """
    [강사용 정답] D23-04-I02 · sql_extension_state
        vector 확장의 제공 여부와 설치 여부를 확인하는 SQL 문자열을 작성하세요.
        pg_available_extensions, installed_version, WHERE name='vector' 사용.
    """
    # 해설 D23-04-I02: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    return "SELECT name, default_version, installed_version FROM pg_available_extensions WHERE name='vector';"
# END D23-04-I02

# BEGIN D23-04-I03
def sql_distance_probe():
    """
    [강사용 정답] D23-04-I03 · sql_distance_probe
        SQL에서 3차원 벡터 [1,0,0]과 [0,1,0]의 Cosine distance를 계산하세요.
        문자열 반환. CAST는 ::vector, 연산자는 <=>를 사용합니다.
        예상값 1.0이며 384차원 E5 출력이 아닙니다.
    """
    # 해설 D23-04-I03: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    return "SELECT '[1,0,0]'::vector <=> '[0,1,0]'::vector AS cosine_distance;"
# END D23-04-I03

# BEGIN D23-04-I04
def check_extension_row(row):
    """
    [강사용 정답] D23-04-I04 · check_extension_row
        fetchone()으로 읽은 (name, default_version, installed_version) 행을 판정하세요.
        None이면 unavailable, installed_version이 None이면 available_not_installed,
        설치됐으면 installed 및 version을 반환합니다.
    """
    # 해설 D23-04-I04: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    if row is None:return {'state':'unavailable','version':None}
    return {'state':'installed' if row[2] else 'available_not_installed','version':row[2]}
# END D23-04-I04

# BEGIN D23-04-I05
def classify_install_error(message):
    """
    [강사용 정답] D23-04-I05 · classify_install_error
        대표 오류를 실패 위치(compile, server_files, db_permission,
        db_extension, python_env, other)로 분류하세요.
        키나 비밀번호가 들어 있는 예외 원문은 저장하지 않습니다.
    """
    # 해설 D23-04-I05: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    # 로그 원문 대신 주어진 짧은 오류 종류만 분류합니다.
    msg=message.lower()
    if 'nmake' in msg or 'postgres.h' in msg:return 'compile'
    if 'vector.control' in msg:return 'server_files'
    if 'permission denied' in msg or 'must be superuser' in msg:return 'db_permission'
    if 'type "vector" does not exist' in msg:return 'db_extension'
    if 'no module named' in msg:return 'python_env'
    return 'other'
# END D23-04-I05
