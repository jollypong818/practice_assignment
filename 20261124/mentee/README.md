# Day27 · LangChain RAG 확장 · 수강생용 TODO

실습 01~08은 최종 HTML **15·25·34·42·54·64·73·81페이지**의 실습 안내와 대응합니다.

> 프로젝트를 VS Code에서 열 때 **이 `mentee` 폴더 자체를 여세요.**
> `01_basic`, `02_intermediate`, `03_advanced` 중 하나를 골라 실습합니다.

## 1. 먼저 설치

`docs/ENVIRONMENT_SETUP.md`를 **위에서부터** 따라 하세요.

## 2. 실습 실행 순서

```bash
# 현재 폴더 = mentee/, .venv 활성화 상태
python tools/check_environment.py
python 01_basic/01_failure_diagnosis/main.py --offline
python 01_basic/02_query_rewrite/main.py --offline
# 본인의 TODO 완성 후 실습별 실행. 실제 모델 경로는 --offline 생략
python 01_basic/05_cross_encoder_reranking/main.py
```

- `01_basic`: `main.py`에서 TODO 2개를 완성합니다.
- `02_intermediate`: `steps.py`와 `checks.py`에서 기능·검사를 나눕니다.
- `03_advanced`: 폴더를 역할별로 분리하되, 불필요한 파일은 만들지 않습니다.

## 3. 실습 번호·페이지·학습 결과

| 번호 | HTML | 학습 내용 |
|---|---:|---|
| 01 | 15 | 실패 위치 진단 (고정 사례) |
| 02 | 25 | History를 독립적인 검색 Query로 변환 |
| 03 | 34 | Multi-query 후보 병합·중복 제거 |
| 04 | 42 | E5/pgvector 후보·Metadata 계약 |
| 05 | 54 | GPU CrossEncoder Reranking |
| 06 | 64 | LangChain Runnable Pipeline 통합 |
| 07 | 73 | Baseline과 재정렬 후 결과 비교 |
| 08 | 81 | FastAPI 연결·출처·실패 검증 |

## 4. 모드와 환경

- `--offline`: 실제 DB·Embedding·LLM·CrossEncoder를 호출하지 않습니다. `fixed fixture`를 사용하는 교육용 경로입니다.
- 기본 실행: 실습 02~08은 필요한 **실제** 모델 또는 DB/API를 호출합니다. API 사용 비용에 주의하십시오.
- 실습 01은 별도의 실제 모델 호출이 없는 고정 실패 진단 실습입니다.
- `01_basic`을 성공하지 못해도 `02_intermediate`나 다음 실습을 시작할 수 있습니다.
- `coursekit/`는 제공된 독립 실행용 이전 단계 Checkpoint입니다. 이 폴더를 함부로 수정하지 마세요.
- 실습 08은 FastAPI `TestClient`로 HTTP 처리 흐름을 검증합니다. Advanced에는 실제 Uvicorn 실행 경로도 포함합니다.

## 5. 평가 기준

**TODO 완료 · 실제 입출력 확인 · 출처 ID 보존 · 상황별 오류 분리 · 본인 말로 원리 설명**을 평가합니다.
`reports/review.md`에 실행 모드를 명확히 표시하세요. 자동 Test 통과는 Grounding을 보장하지 않습니다.
