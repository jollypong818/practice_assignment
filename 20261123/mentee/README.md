# 수강생용 TODO · Day26 Basic RAG & LangChain

**2026-11-23(월) · 8개 실습 · 3수준**

질문 → 검색 결과 → Context → Prompt → 생성 → Validation → 출처 포함 API를 한 흐름으로 읽고 구현합니다. 현재 실습의 TODO를 직접 완성하고, 앞선 실습이 미완성이면 제공된 Checkpoint로 다음 주제를 시작할 수 있습니다.

## 어디서 시작하나요?

1. 이 `mentee` 폴더를 VS Code로 열고 기존 수업용 Python 환경을 선택합니다.
2. [Windows 준비 안내](docs/SETUP_WINDOWS.md)에 따라 패키지·`.env`를 준비합니다.
3. 한 수준을 선택하여 `01_rag_flow`부터 순서대로 진행합니다.
4. 각 폴더의 README → main.py/tasks.py → outputs → reports/review.md 순서로 확인합니다.

```bash
python -c "import sys; print(sys.executable)"
python tools/check_environment.py --group base
cd 01_basic/01_rag_flow
python main.py
python -m pytest -q tests
```

TODO를 채우기 전 `NotImplementedError: D26-...`로 멈추는 것이 정상입니다. 해당 ID의 요구사항과 힌트를 읽고 완성한 뒤 다시 실행합니다.

## 세 수준과 폴더

| 폴더 | 수행 방식 | 8개 실습의 TODO |
|---|---|---:|
| `01_basic` | 작은 함수 2개씩, main.py 한 파일에서 입력·출력 따라가기 | 16 |
| `02_intermediate` | 같은 흐름에 직접 완성할 부분·비교 조건 추가, tasks.py 분리 | 24 |
| `03_advanced` | 경계 조건·실패 사례·원문 대조 추가 | 32 |

특심화는 없습니다. 한 실습에서 세 수준을 모두 수행할 필요는 없습니다. 단계가 달라도 같은 핵심 개념을 학습하며, 앞 실습의 출력 파일을 다음 실습의 필수 입력으로 요구하지 않습니다.

## 강의와 실습 연결

**교안 기준:** `Day26_20261123_Basic_RAG_LangChain_강의실습연계수정.html` (총 82페이지). 21페이지의 VS Code 예제는 코드 역할을 설명하기 위한 구조이며 실습 ZIP과 파일 이름이 같지는 않습니다. [파일 역할 대응표](docs/LECTURE_CODE_MAP.md)를 확인합니다.


| 실습 폴더 | 강의 안내 페이지 | 완료할 핵심 |
|---|---:|---|
| 01_rag_flow | 9 | RAG 단계·입출력·원문 근거 확인표 |
| 02_hit_context | 18 | 같은 Hit에서 Context와 포함 ID 생성 |
| 03_langchain_objects | 30 | Document/Retriever/Prompt/Chat Model 역할 구분 |
| 04_document_adapter | 40 | 본문과 여섯 Metadata 필드 보존 |
| 05_prompt_model | 49 | Prompt 생성과 실제 모델 invoke 구분 |
| 06_context_chain | 59 | Context·출처를 보관하고 Runnable Chain 실행 |
| 07_validation | 70 | 형식·상태·허용 출처 검증과 원문 대조 |
| 08_rag_api | 80 | 실제 RAG API, result/sources와 200/422/502 확인 |

## 실행 종류

| 실습 | `python main.py` | 추가 선택 |
|---|---|---|
| 01~03 | 로컬 개념·문자열·대응표 | 실제 LLM 호출 없음 |
| 04 | 제공 Hit를 실제 Document로 변환 | `--live-db`: 실제 E5/DB 검색 Hit 변환 |
| 05 | 실제 Chat Model: 기본필수 1회, 응용/심화 2회 | `--offline`: 고정 응답으로 연결 확인 |
| 06 | 실제 Structured Model 1회 | `--offline`: 고정 bundle 관찰 |
| 07 | 고정 정상/오류 응답의 Validation | 실제 LLM 호출 없음 |
| 08 | 실제 DB·E5·LLM + TestClient, 모델 invoke 최대 2회 | `--offline`, `--serve`; 상위 수준 `--compare-k`는 모델 호출 최대 1회 추가 |

호출 횟수는 애플리케이션의 invoke 기준이며, 설정된 재시도 때문에 실제 HTTP 요청 수는 늘어날 수 있습니다. 단위 테스트는 네트워크를 사용하지 않습니다. 실습 08의 테스트는 서버를 따로 열 필요가 없습니다.

API Key가 없는 동안 05·06·08에서 `--offline`으로 연결과 중간값을 학습할 수 있습니다. **05·06의 실제 실행에는 LLM 설정만 필요하며 E5·DB 준비는 필요하지 않습니다.** 08의 실제 실행은 LLM과 E5·DB를 함께 준비합니다. 해당 준비를 마친 뒤 기본 실행의 실행 종류와 출처를 확인해야 실제 연동 성공으로 기록할 수 있습니다.

## 공통 폴더의 역할

| 경로 | 역할 |
|---|---|
| `coursekit/` | 앞 장의 Checkpoint, 실제 연결 도구, 명시적 Fixture |
| `data/raw/` | 강의와 같은 세 원문; 숫자·조건·출처 대조 |
| `data/lecture_hits.json` | 설명용 ID가 있는 고정 Hit |
| `tools/setup_db.py` | 제공 문서를 Day26 전용 PostgreSQL Schema(`d26_rag`)에 E5로 적재; 11/19 Schema를 그대로 사용하지 않음 |
| `tools/check_environment.py` | 현재 Python·패키지 확인 |
| `tools/run_all.py` | 선택한 수준의 8개 로컬 실행/테스트 |
| 각 실습 `expected/` | 완료 기준과 로컬 관찰 예시 |
| 각 실습 `outputs/` | 실행 시 생성하는 본인 결과 |
| 각 실습 `reports/review.md` | 원문 대조와 이유를 직접 기록 |

현재 학습할 TODO를 `coursekit`의 완성 함수 호출 한 줄로 대체하지 않습니다. 공유 코드는 진도 차이 때문에 앞 장에서 막히지 않도록 제공한 준비 코드입니다.

## 한 수준 전체를 로컬로 점검하기

역할 루트에서 실행합니다. 이 도구는 05·06·08에 자동으로 `--offline`을 붙입니다.

```bash
python tools/run_all.py --level 01_basic
python tools/run_all.py --level 01_basic --tests
```

일반적인 학습은 각 실습 폴더에서 하나씩 실행하면 됩니다. 전체 도구가 실패하면 첫 오류의 실습 이름과 TODO ID부터 확인합니다. 제출 항목과 자동 검사의 한계는 [결과 읽기](docs/OUTPUT_GUIDE.md), 검수 버전은 [제작 환경](docs/TESTED_ENVIRONMENT.md)에 정리했습니다.

마지막에는 [다섯 질문 대조](docs/FIVE_QUESTION_REVIEW.md)와 `data/api_requests.json`으로 실제 답변·출처를 확인합니다.
