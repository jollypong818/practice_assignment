# 문제 해결 · Windows 11 / VS Code / Git Bash

| 현상 | 확인·조치 |
|---|---|
| `ModuleNotFoundError` | `python -c "import sys;print(sys.executable)"`으로 실행 인터프리터 확인. `python -m pip show ...` 사용 |
| `NotImplementedError D24-...` | 수강생용 TODO의 예상 시작 상태. 해당 블록 구현 후 제거하고 테스트 재실행 |
| 파일 없음 | ZIP 압축을 풀었는지, `data/raw`의 원본을 수정하지 않았는지 확인. 코드는 `__file__` 기준 |
| 한글 디코딩 실패 | 파일 인코딩을 확인. `errors="ignore"`로 강제 삭제하지 않음 |
| TXT인데 페이지가 없음 | 정상. `page_number=None`은 실제 페이지 개념이 없음을 표시 |
| PDF 텍스트가 빈 문자열 | 원본 페이지 형태, 파서 오류, 이미지 PDF 여부를 구분. pypdf는 OCR이 아님 |
| HTML 메뉴가 본문에 섞임 | 지정한 `main` 영역을 읽었는지, script/style 제외 여부 확인 |
| Chunk가 무한 반복됨 | `overlap < size`, `end == len(text)` 시 종료 검사 |
| Coverage > 100% | 중복된 구간 길이를 여러 번 더했는지 확인. 합집합으로 계산 |
| E5 모델 다운로드 실패 | 네트워크 정책·모델 캐시·패키지 버전 확인. 모의 임베딩을 실측으로 기록하지 않음 |
| `pgvector` 모듈 없음 | Python 가상환경의 `pip show pgvector` 확인 (서버 확장과 별개) |
| `extension vector is not available` | PostgreSQL 서버에 확장 파일 설치 여부. Python pip로 해결되지 않음 |
| `relation ingest_chunks does not exist` | `--live-db` 실행 전에 `tools/setup_db.py --apply`와 선택한 실습 Schema 확인 |
| DB 접속 거절 | PostgreSQL 서비스·포트·DB·계정·.env 확인. 비밀번호를 출력/공유하지 않음 |
| Transaction aborted | 같은 연결에서 이미 실패한 SQL을 확인하고 Rollback 필요 여부 점검 |
| 검색 결과가 비어 있음 | category, current_version/current_pipeline_version, 모델 입력 계약, 준비된 Chunk 수 확인 |

같은 장애라도 최초 실패 지점부터 확인합니다. `outputs/` 로그에 API 키·비밀번호·실제 개인정보를 기록하지 않습니다.
