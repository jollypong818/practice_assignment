# 구현 블록 대응표

각 블록 ID는 mentee·mentor에서 같습니다. 파일 경로는 역할 폴더 기준입니다.

| ID | 경로 | 요구사항 |
|---|---|---|
| `D21-01-B01` | `01_basic/01_prompt_structure/main.py` | 역할·작업·입력·제약·실패·출력 여섯 칸을 완성하세요. |
| `D21-01-B02` | `01_basic/01_prompt_structure/main.py` | Template에 질문·직렬화한 지식·출력 계약을 대입하세요. |
| `D21-01-B03` | `01_basic/01_prompt_structure/main.py` | 요구사항과 Prompt 원문을 저장하고 기준 질문을 확인하세요. |
| `D21-02-B01` | `01_basic/02_examples_versions/main.py` | 예제 ID 901을 사용해 정상 답과 정보 부족 답을 완성하세요. |
| `D21-02-B02` | `01_basic/02_examples_versions/main.py` | 같은 질문에 Zero-shot과 Few-shot Prompt를 각각 만드세요. |
| `D21-02-B03` | `01_basic/02_examples_versions/main.py` | 변경점·가설·고정 조건과 두 Prompt를 저장하세요. |
| `D21-03-B01` | `01_basic/03_task_decomposition/main.py` | 질문이 요구하는 사실과, 제공 자료가 지원하는 사실을 구분하세요. |
| `D21-03-B02` | `01_basic/03_task_decomposition/main.py` | 하나라도 근거가 부족하면 수업의 정보 부족 상태를 선택하세요. |
| `D21-03-B03` | `01_basic/03_task_decomposition/main.py` | 정상·정보 부족의 판단과 최종 출력 지시를 저장하세요. |
| `D21-04-B01` | `01_basic/04_context_builder/main.py` | 선택 ID의 순서를 보존해 지식을 골라 JSON으로 직렬화하세요. |
| `D21-04-B02` | `01_basic/04_context_builder/main.py` | PPT의 가상 token 예산에서 근거 문맥에 남는 공간을 구하세요. |
| `D21-04-B03` | `01_basic/04_context_builder/main.py` | 포함·제외 ID와 원문·예산을 저장하세요. |
| `D21-05-B01` | `01_basic/05_ab_evaluation/main.py` | A의 규칙을 유지하면서 B에 근거 부족 규칙 한 개만 추가하세요. |
| `D21-05-B02` | `01_basic/05_ab_evaluation/main.py` | 개선용 D01~D03 세 질문만 선택하세요. |
| `D21-05-B03` | `01_basic/05_ab_evaluation/main.py` | 첫 응답만 골라 통과·미실행·미평가 개수를 기록하세요. |
| `D21-06-B01` | `01_basic/06_output_validation/main.py` | PPT 50장의 엄격한 네 필드 계약을 선언하세요. |
| `D21-06-B02` | `01_basic/06_output_validation/main.py` | JSON 문법 실패와 Pydantic Schema 실패를 분리하세요. |
| `D21-06-B03` | `01_basic/06_output_validation/main.py` | 이번 문맥의 출처 범위와 상태별 조합을 확인하세요. |
| `D21-06-B04` | `01_basic/06_output_validation/main.py` | 제공 fixture를 분류하고 모델 정의에서 Schema를 내보내세요. |
| `D21-07-B01` | `01_basic/07_bounded_retry/main.py` | 허용한 형식 오류만 안전한 한 문장 요약으로 수정 요청을 만드세요. |
| `D21-07-B02` | `01_basic/07_bounded_retry/main.py` | 최초 1회+수정 1회까지만 반복하고 통과하지 못하면 None을 반환하세요. |
| `D21-07-B03` | `01_basic/07_bounded_retry/main.py` | 네 fixture 순서의 호출 수 2·2·1·1을 확인하고 기록하세요. |
| `D21-08-B01` | `01_basic/08_daily_project/main.py` | 05에서 고정한 A/B 입력을 재사용하고 실행에 사용할 버전을 확인하세요. |
| `D21-08-B02` | `01_basic/08_daily_project/main.py` | 최종 확인용 H01~H03만 골라 세 질문의 A/B 계획을 만드세요. |
| `D21-08-B03` | `01_basic/08_daily_project/main.py` | 검증과 사람 평가를 합치되 미실행·미평가 상태를 그대로 남기세요. |
| `D21-01-I01` | `02_intermediate/01_prompt_structure/analysis.py` | 역할·작업·입력·제약·실패·출력 여섯 칸을 완성하세요. |
| `D21-01-I02` | `02_intermediate/01_prompt_structure/analysis.py` | 빈 질문과 필수 요구사항 누락을 먼저 거부하세요. |
| `D21-01-I03` | `02_intermediate/01_prompt_structure/analysis.py` | Template에 질문·직렬화한 지식·출력 계약을 대입하세요. |
| `D21-01-I04` | `02_intermediate/01_prompt_structure/analysis.py` | 요구사항과 Prompt 원문을 저장하고 기준 질문을 확인하세요. |
| `D21-01-I05` | `02_intermediate/01_prompt_structure/analysis.py` | 정상·정보 부족 두 질문에 같은 요구사항을 적용하고 충돌 지시를 고치세요. |
| `D21-02-I01` | `02_intermediate/02_examples_versions/analysis.py` | 예제 ID 901을 사용해 정상 답과 정보 부족 답을 완성하세요. |
| `D21-02-I02` | `02_intermediate/02_examples_versions/analysis.py` | 같은 질문에 Zero-shot과 Few-shot Prompt를 각각 만드세요. |
| `D21-02-I03` | `02_intermediate/02_examples_versions/analysis.py` | 변경점·가설·고정 조건과 두 Prompt를 저장하세요. |
| `D21-02-I04` | `02_intermediate/02_examples_versions/analysis.py` | 예제 하나의 질문 표현만 바꾸고 새 버전으로 기록하세요. |
| `D21-03-I01` | `02_intermediate/03_task_decomposition/analysis.py` | 질문이 요구하는 사실과, 제공 자료가 지원하는 사실을 구분하세요. |
| `D21-03-I02` | `02_intermediate/03_task_decomposition/analysis.py` | 하나라도 근거가 부족하면 수업의 정보 부족 상태를 선택하세요. |
| `D21-03-I03` | `02_intermediate/03_task_decomposition/analysis.py` | 정상·정보 부족의 판단과 최종 출력 지시를 저장하세요. |
| `D21-03-I04` | `02_intermediate/03_task_decomposition/analysis.py` | 위치와 기간을 함께 묻는 질문에서 빠진 사실을 확인하세요. |
| `D21-04-I01` | `02_intermediate/04_context_builder/analysis.py` | 선택 ID의 순서를 보존해 지식을 골라 JSON으로 직렬화하세요. |
| `D21-04-I02` | `02_intermediate/04_context_builder/analysis.py` | PPT의 가상 token 예산에서 근거 문맥에 남는 공간을 구하세요. |
| `D21-04-I03` | `02_intermediate/04_context_builder/analysis.py` | 포함·제외 ID와 원문·예산을 저장하세요. |
| `D21-04-I04` | `02_intermediate/04_context_builder/analysis.py` | 중복 선택은 제거하고, 스냅샷 중복 ID와 없는 ID는 오류인지 확인하세요. |
| `D21-04-I05` | `02_intermediate/04_context_builder/analysis.py` | 허용·유효성·관련성 검토를 선택 이유와 함께 적으세요. |
| `D21-05-I01` | `02_intermediate/05_ab_evaluation/analysis.py` | A의 규칙을 유지하면서 B에 근거 부족 규칙 한 개만 추가하세요. |
| `D21-05-I02` | `02_intermediate/05_ab_evaluation/analysis.py` | 개선용 D01~D03 세 질문만 선택하세요. |
| `D21-05-I03` | `02_intermediate/05_ab_evaluation/analysis.py` | 첫 응답만 골라 통과·미실행·미평가 개수를 기록하세요. |
| `D21-05-I04` | `02_intermediate/05_ab_evaluation/analysis.py` | source_mode별 결과를 분리하고 fixture 지표를 실모델 품질로 해석하지 마세요. |
| `D21-05-I05` | `02_intermediate/05_ab_evaluation/analysis.py` | 같은 조건을 한 번 더 관찰하도록 반복 수를 설정하세요. |
| `D21-06-I01` | `02_intermediate/06_output_validation/analysis.py` | PPT 50장의 엄격한 네 필드 계약을 선언하세요. |
| `D21-06-I02` | `02_intermediate/06_output_validation/analysis.py` | JSON 문법 실패와 Pydantic Schema 실패를 분리하세요. |
| `D21-06-I03` | `02_intermediate/06_output_validation/analysis.py` | 중복 출처와 이번에 제공하지 않은 출처를 서로 구분하세요. |
| `D21-06-I04` | `02_intermediate/06_output_validation/analysis.py` | 상태별 필드 조합과 공백·부족 고정문을 검사하세요. |
| `D21-06-I05` | `02_intermediate/06_output_validation/analysis.py` | 제공 fixture를 분류하고 모델 정의에서 Schema를 내보내세요. |
| `D21-06-I06` | `02_intermediate/06_output_validation/analysis.py` | ID 101을 붙인 서버 답변이 자동 검사만 통과하는 반례를 확인하세요. |
| `D21-07-I01` | `02_intermediate/07_bounded_retry/analysis.py` | 허용한 형식 오류만 안전한 한 문장 요약으로 수정 요청을 만드세요. |
| `D21-07-I02` | `02_intermediate/07_bounded_retry/analysis.py` | 최초 1회+수정 1회까지만 반복하고 통과하지 못하면 None을 반환하세요. |
| `D21-07-I03` | `02_intermediate/07_bounded_retry/analysis.py` | 네 fixture 순서의 호출 수 2·2·1·1을 확인하고 기록하세요. |
| `D21-07-I04` | `02_intermediate/07_bounded_retry/analysis.py` | 첫 응답과 재시도 후 결과를 다른 필드로 집계하세요. |
| `D21-07-I05` | `02_intermediate/07_bounded_retry/analysis.py` | 마지막 실패 뒤에는 수정 요청이 더 만들어지지 않는지 확인하세요. |
| `D21-08-I01` | `02_intermediate/08_daily_project/analysis.py` | 05에서 고정한 A/B 입력을 재사용하고 실행에 사용할 버전을 확인하세요. |
| `D21-08-I02` | `02_intermediate/08_daily_project/analysis.py` | 최종 확인용 H01~H03만 골라 세 질문의 A/B 계획을 만드세요. |
| `D21-08-I03` | `02_intermediate/08_daily_project/analysis.py` | 검증과 사람 평가를 합치되 미실행·미평가 상태를 그대로 남기세요. |
| `D21-08-I04` | `02_intermediate/08_daily_project/analysis.py` | 첫 응답과 재시도 후 결과의 수를 분리하고 한 가지 개선안을 기록하세요. |
| `D21-08-I05` | `02_intermediate/08_daily_project/analysis.py` | 가능하면 같은 조건의 최종 질문을 한 번 더 관찰하세요. |
| `D21-01-A01` | `03_advanced/01_prompt_structure/prompt_builder.py` | 역할·작업·입력·제약·실패·출력 여섯 칸을 완성하세요. |
| `D21-01-A02` | `03_advanced/01_prompt_structure/prompt_builder.py` | 빈 질문과 필수 요구사항 누락을 먼저 거부하세요. |
| `D21-01-A03` | `03_advanced/01_prompt_structure/prompt_builder.py` | Template에 질문·직렬화한 지식·출력 계약을 대입하세요. |
| `D21-01-A04` | `03_advanced/01_prompt_structure/prompt_builder.py` | 요구사항과 Prompt 원문을 저장하고 기준 질문을 확인하세요. |
| `D21-01-A05` | `03_advanced/01_prompt_structure/prompt_builder.py` | 정상·정보 부족 두 질문에 같은 요구사항을 적용하고 충돌 지시를 고치세요. |
| `D21-01-A06` | `03_advanced/01_prompt_structure/prompt_builder.py` | 누락 변수와 빈 질문이 실패함을 검사하세요. |
| `D21-02-A01` | `03_advanced/02_examples_versions/example_design.py` | 예제 ID 901을 사용해 정상 답과 정보 부족 답을 완성하세요. |
| `D21-02-A02` | `03_advanced/02_examples_versions/example_design.py` | 같은 질문에 Zero-shot과 Few-shot Prompt를 각각 만드세요. |
| `D21-02-A03` | `03_advanced/02_examples_versions/example_design.py` | 변경점·가설·고정 조건과 두 Prompt를 저장하세요. |
| `D21-02-A04` | `03_advanced/02_examples_versions/example_design.py` | 예제 하나의 질문 표현만 바꾸고 새 버전으로 기록하세요. |
| `D21-02-A05` | `03_advanced/02_examples_versions/example_design.py` | Few-shot 예제에 D/H 질문과 답이 누출되지 않았는지 검사하세요. |
| `D21-02-A06` | `03_advanced/02_examples_versions/example_design.py` | 동일 버전 덮어쓰기 방지가 실제로 동작하는지 임시 폴더에서 검사하세요. |
| `D21-03-A01` | `03_advanced/03_task_decomposition/task_analysis.py` | 질문이 요구하는 사실과, 제공 자료가 지원하는 사실을 구분하세요. |
| `D21-03-A02` | `03_advanced/03_task_decomposition/task_analysis.py` | 하나라도 근거가 부족하면 수업의 정보 부족 상태를 선택하세요. |
| `D21-03-A03` | `03_advanced/03_task_decomposition/task_analysis.py` | 정상·정보 부족의 판단과 최종 출력 지시를 저장하세요. |
| `D21-03-A04` | `03_advanced/03_task_decomposition/task_analysis.py` | 위치와 기간을 함께 묻는 질문에서 빠진 사실을 확인하세요. |
| `D21-03-A05` | `03_advanced/03_task_decomposition/task_analysis.py` | 자료 누락과 상충하는 자료를 다른 이유로 기록하세요. |
| `D21-04-A01` | `03_advanced/04_context_builder/context_builder.py` | 선택 ID의 순서를 보존해 지식을 골라 JSON으로 직렬화하세요. |
| `D21-04-A02` | `03_advanced/04_context_builder/context_builder.py` | PPT의 가상 token 예산에서 근거 문맥에 남는 공간을 구하세요. |
| `D21-04-A03` | `03_advanced/04_context_builder/context_builder.py` | 포함·제외 ID와 원문·예산을 저장하세요. |
| `D21-04-A04` | `03_advanced/04_context_builder/context_builder.py` | 중복 선택은 제거하고, 스냅샷 중복 ID와 없는 ID는 오류인지 확인하세요. |
| `D21-04-A05` | `03_advanced/04_context_builder/context_builder.py` | 허용·유효성·관련성 검토를 선택 이유와 함께 적으세요. |
| `D21-04-A06` | `03_advanced/04_context_builder/context_builder.py` | 원문과 canonical JSON 해시를 함께 보존하고 순서 차이를 확인하세요. |
| `D21-05-A01` | `03_advanced/05_ab_evaluation/evaluation.py` | A의 규칙을 유지하면서 B에 근거 부족 규칙 한 개만 추가하세요. |
| `D21-05-A02` | `03_advanced/05_ab_evaluation/evaluation.py` | 개선용 D01~D03 세 질문만 선택하세요. |
| `D21-05-A03` | `03_advanced/05_ab_evaluation/evaluation.py` | 첫 응답만 골라 통과·미실행·미평가 개수를 기록하세요. |
| `D21-05-A04` | `03_advanced/05_ab_evaluation/evaluation.py` | source_mode별 결과를 분리하고 fixture 지표를 실모델 품질로 해석하지 마세요. |
| `D21-05-A05` | `03_advanced/05_ab_evaluation/evaluation.py` | 같은 질문·반복의 A/B 문맥 해시가 같은지 대조하세요. |
| `D21-05-A06` | `03_advanced/05_ab_evaluation/evaluation.py` | 같은 조건을 한 번 더 관찰하도록 반복 수를 설정하세요. |
| `D21-05-A07` | `03_advanced/05_ab_evaluation/evaluation.py` | 버전 정보·가설·변경점이 비어 있지 않은지 확인하세요. |
| `D21-06-A01` | `03_advanced/06_output_validation/contracts/schema.py` | PPT 50장의 엄격한 네 필드 계약을 선언하세요. |
| `D21-06-A02` | `03_advanced/06_output_validation/contracts/parser.py` | JSON 문법 실패와 Pydantic Schema 실패를 분리하세요. |
| `D21-06-A03` | `03_advanced/06_output_validation/contracts/rules.py` | 중복 출처와 이번에 제공하지 않은 출처를 서로 구분하세요. |
| `D21-06-A04` | `03_advanced/06_output_validation/contracts/rules.py` | 상태별 필드 조합과 공백·부족 고정문을 검사하세요. |
| `D21-06-A05` | `03_advanced/06_output_validation/validation.py` | 제공 fixture를 분류하고 모델 정의에서 Schema를 내보내세요. |
| `D21-06-A06` | `03_advanced/06_output_validation/validation.py` | ID 101을 붙인 서버 답변이 자동 검사만 통과하는 반례를 확인하세요. |
| `D21-06-A07` | `03_advanced/06_output_validation/validation.py` | 중복 키·NaN·과도한 크기·Schema 경계를 실제 반례로 검사하세요. |
| `D21-07-A01` | `03_advanced/07_bounded_retry/retry_policy.py` | 허용한 형식 오류만 안전한 한 문장 요약으로 수정 요청을 만드세요. |
| `D21-07-A02` | `03_advanced/07_bounded_retry/retry_policy.py` | 최초 1회+수정 1회까지만 반복하고 통과하지 못하면 None을 반환하세요. |
| `D21-07-A03` | `03_advanced/07_bounded_retry/retry_policy.py` | 네 fixture 순서의 호출 수 2·2·1·1을 확인하고 기록하세요. |
| `D21-07-A04` | `03_advanced/07_bounded_retry/retry_policy.py` | 첫 응답과 재시도 후 결과를 다른 필드로 집계하세요. |
| `D21-07-A05` | `03_advanced/07_bounded_retry/retry_policy.py` | 마지막 실패 뒤에는 수정 요청이 더 만들어지지 않는지 확인하세요. |
| `D21-07-A06` | `03_advanced/07_bounded_retry/retry_policy.py` | 비표준 오류 문자열을 모델 지시로 복사하지 않는지 검사하세요. |
| `D21-08-A01` | `03_advanced/08_daily_project/workflow.py` | 05에서 고정한 A/B 입력을 재사용하고 실행에 사용할 버전을 확인하세요. |
| `D21-08-A02` | `03_advanced/08_daily_project/workflow.py` | 로드한 출력 계약이 현재 검증 모델과 일치하는지 확인하세요. |
| `D21-08-A03` | `03_advanced/08_daily_project/workflow.py` | 최종 확인용 H01~H03만 골라 세 질문의 A/B 계획을 만드세요. |
| `D21-08-A04` | `03_advanced/08_daily_project/workflow.py` | 검증과 사람 평가를 합치되 미실행·미평가 상태를 그대로 남기세요. |
| `D21-08-A05` | `03_advanced/08_daily_project/workflow.py` | 첫 응답과 재시도 후 결과의 수를 분리하고 한 가지 개선안을 기록하세요. |
| `D21-08-A06` | `03_advanced/08_daily_project/workflow.py` | 출처 유형과 평가 대기 수를 공개하고 실측이 없으면 결론을 보류하세요. |
| `D21-08-A07` | `03_advanced/08_daily_project/workflow.py` | 가능하면 같은 조건의 최종 질문을 한 번 더 관찰하세요. |
