# 03_advanced · 실제 Uvicorn 실행

실습 08 TODO 4개를 완성하고 `.env`, pgvector, E5·CrossEncoder GPU 및 LLM API를 모두 준비해야 합니다.

역할 폴더에서 아래 명령으로 `03_advanced/08_enhanced_rag_api/` 위치로 이동합니다.

```bash
cd 03_advanced/08_enhanced_rag_api
python -m uvicorn app.main:create_app_factory --factory --host 127.0.0.1 --port 8000
```

브라우저에서 `http://127.0.0.1:8000/docs`를 엽니다. `POST /api/v1/rag/answer`에 질문을 입력합니다.

```json
{"query":"회의실 예약 취소 방법은?","category":"시설","history":[],"candidate_k":5,"context_k":2,"use_rewrite":true,"use_multiquery":false,"use_rerank":true}
```

`role` 필드는 입력받지 않습니다. 서버측 교육용 역할은 `learner`이며, 실제 업무 시스템에서는 인증·인가 미들웨어가 이를 결정해야 합니다.
