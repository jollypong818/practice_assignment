# 08 · AI 지식 답변 생성기 v1

PPT **64~72장**, 실습 약 **40분**. 수강생용: TODO가 있는 미완성 코드입니다.

## 목표
05에서 고정한 A/B를 H01~H03에 적용하고 입력·검증·평가 흐름을 연결합니다.

## 편집할 파일
`analysis.py`
`# BEGIN/END` 블록의 골격을 완성하고 해당 NotImplementedError 줄을 지웁니다.
각 TODO는 요구·입력·완료 기준을 주석으로 함께 설명합니다.

| 블록 | 요구사항 |
|---|---|
| `D21-08-I01` | 05에서 고정한 A/B 입력을 재사용하고 실행에 사용할 버전을 확인하세요. |
| `D21-08-I02` | 최종 확인용 H01~H03만 골라 세 질문의 A/B 계획을 만드세요. |
| `D21-08-I03` | 검증과 사람 평가를 합치되 미실행·미평가 상태를 그대로 남기세요. |
| `D21-08-I04` | 첫 응답과 재시도 후 결과의 수를 분리하고 한 가지 개선안을 기록하세요. |
| `D21-08-I05` | 가능하면 같은 조건의 최종 질문을 한 번 더 관찰하세요. |

## 실행 위치
터미널에서 **이 README가 있는 폴더**로 이동합니다. `python`은 선택한 가상환경입니다.
```powershell
python main.py prepare --run holdout_01
# 실제 응답을 원문 그대로 등록한 뒤
python main.py review --run holdout_01
# 별도 fixture 제어 흐름만 확인하려면
python main.py fixtures
```
`python main.py`를 파일의 절대경로로 실행해도 데이터·출력은 이 폴더 기준입니다.

## 산출물
`outputs/holdout_01/`의 최종 실제 관찰·요약. 예상 결과는 `expected/EXPECTED.md`와 대조합니다.

## 한 문장 설명
이 코드가 해결하는 문제와 아직 확인하지 못한 것을 구분해 설명하세요.
실행 성공·샘플 통과만으로 실제 모델 답변 품질이 좋아졌다고 주장하지 않습니다.

## 실제 응답 입력 — 별도 가이드
`../../docs/MANUAL_RUN_GUIDE.md`를 열어 원문을 등록합니다. 새 대화에서 A/B를 각각 실행합니다.
`meta.json`에 completed만 적거나 raw.txt를 임의로 생성하지 말고 제공 `record_manual.py`를 사용합니다.
`responses/<slot>/human_review.json`의 null을 실제 판단 후 true/false로 바꾸고 reviewer·note를 남깁니다.
모델 실행이 불가능하면 not_run과 이유를 유지하고 fixture 검사는 별도로 수행합니다.
source_mode=fixture는 checker 테스트용입니다. 실제 Prompt 성능 비교로 합산하지 않습니다.
초기 미실행 시 각 버전 N은 3(반복 수준은 6), attempted=0, pass rate=null, 사람평가 rated=0입니다.
그 상태를 0% 품질이나 완료 성적으로 발표하지 않습니다.

## 05의 고정 입력을 가져오기
```powershell
python main.py prepare --run holdout_01 --bundle ../05_ab_evaluation/outputs/dev_01/frozen_bundle.json
```
05가 미완성이면 --bundle 없이 제공 시작점을 사용하고 그 사실을 기록하세요.
H를 본 뒤 A/B를 수정하려면 새 버전으로 구분합니다. 같은 H를 새 독립 확인처럼 재사용하지 않습니다.
마지막은 긴 보고서가 아니라 입력 버전·첫 응답표·근거 메모·실패 처리 한 건으로 설명하면 됩니다.
