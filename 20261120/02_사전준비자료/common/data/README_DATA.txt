Day25 Report Agent v1.4 · 데이터 파일 사용 안내

1. seed_catalog.json — 시드 원문과 출처 확인

180개 보고서의 ID, 문서 유형, 제목, 작성자, 개요, 본문을 확인하는 참고 목록입니다.
실제 DB 초기 데이터는 common/sql/seed.sql로 넣습니다.

이 파일의 details는 배열입니다. API의 details 객체와 형식이 다르므로 항목을
그대로 POST 요청 Body에 붙여 넣지 마세요. 등록 요청 JSON은 요구사항명세서의
API-02 카드 또는 Postman의 보고서 생성 요청을 참고합니다.

2. search_cases.json — Basic·응용의 수동 검색 확인 5개

각 query를 POST /api/v1/search/similar에 보내고 응답을 확인합니다.
반환된 보고서의 ID·문서 유형·원문을 seed_catalog.json과 비교하고,
질의와 어떤 내용이 관련되는지 한 줄로 기록합니다.

expected_category_codes는 관련 문서 유형의 안내이며, 범주만 맞으면 정답이라는
뜻은 아닙니다. 회의 결정이나 프롬프트 버전을 다루는 연구계획도 관련 문서입니다.
expected_keyword는 제목·개요·본문의 Keyword 일치 기대를 나타냅니다.
정확한 cosine 값이나 한 개의 report_id를 고정 정답으로 삼지 않습니다.
무관 질의는 not_found가 되는지 확인하고, 오탐이면 점수·임계값·원문을 기록합니다.

3. evaluation_cases.json — Advanced 자동 평가용 6개

각 query와 사람이 정한 관련 보고서 ID 집합(relevant_ids)을 담습니다.
실제 검색 결과를 그대로 정답으로 만든 파일이 아닙니다.
search_cases.json의 수동 확인 5개와는 별도의 평가 세트입니다.

이 파일을 실행할 Advanced 프로젝트의 tests/evaluation_cases.json으로 복사합니다.
평가 코드가 준비되면 그 프로젝트 폴더에서 다음 명령을 실행합니다.

    python scripts/evaluate_search.py

평가 스크립트는 프로젝트의 tests/evaluation_cases.json을 읽습니다.
이 common/data 폴더의 파일을 직접 읽는 구조는 아닙니다.
실제 PostgreSQL 접속과 E5 인덱싱을 마친 뒤 실행하면 outputs 폴더에
search_evaluation.json과 search_evaluation.csv를 생성합니다.
결과에서 Recall@5, 선택한 ID, 오탐·누락, 점수와 선정 근거를 확인합니다.

4. 초기 시드 기준과 실제 실행 결과

이 파일들은 제공 시드를 기준으로 합니다. 시드 원문을 수정·삭제했다면 현재 DB의
원문과 관련성을 다시 확인하세요. 데이터가 달라졌는데 초기 기대값만으로 채점하면
잘못 판단할 수 있습니다. seed.sql 재실행은 수정한 내용을 초기 값으로 되돌리지 않습니다.

이 묶음에는 실제 강의 PC의 PostgreSQL·E5 실행 결과가 들어 있지 않습니다.
검색 점수와 평가 결과는 수강생 환경에서 실행하여 확인합니다.
