# 실습 05 · Prompt와 Chat Model

**01_basic · 기본필수 · 수강생 TODO**  
강의 연결: 11월 23일 HTML 42~49페이지 (실습 안내 49페이지). 세 수준 중 하나를 선택합니다.

## 목표와 준비

질문·Context로 메시지를 만들고 실제 모델 응답과 구분합니다. 앞 실습이 미완성이어도 이 폴더와 제공된 `coursekit/`만으로 시작할 수 있습니다. 다른 날짜의 실습 폴더를 가져오지 않습니다.

- **ChatPromptTemplate**: 규칙과 입력 변수로 메시지를 만드는 틀입니다. 객체를 준비하는 일과 실행하는 일은 다릅니다.
- **ChatPromptValue**: `prompt.invoke()`가 만든 메시지 묶음입니다. 아직 모델 답변이 아닙니다.
- **Chat Model / AIMessage**: 모델에 메시지를 보내면 `AIMessage`가 돌아옵니다. 이번 실습에서는 `.text`로 텍스트를 관찰합니다.
- **Context**: 답변에 참고하도록 전달한 원문입니다. 관련 문서가 있다는 사실만으로 질문에 답할 수 있는 것은 아닙니다.

## 구현할 부분

수정 파일: **`main.py`**. 함수와 실행 코드를 한 파일에서 읽습니다.

| ID | 완료할 작업 |
|---|---|
| `D26-05-B01` | 질문과 Context를 각각 question·context Key로 묶어 반환합니다. |
| `D26-05-B02` | Prompt를 먼저 실행하고 그 반환값을 Chat Model에 전달한 뒤 두 반환값을 함께 반환합니다. |

## 실행 순서 · Windows 11 / VS Code / Git Bash

1. ZIP을 풀고 `mentee/`를 VS Code로 엽니다. 기존 수업용 Python 환경을 선택합니다.
2. 역할 폴더 루트 README의 패키지·`.env` 준비를 완료합니다. `.env.example`을 복사하여 `OPENAI_API_KEY`, `LLM_MODEL`을 설정합니다. 키와 비밀번호는 코드·보고서에 적지 않습니다.
3. Terminal에서 `01_basic/05_prompt_model` 폴더로 이동합니다.
4. TODO를 작성한 뒤 다음을 실행합니다.

```bash
python main.py
```

이 명령의 기본 경로는 **실제 Chat Model 호출 1회**입니다. 서버가 오류를 반환하면 설정된 재시도로 실제 HTTP 요청은 더 발생할 수 있습니다. 사용량과 비용은 모델·응답에 따라 달라집니다. 정상 결과는 `outputs/prompt_model.json`에 저장됩니다. 실제 문장은 매번 같다고 가정하지 않습니다.

모델 설정을 기다리는 동안 고정 예시로 코드 연결을 확인하려면 다음을 명시적으로 실행합니다.

```bash
python main.py --offline
python -m pytest -q tests
```

`--offline`은 실제 LLM을 실행하지 않습니다. 로컬의 LangChain 객체와 교육용 고정 응답을 연결합니다. 고정 응답의 문장·ID를 실제 API 실측 결과로 기록하지 않습니다. 자동 테스트는 항상 로컬 Spy/Fixture만 사용합니다.

TODO가 남은 수강생 파일은 지정된 `NotImplementedError`로 중단됩니다. 이는 정상적인 시작 상태이며, 해당 블록을 구현한 뒤 다시 실행합니다.

## 결과를 읽는 방법

- `execution`과 `real_model_calls`로 실행 종류를 확인합니다. 실제 모델이 실패했는데 정상 응답으로 포장하지 않습니다.
- `prompt_messages`는 모델에 보낸 입력, `response`는 돌려받은 응답입니다. 두 항목의 역할이 다릅니다.
- `human_evidence_review=pending`은 사람이 원문과 답변을 대조해야 한다는 뜻입니다. 프로그램 실행 완료가 정답 승인은 아닙니다.
- 상세 조건은 `expected/EXPECTED.md`, 확인 질문은 `reports/review.md`에 있습니다.

## 흔한 문제와 확인 위치

| 현상 | 확인할 부분 |
|---|---|
| `NotImplementedError: D26-...` | 해당 TODO 블록이 아직 남았습니다. |
| `ModuleNotFoundError` | 역할 루트의 준비 안내와 `python -c "import sys; print(sys.executable)"`로 현재 환경을 확인합니다. |
| API Key·모델 설정 누락 | `.env` 위치는 현재 실습 폴더가 아니라 `mentee/` 루트입니다. |
| 401 / 인증 실패 | Key의 유효성·접근 권한을 확인합니다. 값 자체는 보고서에 붙이지 않습니다. |
| 429 / Timeout | 요청 제한 또는 호출 실패입니다. `insufficient_context`로 바꿀 수 없습니다. |
| 입력 변수 `context` 누락 | Prompt의 입력 Key를 확인합니다. 이 오류는 모델 호출보다 먼저 발생합니다. |
| 응답의 내용이 원문과 다름 | 원문과 응답을 대조하여 기록합니다. 문자열이 생성되었다는 이유로 정답 처리하지 않습니다. |

## 공식 참고 자료

- [LangChain ChatPromptTemplate](https://reference.langchain.com/python/langchain-core/prompts/chat/ChatPromptTemplate)
- [LangChain ChatOpenAI output_version](https://reference.langchain.com/python/langchain-openai/chat_models/base/BaseChatOpenAI/output_version)
