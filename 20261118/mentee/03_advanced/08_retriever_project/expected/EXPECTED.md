# 실습 08 · 검증할 결과

질문 → (query Embedding) → Top-k → 지식 id/title/content/category/source_version/distance 후보 반환. 여기서는 GPT 답변을 생성하지 않습니다.

실습 난이도: 03_advanced / TODO 6개

- `python main.py --mode fixture`는 로컬 모의 검증이며 E5/DB 실측이 아닙니다.
- `python main.py --mode live`의 실제 성공은 설치·DB·모델 다운로드가 준비된 Windows PC에서만 확인할 수 있습니다.
- 오류 또는 미실행은 성공·빈 결과·비용 0으로 임의 변환하지 않습니다.
- JSON 출력은 `outputs/exercise_08.json`에 저장됩니다.
