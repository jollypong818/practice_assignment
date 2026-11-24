# Day27 실습 07 · 검색 개선 전후 비교 — 심화

**강의 HTML 73페이지**에 대응합니다. 핵심 학습 목표는 **같은 질문·문서·필터에서 Baseline과 Reranking 결과를 비교합니다.**입니다.

## 1. 학습 전 확인

- 11월 23일에 학습한 LangChain `Document`·`Runnable`·`invoke()`와 출처 Metadata를 복습합니다.
- `coursekit/`의 제공 코드는 이전 실습을 끝내지 못한 학생도 현재 과제를 시작할 수 있게 도와줍니다.
- 같은 실습에서 **현재 선택한 수준 하나만** 수행합니다. 세 단계 전체를 모두 풀지 않습니다.
- **심화**: 책임에 따라 API·Policy·Service 등 분리.

## 2. 파일의 역할

```text
07_before_after/
  main.py
  metrics/__init__.py
  metrics/topk.py
  policies/__init__.py
  policies/control.py
  reports/__init__.py
  reports/summary.py
  services/__init__.py
  services/audit.py
  tests/test_exercise.py
  expected/EXPECTED.md     # 반드시 확인할 결과
  reports/review.md        # 본인이 직접 해석
  tests/test_exercise.py   # 현재 단계 테스트
```

`main.py`가 실행 진입점이며, 상위 역할 폴더의 `coursekit/`는 이전 Chapter의 제공 실행 기능입니다.

## 3. 수강생 수행 요구사항

| TODO ID | 수정할 함수 | 성공 기준·힌트 |
|---|---|---|
| `D27-07-A01` | `compare_rankings()` | 고정한 관련 문서 ID를 Top-2에 포함했는지 확인합니다. |
| `D27-07-A02` | `interpret_change()` | 순위가 바뀌어도 반드시 개선됐다는 결론을 내리지 않습니다. |
| `D27-07-A03` | `check_conditions()` | Gold Label은 검색과 Reranker의 입력이 아니라 평가할 때만 사용합니다. |
| `D27-07-A04` | `audit_comparison()` | 시간·실행모드·비교 조건을 기록하고 단일 사례로 성능 개선을 단정하지 않습니다. |

**실행 후 무엇을 확인하는가?**

- 같은 질문·필터·Corpus에서 비교
- Gold Label은 평가 전용
- Latency 실제 측정과 fixture 구분

## 4. 실행 절차 (Windows 11 · VS Code)

1. ZIP을 압축 해제하고 `mentor/README.md`를 참고하여 같은 역할 폴더에서 `.venv`를 준비합니다.
2. `main.py`와 TODO 위치를 읽고 코드를 완성합니다. 오류 메시지가 뜨면 해당 TODO ID를 확인합니다.
3. 역할 폴더를 작업 디렉터리로 열어 아래 경로에서 실행합니다.

```bash
# 역할 폴더에서 실행 (venv 활성화 상태)
python 03_advanced/07_before_after/main.py --offline
# 실제 LLM·GPU·DB 준비 완료 후 실행 (실습01은 고정 진단)
python 03_advanced/07_before_after/main.py
# 테스트: 실습 폴더로 이동해 실행
cd 03_advanced/07_before_after
python -m pytest -q tests
```

4. `outputs/`에 저장된 JSON을 확인하고, `expected/EXPECTED.md`와 비교합니다.
5. `reports/review.md`에 실제 원문·근거·결과·실행 모드를 구분하여 작성합니다.

## 5. 완료 기준 및 주의사항

- 모든 TODO에서 NotImplementedError를 제거하고 예상한 자료형을 반환합니다.
- 실습 시작·종료 사이의 **값의 전달 과정**을 본인 말로 설명할 수 있어야 합니다.
- 기본 실행은 외부 서비스/모델 연결 경로입니다. 01번은 교육용 고정 진단입니다.
- `--offline`에서 표시한 고정 점수·질문 변환 결과를 **실제 성능으로 보고하면 안 됩니다**.
- 05·07번에서 Cross-Encoder는 실제 GPU에서 추론해야 하며 CPU 자동 전환은 없습니다.
- `source_ids`의 구조 검증과 답변 내용의 Grounding은 다른 검사입니다.

## 6. 강사 확인 사항

- 대상 강의 페이지: 73. 실습 목표와 요구사항·출력 필드를 대조합니다.
- `tests/` 검사 통과뿐 아니라 원문 근거·권한·버전·오류 처리 이유를 설명하는지 확인합니다.
