# 05 · 개선용 질문 A/B 비교

PPT **37~45장**, 실습 약 **30분**. 수강생용: TODO가 있는 미완성 코드입니다.

## 목표
D01~D03으로 Prompt A/B를 실제 관찰합니다. 기본은 첫 응답 6개입니다.

## 편집할 파일
`analysis.py`
`# BEGIN/END` 블록의 골격을 완성하고 해당 NotImplementedError 줄을 지웁니다.
각 TODO는 요구·입력·완료 기준을 주석으로 함께 설명합니다.

| 블록 | 요구사항 |
|---|---|
| `D21-05-I01` | A의 규칙을 유지하면서 B에 근거 부족 규칙 한 개만 추가하세요. |
| `D21-05-I02` | 개선용 D01~D03 세 질문만 선택하세요. |
| `D21-05-I03` | 첫 응답만 골라 통과·미실행·미평가 개수를 기록하세요. |
| `D21-05-I04` | source_mode별 결과를 분리하고 fixture 지표를 실모델 품질로 해석하지 마세요. |
| `D21-05-I05` | 같은 조건을 한 번 더 관찰하도록 반복 수를 설정하세요. |

## 실행 위치
터미널에서 **이 README가 있는 폴더**로 이동합니다. `python`은 선택한 가상환경입니다.
```powershell
python main.py prepare --run dev_01
# 실제 응답을 원문 그대로 등록한 뒤
python main.py review --run dev_01
# 별도 fixture 제어 흐름만 확인하려면
python main.py fixtures
```
`python main.py`를 파일의 절대경로로 실행해도 데이터·출력은 이 폴더 기준입니다.

## 산출물
`outputs/dev_01/`의 Prompt·고정 bundle·raw·메타·첫 응답 표. 예상 결과는 `expected/EXPECTED.md`와 대조합니다.

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
