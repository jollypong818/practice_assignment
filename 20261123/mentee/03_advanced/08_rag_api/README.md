# 실습 08 · FastAPI로 RAG 흐름 연결

**03_advanced · 심화 · 수강생 TODO / 강의 실습 안내 80페이지 (본문 72~79페이지)**

## 목표

검색 → Context → LangChain Generation → Validation → 출처 응답을 `/rag/answer`로 연결합니다. 정상 답변·근거 부족·요청 오류·실행 오류를 구분하고, 실제 Context 포함 문서와 응답 출처를 대조합니다.

## 먼저 알아야 할 용어

| 용어 | 의미 | 이번 실습 |
|---|---|---|
| Wiring | 준비한 부품을 입력·출력 계약에 맞게 연결 | Retriever·Generation → service → FastAPI |
| Dependency Injection | 함수가 사용할 부품을 외부에서 전달 | 실제 Runnable 또는 시험용 Fixture 주입 |
| candidate_k | 검색 결과 후보 수 상한 | 요청 1~20 |
| context_k | Context에 포함할 문서 수 상한 | 요청 1~3, 길이 예산도 적용 |
| TestClient | 서버 프로세스 없이 FastAPI 경로를 호출하는 도구 | 같은 HTTP 요청 검사를 현재 Python 프로세스에서 실행 |

## 준비할 것

1. 역할 폴더 README대로 기존 Python 가상환경, 기본·live 패키지를 확인합니다.
2. 역할 폴더의 `.env.example`을 참고해 `.env`에 DB 연결 및 `OPENAI_API_KEY`, `LLM_MODEL`을 설정합니다.
3. 역할 폴더에서 실행하는 `python tools/setup_db.py --apply` 안내를 따라 **Day26 전용 DB 자료**를 준비합니다. 11/19 파일을 import하거나 ID 201을 DB의 ID라고 가정하지 않습니다.
4. E5가 CPU에서 준비되고 DB의 문서 벡터와 같은 모델·차원·입력 접두어를 사용하는지 확인합니다.
5. TODO를 채운 뒤 아래 실제 경로로 진행합니다. 환경 준비 전에는 명시적 `--offline`으로 연결 구조만 확인할 수 있습니다.

## 입력과 출력

- 입력 JSON: `query, category, candidate_k, context_k`.
- `category`는 `학사/시설/지원` 중 하나이며 전체 검색을 뜻하는 값은 없습니다.
- 반환 JSON: `result`의 네 필드와, 서버가 실제 포함 문서에서 연결한 `sources`.
- 기본 실행 출력: `outputs/api_live_report.json`.
- `--offline` 출력: `outputs/api_fixture_report.json`. 두 실행 결과를 같은 파일로 덮어쓰지 않습니다.
- 각 요청에 검색 후보 ID, Context 포함 ID, 응답 출처 ID, 호출 시도 수, 외부 실행 여부를 기록합니다.

## 구현할 TODO

수정 대상은 **`tasks.py`**입니다. 이전 단계의 `coursekit`은 준비된 Checkpoint이고, 현재 TODO의 `wire_app`과 `make_request`는 직접 완성합니다.

| ID | 요구사항 |
|---|---|
| `D26-08-A01` | retriever와 generation을 make_rag_service에 연결한 뒤 create_app의 결과를 반환합니다. |
| `D26-08-A02` | query/category/candidate_k/context_k를 같은 이름의 네 Key로 묶어 반환합니다. |
| `D26-08-A03` | 원본 요청을 복사하고 context_k만 1로 바꾼 요청을 반환합니다. |
| `D26-08-A04` | 빈 검색 결과와 Timeout을 각각 run_fixed_failure로 실행한 두 결과를 반환합니다. |

## 실행 방법

VS Code의 Git Bash에서 현재 실습 폴더로 이동합니다.

```bash
# 실제 DB·E5·LLM + FastAPI 경로: 서버 프로세스는 띄우지 않음
python main.py
# 설정이나 외부 연결 없이 고정 Fixture로 API 경로 확인
python main.py --offline
# 자동 테스트는 외부 호출 없음
python -m pytest -q tests

# 같은 질문의 context_k만 바꾼 요청 1회 추가 (실제 모델 invoke 최대3회)
python main.py --compare-k
# Fixture로 같은 연결과 k 비교를 확인
python main.py --offline --compare-k
```

기본 smoke는 정상 질문 1회, 정확한 과제 마감 날짜 질문 1회, 잘못된 요청 1회입니다. **성공 경로에서 모델 `invoke`는 최대2회**이고 422 요청은 모델을 호출하지 않습니다. SDK에 `max_retries=1`이 있으므로 네트워크 문제 시 실제 전송 시도는 더 많을 수 있습니다. 재실행하면 유료 API 요청도 다시 발생합니다. 답변 문장은 모델·시점에 따라 달라지므로 고정 문장 일치를 정답으로 삼지 않습니다.

### 사용자 PC에서 HTTP 서버 실행

```bash
python main.py --serve
# 8000을 이미 사용 중이면:
python main.py --serve --port 8001
```

브라우저에서 `http://127.0.0.1:8000/docs`의 `POST /rag/answer`를 선택하고 다음 JSON을 보냅니다.

```json
{"query":"15분 늦으면 어떻게 기록되나요?","category":"학사","candidate_k":3,"context_k":2}
```

서버는 `Ctrl+C`로 종료합니다. `--serve`는 실제 연결용이며 `--offline`과 함께 사용하지 않습니다. 실제 서버 요청마다 필요에 따라 모델 호출이 발생합니다. smoke용 관찰 dict는 서버 요청 사이에 공유하지 않습니다.

## 확인 순서

1. 정상 응답 200에서 답변의 정수 ID와 `sources`의 ID 순서가 같은지 확인합니다.
2. `sources`의 ID가 `included_ids` 안에 있는지 확인합니다. 검색 후보에만 있던 ID는 허용하지 않습니다.
3. 마감 날짜 질문은 문서가 있어도 날짜 정보가 없어 `insufficient_context`가 기대됩니다.
4. candidate_k=0인 요청은 422이고 검색·생성을 호출하지 않는지 확인합니다.
5. 별도 `fixed_failure_examples`의 Timeout 502를 봅니다. **이 부분은 실제 실행 중에도 항상 Fixture 사례**입니다.
6. `reports/review.md`에 원문·조건·예외와 실제/Fixture 실행 범위를 기록합니다.

## 오류를 해석하는 방법

| 결과 | 의미 | 확인할 곳 |
|---|---|---|
| 200 + answered | 구조·출처 규칙을 통과한 답변 | 원문이 주장까지 지지하는지 대조 |
| 200 + insufficient_context | 현재 Context에서 답변 근거 부족 | 관련 문서·정확한 정보 존재 여부 |
| 422 | 요청 자료형·범위·허용 필드 오류 | 요청 JSON, 두 k, 빈 질문 |
| 502 + retrieval_error | 검색 단계 실패 | DB 설정·Schema·E5 준비 |
| 502 + generation_error | 모델 호출 실패 | 인증·모델 접근·네트워크·Timeout |
| 502 + output_parsing_error | 생성 결과를 WireAnswer로 해석하지 못함 | Structured Output 지원과 결과 형식 |
| 502 + answer_validation_error | 출처 또는 상태 업무 규칙 실패 | 포함 ID·중복·상태 조합 |

API Key와 DB 비밀번호는 결과표에 넣지 않습니다. DB·API가 실패하면 Fixture로 자동 전환하지 않습니다. 고정 입력 검사가 통과했어도 실제 DB·모델 성공으로 기록하지 않습니다.

## 완료 기준

실제 연결에서 공통 세 요청의 200/200/422와 출처 연결을 확인합니다. 별도 502 Fixture와 근거 부족의 차이를 설명하고 원문 대조를 남깁니다. 환경을 준비하지 못한 경우에는 `--offline` 관찰까지 완료한 것으로 적고 실제 DB·Embedding·LLM 연동은 미실행으로 남깁니다.
