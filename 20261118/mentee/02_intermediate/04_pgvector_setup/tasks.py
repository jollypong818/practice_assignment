# Day23 / 실습 04 / 응용 / mentee
from day23kit.mathops import cosine_distance

# BEGIN D23-04-I01
def sql_server_info():
    """
    TODO D23-04-I01 · sql_server_info
        pgAdmin에서 실행할 서버 버전·현재 DB 조회 SQL을 작성하세요.
        반드시 SELECT version()과 current_database()를 포함하세요.
        DB 변경이나 DROP/CREATE DATABASE는 하지 않습니다.
    """
    # TODO D23-04-I01: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-04-I01: 직접 구현하세요")
# END D23-04-I01

# BEGIN D23-04-I02
def sql_extension_state():
    """
    TODO D23-04-I02 · sql_extension_state
        vector 확장의 제공 여부와 설치 여부를 확인하는 SQL 문자열을 작성하세요.
        pg_available_extensions, installed_version, WHERE name='vector' 사용.
    """
    # TODO D23-04-I02: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-04-I02: 직접 구현하세요")
# END D23-04-I02

# BEGIN D23-04-I03
def sql_distance_probe():
    """
    TODO D23-04-I03 · sql_distance_probe
        SQL에서 3차원 벡터 [1,0,0]과 [0,1,0]의 Cosine distance를 계산하세요.
        문자열 반환. CAST는 ::vector, 연산자는 <=>를 사용합니다.
        예상값 1.0이며 384차원 E5 출력이 아닙니다.
    """
    # TODO D23-04-I03: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-04-I03: 직접 구현하세요")
# END D23-04-I03

# BEGIN D23-04-I04
def check_extension_row(row):
    """
    TODO D23-04-I04 · check_extension_row
        fetchone()으로 읽은 (name, default_version, installed_version) 행을 판정하세요.
        None이면 unavailable, installed_version이 None이면 available_not_installed,
        설치됐으면 installed 및 version을 반환합니다.
    """
    # TODO D23-04-I04: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-04-I04: 직접 구현하세요")
# END D23-04-I04

# BEGIN D23-04-I05
def classify_install_error(message):
    """
    TODO D23-04-I05 · classify_install_error
        대표 오류를 실패 위치(compile, server_files, db_permission,
        db_extension, python_env, other)로 분류하세요.
        키나 비밀번호가 들어 있는 예외 원문은 저장하지 않습니다.
    """
    # TODO D23-04-I05: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-04-I05: 직접 구현하세요")
# END D23-04-I05
