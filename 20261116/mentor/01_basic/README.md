# 01_basic

강사용: 정답이 완성된 코드입니다. 실제 모델 응답·평가는 자동으로 채우지 않습니다.
**이 수준 하나로 01~08을 진행**합니다. 세 수준을 차례대로 모두 끝내는 과제가 아닙니다.

| 실습 | 구현 블록 | 내용 |
|---|---:|---|
| `01_prompt_structure` | 3 | Prompt 구조와 요구사항 |
| `02_examples_versions` | 3 | Zero/Few-shot·버전 |
| `03_task_decomposition` | 3 | 작업 분해와 정보 부족 |
| `04_context_builder` | 3 | Context 선택·예산 |
| `05_ab_evaluation` | 3 | 개선용 질문 A/B 비교 |
| `06_output_validation` | 4 | JSON·Schema·참조 검증 |
| `07_bounded_retry` | 3 | 실패 분류·최대 2회 |
| `08_daily_project` | 3 | AI 지식 답변 생성기 v1 |

`main.py`는 모두 동일한 실행 입구입니다. basic은 main.py 안의 골격,
intermediate는 analysis.py, advanced는 목적별 모듈에서 TODO를 채웁니다.
각 교시를 독립 시작할 수 있도록 앞 개념의 완성 체크포인트를 제공합니다.
실제 모델 응답은 준비 코드가 생성하지 않습니다. 05/08에서 직접 관찰·등록합니다.
