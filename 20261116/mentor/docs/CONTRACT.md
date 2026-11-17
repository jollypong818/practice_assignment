# 출력 계약 v1 — PPT 47~53, 78~79
이 계약은 기존 /api/knowledge CRUD 입력을 변경하는 것이 아니라, 지식 **답변 결과**의 새로운 계약입니다.

| 필드 | 규칙 |
|---|---|
| status | answered / insufficient_context |
| answer | 문자열 1~500자, 한국어 2문장 이내(Prompt·사람 확인); 공백만은 금지 |
| source_ids | 양의 정수 목록, 최대 3개, 중복 금지. bool·문자열 정수는 불허 |
| missing_information | 문자열 최대 200자 |

네 필드 모두 필수, 추가 필드는 금지합니다.
answered는 출처가 최소 1개이고 missing_information은 정확히 빈 문자열입니다.
insufficient_context는 출처 [], missing_information은 공백 아닌 부족한 사실 이름,
answer는 정확히 **제공된 지식으로는 답할 수 없습니다.** 입니다.
부분적으로만 답할 수 있는 질문은 이 수업에서 부족 상태로 처리합니다. 실제 서비스의 부분 답변 정책은 별도 버전으로 설계합니다.

| 검사 | 반환 오류 | 무엇을 검사하지 못하는가 |
|---|---|---|
| JSON | json_error | 자료형·사실성 |
| Schema | schema_error | 이번 문맥에 출처가 있는지 |
| 참조·상태 | duplicate_source / unknown_source / status_rule / blank_answer | 실제 본문이 주장을 뒷받침하는지 |
| 사람 검토 | evidence_ok·task_ok·insufficiency_ok | 모든 현실 사실에 대한 절대 보증 |

PPT 56장의 rule_error 범주는 이 자료에서 위의 구체적인 오류 이름으로 기록합니다.
`None` 오류는 자동 검사를 통과했다는 뜻이며 evidence_ok는 여전히 null입니다.
엄격 JSON의 크기·중복 키·NaN 거부는 부록 77장의 제공 보호 코드이며 basic의 추가 암기 과제가 아닙니다.
JSON Schema는 모델 정의의 model_json_schema()로 생성합니다. 공급자 API의 Structured Outputs 적용은 내일 다룹니다.
