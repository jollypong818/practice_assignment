# Day21 · Prompt·Context Engineering 실습

2026-11-16 · 수강생용: TODO가 있는 미완성 코드입니다.
기준: **Day21_Lecture_20261116.pptx, 총 86장**. PPT를 변경하지 않았습니다.

## 시작
`START_HERE.html` 또는 이 README를 여세요. **한 수준만 선택**합니다.

| 폴더 | 수준 | 구현 TODO | 구조 |
|---|---|---:|---|
| `01_basic` | 기본필수 | 25 | main.py에 변수·자료구조·호출·제어문 골격 제공 |
| `02_intermediate` | 응용 | 39 | 실행 main.py와 작업 analysis.py 분리 |
| `03_advanced` | 심화 | 50 | 목적별 모듈, Schema·parser·rules 분리, 제공 테스트 |

모든 수준이 Prompt·Context·검증·A/B·재시도를 다룹니다. 폴더 수나 B의 승리로 평가하지 않습니다.
`coursekit/`은 파일 기록과 교시별 독립 시작점을 위한 **제공 코드**입니다. 반드시 모두 직접 작성하는 과제가 아닙니다.
특히 05는 아직 06을 배우기 전이므로 완성 검증기를 제공하고, 06에서는 자신의 검사기를 구현합니다.
08은 앞서 완성한 개념의 제공 체크포인트를 이어 사용하고, 05의 **실제 frozen_bundle.json**을 받아 최종 확인을 합니다.

## 설치·실행 (Windows 11 / VS Code)
압축을 풀고 **mentee 폴더**를 VS Code로 엽니다. ZIP 안에서 직접 실행하지 않습니다.
기존 정상 가상환경에 Pydantic v2가 있으면 그대로 사용합니다. 다른 수업 환경을 무조건 업그레이드하지 않습니다.
```powershell
python tools/check_environment.py
```
새 가상환경이 필요할 때만:
```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe tools/check_environment.py
.\.venv\Scripts\python.exe 01_basic/01_prompt_structure/main.py
```
활성화 스크립트가 차단되면 위처럼 python.exe를 직접 지정합니다. 기관 보안 정책을 바꾸지 않습니다.
이후 각 README의 `python`은 **선택한 동일한 가상환경 Python**을 뜻합니다. VS Code의 Interpreter도 일치시킵니다.
Linux/macOS의 새 환경 Python 경로는 `.venv/bin/python`입니다.

## 진행 순서
| 순서 | 폴더 | 내용 | PPT | 실습 시간 |
|---|---|---|---|---|
| 1 | `01_prompt_structure` | Prompt 구조와 요구사항 | 7~13 | 25분 |
| 2 | `02_examples_versions` | Zero/Few-shot·버전 | 14~20 | 30분 |
| 3 | `03_task_decomposition` | 작업 분해와 정보 부족 | 21~27 | 30분 |
| 4 | `04_context_builder` | Context 선택·예산 | 28~36 | 25분 |
| 5 | `05_ab_evaluation` | 개선용 질문 A/B 비교 | 37~45 | 30분 |
| 6 | `06_output_validation` | JSON·Schema·참조 검증 | 46~55 | 25분 |
| 7 | `07_bounded_retry` | 실패 분류·최대 2회 | 56~63 | 30분 |
| 8 | `08_daily_project` | AI 지식 답변 생성기 v1 | 64~72 | 40분 |

01~04·06~07은 `python main.py`로 로컬 계산·작성한 샘플 검사를 수행합니다.
05·08은 **prepare → 실제 화면 실행·원문 등록 → review → 사람 평가 → review**입니다.
**prepare가 끝났다고 실제 모델 실험을 마친 것이 아닙니다.** raw 파일이 없는 항목은 미실행입니다.

## mentee TODO 완성법
`# BEGIN D21-...`와 `# END ...` 사이의 값·조건·연산·인자를 완성합니다.
`raise NotImplementedError("D21-...")`는 해당 블록을 다 채운 뒤 삭제합니다. **raise만 삭제해서 통과하려 하지 않습니다.**
기본필수는 최소 골격이 남아 있습니다. `None`, 빈 목록, `if False` 등은 의도적인 미완성 자리입니다.
수강생 코드의 실행 중단은 기대되는 상태이며, 각 README에서 목표와 결과를 확인합니다.

## 결과의 출처
- `design_only`: 작성한 Prompt·예제·작업 카드. 모델 품질 실험이 아닙니다.
- `fixture`: 교사가 작성한 정상/실패 문자열. 검사기와 재시도 **제어 흐름**만 확인합니다.
- `manual_chat`: 수강생이 실제 모델 화면에서 얻은 첫 응답을 수정하지 않고 등록한 관찰입니다.
API 호출·인증·사용량·비용·스트리밍 실습은 **11월 17일**입니다. 오늘 LLM API를 자동 호출하는 코드는 없습니다.
API 키·비밀번호·개인정보·실제 내부 문서를 입력하지 않습니다. 이 자료의 가상 지식만 사용합니다.

## 실험 규칙
D01~D03으로 개선하고 A/B 버전을 고정한 뒤 H01~H03으로 최종 확인합니다.
H 질문은 PPT에 공개되어 있습니다. 비공개 벤치마크라고 주장하지 않습니다.
같은 질문·문맥·예제 유무·출력 계약·모델 표시·실행 조건을 유지하고 **근거 규칙 한 가지**만 바꿉니다.
A와 B는 각각 새 대화에서 실행합니다. 웹 도구·개인화·모델 등 통제할 수 없는 조건은 미확인으로 남깁니다.
원문을 먼저 저장합니다. 실패 응답을 지우거나 수정 응답을 첫 응답처럼 기록하지 않습니다.
형식 수정은 최초+수정 **최대 2회**입니다. 출처 규칙 오류·정상 정보 부족·공급자 거절은 같은 방식으로 반복하지 않습니다.

## 결과 확인
`outputs/`는 실행 때 생성됩니다. `expected/`에는 예상 **로컬 검사 결과**만 있습니다.
모델 응답 문장이 예시와 완전히 같아야 하는 것은 아닙니다. 상태·출처·주장과 근거를 대조합니다.
기본필수도 공통 평가 100점이 가능합니다. AI 도구를 사용해도 각 코드가 왜 필요한지 설명해야 합니다.
문제 해결은 `docs/TROUBLESHOOTING.md`, 실제 응답 등록은 `docs/MANUAL_RUN_GUIDE.md`를 참고하세요.
