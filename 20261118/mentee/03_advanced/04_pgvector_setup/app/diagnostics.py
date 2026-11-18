# Day23 / 실습 04 / 심화 diagnostics / mentee



# BEGIN D23-04-A04
def check_extension_row(row):
    """
    TODO D23-04-A04 · check_extension_row
        fetchone()으로 읽은 (name, default_version, installed_version) 행을 판정하세요.
        None이면 unavailable, installed_version이 None이면 available_not_installed,
        설치됐으면 installed 및 version을 반환합니다.
    """
    # TODO D23-04-A04: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-04-A04: 직접 구현하세요")
# END D23-04-A04

# BEGIN D23-04-A05
def classify_install_error(message):
    """
    TODO D23-04-A05 · classify_install_error
        대표 오류를 실패 위치(compile, server_files, db_permission,
        db_extension, python_env, other)로 분류하세요.
        키나 비밀번호가 들어 있는 예외 원문은 저장하지 않습니다.
    """
    # TODO D23-04-A05: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-04-A05: 직접 구현하세요")
# END D23-04-A05

# BEGIN D23-04-A06
def audit_install_steps(steps):
    """
    TODO D23-04-A06 · audit_install_steps
        빌드 도구·PGROOT·서버 파일·DB 활성화·Python 등록 5단계를 판정하세요.
        입력: {단계명: bool}. 누락된 단계를 리스트로 반환합니다.
        HTML의 순서를 유지하고 미확인을 성공 처리하지 마세요.
    """
    # TODO D23-04-A06: 위 입력·출력 계약에 맞게 직접 구현합니다.
    raise NotImplementedError("D23-04-A06: 직접 구현하세요")
# END D23-04-A06
