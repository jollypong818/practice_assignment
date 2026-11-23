# Day26 강의 21페이지와 실제 실습 코드의 연결

강의 21페이지의 `rag_intro/app/`은 **실무형 서비스 책임 분리 예시**입니다. LangChain이 강제하는 디렉터리 구조가 아니며 실습 ZIP에 동일한 이름의 파일이 있다는 뜻도 아닙니다.

| 강의에서 보는 파일·역할 | 이번 배포 실습에서 확인할 코드 |
|---|---|
| `retrieval.py` — 검색·Context | `coursekit/live.py`, `coursekit/checkpoints.py` |
| `prompts.py` — Prompt 구성 | `coursekit/checkpoints.py`의 `make_prompt()` |
| `model.py` — Chat Model 구성 | `coursekit/llm.py` |
| `chain.py` — RAG 연결 | `coursekit/checkpoints.py`의 Chain·서비스 구성 함수 |
| `main.py` — 실행 진입점 | 각 실습의 `main.py`, 응용·심화의 `tasks.py` |

**실행 기준:** 실제 서비스는 `tools/setup_db.py --apply`로 제공 문서를 Day26 전용 `d26_rag` Schema에 넣습니다. 11월 19일에 배운 Indexing 개념을 재사용하지만 기존 DB 테이블이나 고정 예시 ID 201을 그대로 사용하는 것은 아닙니다.

**구현 순서:** 01–03은 처리 흐름·자료형, 04는 `Document`, 05–06은 실제 Model·Runnable, 07은 Validation, 08은 E5·DB·LLM·FastAPI 통합입니다. 앞 실습의 결과 파일을 다음 실습에서 요구하지 않습니다.
