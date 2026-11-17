# 오류 해결 순서

| 증상 | 확인과 조치 |
|---|---|
| [미완성 TODO] | 해당 ID의 코드 골격을 채우고 raise 줄만 마지막에 삭제합니다. |
| ModuleNotFoundError: pydantic | 실행한 python의 경로를 확인하고 같은 환경에 requirements.txt를 설치합니다. |
| model_validate/model_json_schema 없음 | Pydantic v1이 아닌 v2 Interpreter인지 확인합니다. |
| 이미 있는 실험 | --run dev_02처럼 새 이름으로 보존합니다. 기존 실패 원문을 지우지 않습니다. |
| completed지만 원문 없음 | record_manual.py --raw-file로 실제 응답 파일을 등록합니다. |
| 원문 해시가 다름 | 등록 뒤 raw.txt를 수정하지 않습니다. 원본을 복구하거나 별도 새 실험으로 분리합니다. |
| Prompt·문맥 해시가 다름 | freeze 이후 파일을 수정했습니다. 현재 실험의 입력을 복구하거나 새 버전을 만듭니다. |
| json_error | 코드 블록·닫는 괄호·중복 키·크기를 확인합니다. 원문을 몰래 수정하지 않습니다. |
| schema_error | 네 필드 필수·추가 필드 금지·출처 int·문자열 길이를 확인합니다. |
| unknown_source | 전체 DB ID가 아니라 **이번 요청에서 제공한 ID**와 비교합니다. 901은 예제 ID입니다. |
| status_rule | answered/부족 상태별 출처·부족 정보·고정문을 확인합니다. |
| CSV 한글/공백 칸 | CSV는 UTF-8 BOM입니다. 빈 칸은 미평가일 수 있으니 summary.json의 null/분모를 봅니다. |
| 새 실험은 다 미실행 | 정상입니다. prepare는 Prompt와 기록 틀만 만듭니다. 실제 응답을 등록해야 합니다. |
| API 서버/DB가 없음 | 오늘 필수는 고정 knowledge_v1.json입니다. 새 DB나 서버를 만들 필요가 없습니다. |
| ChatGPT 실행 불가 | 로컬 검증은 fixture로 계속하되, 실제 A/B는 not_run+이유로 남깁니다. |

파일명·폴더명은 모두 영문입니다. 예제 한글은 UTF-8 텍스트로 보존합니다.
전날 학습 폴더와 DB를 초기화하지 않습니다. 키·비밀번호를 오류 화면이나 기록지에 붙이지 않습니다.
