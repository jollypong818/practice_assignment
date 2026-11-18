# Day23 / 실습 04 / 심화 sql_checks / mentee
from day23kit.mathops import cosine_distance


# BEGIN D23-04-A01
def sql_server_info():
    """
    TODO D23-04-A01 · sql_server_info
        pgAdmin에서 실행할 서버 버전·현재 DB 조회 SQL을 작성하세요.
        반드시 SELECT version()과 current_database()를 포함하세요.
        DB 변경이나 DROP/CREATE DATABASE는 하지 않습니다.
    """
    # TODO D23-04-A01: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-04-A01: 직접 구현하세요")
# END D23-04-A01

# BEGIN D23-04-A02
def sql_extension_state():
    """
    TODO D23-04-A02 · sql_extension_state
        vector 확장의 제공 여부와 설치 여부를 확인하는 SQL 문자열을 작성하세요.
        pg_available_extensions, installed_version, WHERE name='vector' 사용.
    """
    # TODO D23-04-A02: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-04-A02: 직접 구현하세요")
# END D23-04-A02

# BEGIN D23-04-A03
def sql_distance_probe():
    """
    TODO D23-04-A03 · sql_distance_probe
        SQL에서 3차원 벡터 [1,0,0]과 [0,1,0]의 Cosine distance를 계산하세요.
        문자열 반환. CAST는 ::vector, 연산자는 <=>를 사용합니다.
        예상값 1.0이며 384차원 E5 출력이 아닙니다.
    """
    # TODO D23-04-A03: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-04-A03: 직접 구현하세요")
# END D23-04-A03
