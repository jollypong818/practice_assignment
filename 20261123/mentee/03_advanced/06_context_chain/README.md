# 실습 06 · Context와 Runnable 연결

**03_advanced · 심화 · 수강생 TODO**  
강의 연결: 11월 23일 HTML 51~59페이지 (실습 안내 59페이지). 세 수준 중 하나를 선택합니다.

## 목표와 준비

Context·포함 출처를 보관하고 Prompt와 Structured Model을 연결합니다. 앞 실습이 미완성이어도 이 폴더와 제공된 `coursekit/`만으로 시작할 수 있습니다. 다른 날짜의 실습 폴더를 가져오지 않습니다.

- **Runnable / invoke**: 입력을 받아 실행하는 LangChain의 공통 인터페이스입니다. `|`는 앞 단계의 출력을 뒤 단계로 전달합니다.
- **Structured Output / WireAnswer**: 생성할 `status`, `answer`, `source_ids`, `missing_information` 네 필드의 형식입니다.
- **bundle**: `include_raw=True`일 때 받는 `raw`, `parsed`, `parsing_error`의 묶음입니다. 이 묶음을 받았다는 사실이 업무 규칙 검증 통과를 뜻하지 않습니다.
- **included_docs**: 길이·개수·중복 처리 뒤 실제 Context에 포함한 문서입니다. 출처는 이 목록과 연결합니다.
- **문자 길이 / Token 수**: `len(context)`는 이 실습의 단순 문자 예산입니다. 모델의 Token 수나 Context Window와 같지 않습니다.

## 구현할 부분

수정 파일: **`tasks.py`**. `main.py`는 실행 진입점입니다.

| ID | 완료할 작업 |
|---|---|
| `D26-06-A01` | build_context로 Context와 포함 문서를 얻고, 포함 ID 및 Prompt 입력을 함께 반환합니다. |
| `D26-06-A02` | 빈 Context에서는 None을 반환하고, 나머지는 Prompt와 Structured Model을 연결하여 bundle을 받습니다. |
| `D26-06-A03` | 기본·중복 청크 추가·max_items=1 조건을 각각 실행하여 포함 ID를 비교합니다. |
| `D26-06-A04` | 첫 Document 블록 길이보다 1자 작은 상한과 정확한 길이의 상한에서 포함 여부를 비교합니다. |

- 중복 청크 추가와 `max_items=1` 변경을 각각 적용합니다. 이 비교는 로컬에서만 하므로 모델 요청을 추가하지 않습니다.
- 문자 상한을 한 블록 길이 직전·정확한 값으로 비교하고, 빈 Context에서는 모델 호출을 생략합니다.

## 실행 순서 · Windows 11 / VS Code / Git Bash

1. ZIP을 풀고 `mentee/`를 VS Code로 엽니다. 기존 수업용 Python 환경을 선택합니다.
2. 역할 폴더 루트 README의 패키지·`.env` 준비를 완료합니다. `.env.example`을 복사하여 `OPENAI_API_KEY`, `LLM_MODEL`을 설정합니다. 키와 비밀번호는 코드·보고서에 적지 않습니다.
3. Terminal에서 `03_advanced/06_context_chain` 폴더로 이동합니다.
4. TODO를 작성한 뒤 다음을 실행합니다.

```bash
python main.py
```

이 명령의 기본 경로는 **실제 Chat Model 호출 1회**입니다. 서버가 오류를 반환하면 설정된 재시도로 실제 HTTP 요청은 더 발생할 수 있습니다. 사용량과 비용은 모델·응답에 따라 달라집니다. 정상 결과는 `outputs/context_chain.json`에 저장됩니다. 실제 문장은 매번 같다고 가정하지 않습니다.

모델 설정을 기다리는 동안 고정 예시로 코드 연결을 확인하려면 다음을 명시적으로 실행합니다.

```bash
python main.py --offline
python -m pytest -q tests
```

`--offline`은 실제 LLM을 실행하지 않습니다. 로컬의 LangChain 객체와 교육용 고정 응답을 연결합니다. 고정 응답의 문장·ID를 실제 API 실측 결과로 기록하지 않습니다. 자동 테스트는 항상 로컬 Spy/Fixture만 사용합니다.

TODO가 남은 수강생 파일은 지정된 `NotImplementedError`로 중단됩니다. 이는 정상적인 시작 상태이며, 해당 블록을 구현한 뒤 다시 실행합니다.

## 결과를 읽는 방법

- `execution`과 `real_model_calls`로 실행 종류를 확인합니다. 실제 모델이 실패했는데 정상 응답으로 포장하지 않습니다.
- `context`·`included_ids`·`included_sources`와 `bundle`을 함께 봅니다. Context에 빠진 문서의 ID를 허용 출처로 쓰지 않습니다.
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
| parsed가 None / parsing_error가 존재 | raw와 parsing_error를 읽습니다. 임의의 정상 객체를 만들어 덮어쓰지 않습니다. |

## 공식 참고 자료

- [LangChain Structured Output](https://reference.langchain.com/python/langchain-openai/chat_models/base/ChatOpenAI/with_structured_output)
- [LangChain RunnableSequence](https://reference.langchain.com/python/langchain-core/runnables/base/RunnableSequence)
