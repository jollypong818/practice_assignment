# Postman 사용 안내 (11월 20일 보고서 처리 Agent)

## 1. 준비와 실행 순서

1. Postman의 Import에서 `Report_Agent.postman_collection.json`과 `Report_Agent.postman_environment.json`을 가져옵니다. 이 자료는 pre-request의 `pm.execution.skipRequest()`를 지원하는 Postman에서 사용합니다.
2. Environment에서 **Report Agent | Windows Local**을 선택합니다. `base_url`은 `http://127.0.0.1:8000`, `allow_paid_llm`은 기본 `false`입니다.
3. 선택한 프로젝트 루트에서 DB 시드·실제 E5 인덱싱을 완료하고 `python -m app.main`으로 서버를 실행합니다. `.env`의 `PROJECT_LEVEL`은 선택한 Basic/Intermediate/Advanced와 맞춰 둡니다.
4. **01 Basic 무료 경로**를 순서대로 실행합니다. 생성 → 조회 → 수정 → 수정 후 재조회가 이어집니다. 생성·수정 입력값과 재조회 값이 같아야 통과합니다.
5. **04 오류 사례**를 실행합니다. Intermediate는 **02**, Advanced는 **02와 03**을 추가합니다. 상위 단계 폴더를 Basic 서버에 실행하면 미구현 기능의 오류가 발생하므로 선택하지 않습니다.
6. 다른 카테고리도 확인하려면 **05 선택 실습**을 실행합니다. 모든 기능을 처음부터 따로 구현하라는 뜻이 아니라 동일한 등록 계약을 다른 입력으로 확인하는 단계입니다.
7. 실제 LLM을 확인할 때만 아래의 유료 요청 절차를 수행합니다. **07 Basic 정리** 전에 실행해야 생성한 보고서를 요약할 수 있습니다.
8. 마지막으로 **07 Basic 정리**를 실행해 204 후 재조회 404를 확인합니다. **05**를 실행했다면 **08 선택 실습 정리**도 실행합니다.
9. `sql/verify.sql`로 실제 DB 행·벡터·상세·Prompt 일관성을 확인합니다. Postman 초록색 테스트만으로 최종 완료를 판정하지 않습니다.

## 2. 생성 ID와 입력값의 연결

API 응답의 JSON 필드는 `report_id`이고, 이 값을 다음 요청에 전달하는 **Postman Environment 변수는 `created_report_id`**입니다. 예를 들어 `GET {{base_url}}/api/v1/reports/{{created_report_id}}`를 사용합니다. 별도 `report_id` 환경변수를 만들 필요가 없습니다.

`created_contract`와 `updated_contract`에는 이 Collection에서 보낸 입력값을 보관합니다. 재조회에서 `category_code`, `title`, `author`, `content`, `overview`, `details`를 비교하며, 생성·수정 시각이 유효한 UTC 시각인지도 확인합니다. 이 변수에 실제 개인정보를 넣지 않습니다.

생성이 실패하면 이전 ID를 재사용하지 않습니다. 생성 ID가 없거나 초기 시드 범위(1~180)이면 그 ID를 사용하는 정리 요청을 건너뜁니다. 삭제 성공을 확인한 뒤 해당 임시 변수를 비웁니다. `latest_prompt_version`은 Prompt 버전 생성에 성공하면 자동 저장됩니다.

## 3. 유료 LLM 요청은 명시적으로 선택

**06 실제 LLM 유료 요청**에는 Basic 2개, Intermediate 2개, Advanced 1개 요청을 모았습니다. 각 요청의 pre-request 스크립트는 `allow_paid_llm`이 문자열 `true`일 때만 요청을 보냅니다. 기본 `false`에서는 전체 Runner에 이 폴더가 포함되어도 유료 요청을 건너뜁니다. 건너뛴 요청은 실행 성공이나 LLM 검증 완료가 아닙니다.

API 키·모델·비용과 본인 구현 레벨을 확인한 뒤, 필요한 요청 하나를 골라 `allow_paid_llm`을 `true`로 바꾸고 수동 실행합니다. 실행 후에는 바로 `false`로 되돌립니다. Basic은 기본 요약·Agent 요약, Intermediate는 검색 후 요약·Structured 요약, Advanced는 Tool Calling까지 선택할 수 있습니다. 사용하지 않는 상위 단계 요청은 실행하지 않습니다.

유료 폴더를 포함한 전체 Runner를 `true` 상태로 실행하면 5개 요청을 모두 보낼 수 있으므로 수동 확인에는 개별 요청을 사용합니다. 모델 미설정 503, 타임아웃 504, 건너뜀은 실제 LLM 성공 증거가 아닙니다.

## 4. T-05/T-06: 검색 형식 검사와 의미 판정

자동 **가중치 Hybrid 검색**은 `found`, 관련 범주, 관련 보고서 ID 집합과 Keyword 일치를 검사합니다. 기준 집합은 `common/data/seed_catalog.json` 및 `common/data/search_cases.json`에서 가져왔으며, 이번 실행에서 생성·수정한 관련 보고서 ID도 허용합니다. 보고서 ID 1 한 건이나 정확한 cosine 값을 정답으로 고정하지 않습니다. 제공 시드를 직접 바꾸거나 별도 데이터를 추가했다면 평가 기준도 해당 데이터에 맞춰 확인합니다.

**관련성이 낮은 질의** 요청의 자동 검사는 의도적으로 응답 형식만 확인합니다. 실제 `not_found` 여부는 모델 점수와 임계값에 따라 달라지므로 이 요청이 초록색이라는 이유만으로 검색 품질을 통과한 것은 아닙니다.

Basic도 다음을 직접 확인하고 결과를 제출합니다.

1. `common/data/search_cases.json`의 관련 질의와 무관 질의를 같은 검색 API에 보냅니다.
2. 관련 질의는 반환 보고서의 ID·범주·원문을 `seed_catalog.json`과 비교하고, 왜 관련 있는지 한 줄로 기록합니다.
3. 무관 질의는 `status`, 반환 ID(있을 때), `cosine_similarity`(응답에 있을 때), `.env`의 `SEARCH_MIN_SIMILARITY`를 기록합니다. 미검색 응답에 점수가 없으면 값을 지어내지 않습니다.
4. 판정 기준에 미달하면 HTTP 200, `status=not_found`, `best_match=null`이어야 합니다. 무관한 문서가 반환되면 오탐으로 기록하고 관련 질의를 놓치지 않는지 함께 보며 임계값을 검토합니다. 초기 후보 0.75나 특정 cosine 값은 고정 정답이 아닙니다.
5. **T-05 관련 1건 / T-06 기준 미달 시 미검색** 확인 결과를 Postman 응답 또는 호출 로그와 함께 제출합니다. Advanced는 `scripts/evaluate_search.py`로 평가 파일도 생성할 수 있습니다.

## 5. 데이터 정리와 검증 시점

기본 시드에는 보고서 180개, Prompt 버전 60개가 있습니다. 실제 인덱싱 전 벡터 0개, 인덱싱 후 벡터 180개가 정상입니다. CREATE/DELETE·Prompt 버전 생성 뒤에는 전체 개수가 달라질 수 있으므로 `verify.sql`의 초기 상태 기대값과 현재 상태를 구분합니다.

선택 정리는 이번에 생성해 저장한 `optional_*_id`만 사용합니다. 초기 시드 보고서를 삭제하여 숫자를 억지로 맞추지 않습니다. Intermediate Prompt 버전 생성과 Advanced 활성 버전 전환은 시드 Prompt(기본 121)의 이력·본문 상태를 변경합니다. 별도 실습 DB에서 수행하고 해당 변경을 남긴 경우 Prompt 버전 수가 60을 넘는 것은 정상입니다.
