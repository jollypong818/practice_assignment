# Day23 / 실습 04 / 심화 diagnostics / mentor



# BEGIN D23-04-A04
def check_extension_row(row):
    """
    [강사용 정답] D23-04-A04 · check_extension_row
        fetchone()으로 읽은 (name, default_version, installed_version) 행을 판정하세요.
        None이면 unavailable, installed_version이 None이면 available_not_installed,
        설치됐으면 installed 및 version을 반환합니다.
    """
    # 해설 D23-04-A04: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    if row is None:return {'state':'unavailable','version':None}
    return {'state':'installed' if row[2] else 'available_not_installed','version':row[2]}
# END D23-04-A04

# BEGIN D23-04-A05
def classify_install_error(message):
    """
    [강사용 정답] D23-04-A05 · classify_install_error
        대표 오류를 실패 위치(compile, server_files, db_permission,
        db_extension, python_env, other)로 분류하세요.
        키나 비밀번호가 들어 있는 예외 원문은 저장하지 않습니다.
    """
    # 해설 D23-04-A05: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    # 로그 원문 대신 주어진 짧은 오류 종류만 분류합니다.
    msg=message.lower()
    if 'nmake' in msg or 'postgres.h' in msg:return 'compile'
    if 'vector.control' in msg:return 'server_files'
    if 'permission denied' in msg or 'must be superuser' in msg:return 'db_permission'
    if 'type "vector" does not exist' in msg:return 'db_extension'
    if 'no module named' in msg:return 'python_env'
    return 'other'
# END D23-04-A05

# BEGIN D23-04-A06
def audit_install_steps(steps):
    """
    [강사용 정답] D23-04-A06 · audit_install_steps
        빌드 도구·PGROOT·서버 파일·DB 활성화·Python 등록 5단계를 판정하세요.
        입력: {단계명: bool}. 누락된 단계를 리스트로 반환합니다.
        HTML의 순서를 유지하고 미확인을 성공 처리하지 마세요.
    """
    # 해설 D23-04-A06: 입력을 먼저 확인하고, 핵심 개념을 적용한 다음 결과를 반환합니다.
    order=['build_tools','pgroot','server_files','db_extension','python_adapter']
    return [name for name in order if steps.get(name) is not True]
# END D23-04-A06
