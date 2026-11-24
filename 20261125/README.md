# Day28 수강생용 TODO · 시작 안내

Day28의 8개 Chapter 실습을 기존 LangChain RAG에 연결합니다.

## 실제 시작 명령 (Git Bash, 현재 역할 폴더)

```bash
py -3.12 -m venv .venv
source .venv/Scripts/activate
# PyTorch CUDA Build는 공식 설치 선택기에서 먼저 설치
python -m pip install -r requirements.txt
python -m pip install -r requirements_test.txt
python -m pip install -r requirements_live.txt
python tools/check_environment.py
python tools/validate_dataset.py
```

## 1개 과제를 선택하는 방법

1. `01_basic`, `02_intermediate`, `03_advanced` 중 하나를 선택합니다.
2. `01_failure_diagnosis`에서 시작하거나 당일 필요한 실습 번호를 선택합니다.
3. 실습 폴더의 **`README.md`**를 먼저 읽고 TODO 함수명·입력·출력·완료 기준을 확인합니다.
4. `python 01_basic/01_failure_diagnosis/main.py --offline` 등으로 실행합니다.
5. 결과는 각 실습 폴더의 `outputs/result.json`에 저장됩니다.
6. `python -m pytest -q 01_basic/01_failure_diagnosis/tests` 등으로 검사합니다.

## 난이도별 파일 구조

- `01_basic`: `main.py` 한 파일에서 TODO 2개
- `02_intermediate`: `main.py` + `steps.py` + `checks.py`에서 TODO 3개
- `03_advanced`: 목적별 `app/` 하위 모듈에 TODO 4개. 각 실습이 실제 필요로 하는 책임만 분리

## 강의와 대응하는 8개 과제

| 실습 | HTML 페이지 | 설명 |
|---|---:|---|
| 01 | 9p | `01_failure_diagnosis` | 질문의 실패 단계와 조치 근거를 기록합니다. |
| 02 | 18p | `02_gold_dataset` | 질문별 Gold 문서와 무정답 질문을 구분합니다. |
| 03 | 25p | `03_retrieval_metrics` | Top-k 검색 품질 지표의 분자·분모를 직접 계산합니다. |
| 04 | 33p | `04_ranking_metrics` | 문서 순서와 Gold 등급을 이용해 순위 지표를 계산합니다. |
| 05 | 42p | `05_generation_quality` | Claim의 근거 일치와 질문 적합성·정답성을 구분합니다. |
| 06 | 51p | `06_langchain_runner` | 정답을 Target으로 전달하지 않고 Runnable.invoke 결과를 평가합니다. |
| 07 | 60p | `07_debug_comparison` | 한 번에 하나의 기능을 변경하여 성능 차이와 실패 원인을 진단합니다. |
| 08 | 68p | `08_agent_quality_report` | Retrieval/Generation 평가를 연결하고 Agent Tool의 1차 준비 기준을 검토합니다. |

## 실행·채점 원칙

- 기본은 **`--offline`**입니다. 모델 미호출 고정 데이터로 수식·입출력 구조를 학습합니다.
- 실습 06~08은 GPU/DB/API 설정 후 **`--live`**를 명시한 경우에만 실제 모델과 DB를 호출합니다.
- 오프라인 지표를 실제 모델 성능이라고 발표하지 마세요.
- No-answer는 `Recall=None`이며 Retrieval 평균에서 제외합니다.
- Gold/Reference는 Target 입력에서 제거하고 Evaluator에서만 사용합니다.
- Reranker가 Context를 잘못 선정한 오류와 LLM이 근거 없는 사실을 생성한 오류는 분리합니다.

## 문서 안내

- `docs/ENVIRONMENT_SETUP.md`: Windows 11·VS Code·CUDA·PostgreSQL/pgvector·LLM API 상세설정
- `docs/LECTURE_CODE_MAP.md`: HTML 페이지 ↔ 파일 경로 ↔ 실행 순서
- `docs/GLOSSARY.md`: 처음 만나는 용어의 정의와 업무 사용 위치
- `data/README.md`: Gold·원문·고정 결과의 구분
- 각 실습의 `expected/EXPECTED.md`: 정상 결과의 의미와 확인 기준
- 각 실습의 `reports/review.md`: 수행 기록·해석·실패 원인 작성

## 매우 중요한 주의사항

실습 목적은 **평가 결과를 실제 업무 의사결정으로 이어 가는 역량**입니다. 높은 점수만 확인하지 말고, 데이터 버전·권한·출처·실패 케이스와 함께 해석해야 합니다.

**수강생:** `mentor/` 정답 파일은 포함되어 있지 않습니다. TODO를 완성하기 전 테스트가 실패하는 것은 의도된 동작입니다.

## 선택적 심화 확장: 실제 LLM Judge

`python tools/run_judge_live.py --case-id G01 --confirm-paid-api` — 명시적 유료 API 호출 시에만 실행. 합성 Claim을 JSON Schema로 평가하지만 사람 검수를 대체하지 않습니다.
