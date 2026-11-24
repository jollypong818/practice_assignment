# API 라우팅의 목적

- 실제 ASGI Factory: `app/main.py` → `app/retrieval/stages.py`의 Chain → `app/services/rag_service.py`의 Service → `coursekit.api.create_app()`
- `app/api/routes.py`에는 HTTP 응답 검사 TODO가 있습니다. HTTP 경로 등록은 `coursekit.api.create_app()`에서 완성된 코드로 제공합니다.
- 학습 초점: 책임 구분. FastAPI Router를 불필요하게 이중 등록하지 않습니다.
