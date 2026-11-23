# 2026-11-24 · Day27 LangChain RAG Query Optimization & Reranking

**11월 24일 최종 HTML의 8개 Chapter, 8개 실습 안내(15·25·34·42·54·64·73·81페이지)**에 대응합니다.

**8개 실습 × 3수준 × 수강생·강사용 = 48개 독립 실습 폴더**입니다.

- `mentee/`: **수강생 TODO**. `README.md`에 요구사항·입력·출력·실행·완료기준 명시
- `mentor/`: **정답 및 해설**. 대응 함수에 절차·주의점 주석
- `01_basic`: 실습당 `main.py` 한 파일 중심. 구현 TODO 2개
- `02_intermediate`: `main.py` + `steps.py` + `checks.py`로 필요한 역할만 분리. TODO 3개
- `03_advanced`: 실제 역할과 책임에 따라 `api/`, `services/`, `retrieval/`, `policies/` 등 분리. TODO 4개

## 목표

Day26 Basic RAG의 Document→Retriever→Context→Prompt→Chat Model→Citation 구조를 재사용하고,
**Query Rewrite → Multi-query(선택) → E5 Candidate Retrieval → Cross-Encoder Reranking → Context → Generation → Validation**으로 확장합니다.

- 기존 Day26 ZIP을 직접 가져오거나 파일을 복사할 필요는 없습니다.
- Day27은 별도 `d27_rag` DB Schema와 **24개 교육용 청크**를 사용합니다. 실제 회사 자료가 아닙니다.
- 모델은 CUDA GPU를 기본으로 하며 **조용한 CPU Fallback을 사용하지 않습니다.**
- 각 실습은 독립 진입점으로, 이전 실습 미완료 시에도 제공 `coursekit/`에서 시작합니다.
- Gold Label은 평가 전용이며 Retriever나 Reranker에 입력하지 않습니다.

## 시작

1. 같은 번호의 실습에서 `01_basic`, `02_intermediate`, `03_advanced` 중 **하나만 선택**합니다.
2. 해당 폴더 `main.py`에서 TODO를 작성하고 `expected/EXPECTED.md`와 `reports/review.md`로 대조합니다.

## 기본 설치 명령 (Git Bash, 역할 폴더 기준)

```bash
py -3.12 -m venv .venv
source .venv/Scripts/activate
python -m pip install -U pip
# PyTorch CUDA Build는 먼저 공식 선택기로 설치 후 확인
python -m pip install -r requirements.txt
python -m pip install -r requirements_test.txt
python -m pip install -r requirements_live.txt
python tools/check_environment.py
```

**기본 실행**은 실제 DB·E5·Reranker·OpenAI API 연결을 사용합니다(실습 01 제외). API 요금이 발생할 수 있습니다.
로컬 로직 확인은 `--offline`을 붙입니다. 고정 순위·고정 점수를 성능 측정 결과로 제출하지 마세요.
