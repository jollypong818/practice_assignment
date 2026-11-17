# 자료 근거와 구현 확인 범위

## 기준자료
- 사용자 확정 `Day22_Lecture_20261117.pptx` 86장. 이 패키지를 만들면서 PPT는 수정하지 않았습니다.
- Day21 실습 통합본의 `mentor/coursekit/contracts.py`, `knowledge_v1.json`, `dev_v1.json`, `holdout_v1.json`을 재사용했습니다.

## 외부 확인 — 2026-11-12 공식 문서
- https://developers.openai.com/api/reference/python — Responses·오류·timeout·SDK재시도설정
- https://developers.openai.com/api/docs/guides/structured-outputs — 공급자Schema·거절·불완전처리
- https://developers.openai.com/api/docs/guides/streaming-responses — delta·완료이벤트
- https://developers.openai.com/api/docs/guides/error-codes — 인증·권한·할당량오류분류
- https://developers.openai.com/api/docs/guides/rate-limits — 제한·대기·재시도
- https://developers.openai.com/api/docs/guides/prompt-caching — 입력계산재사용과응답캐시구분
- https://developers.openai.com/api/docs/models/gpt-5.4-mini — 수업후보 snapshot·지원기능·단가
- https://developers.openai.com/api/docs/models/gpt-5.4 — 비교후보 snapshot·지원기능·단가

사용 모델·가격은 PPT 후보와 일치하는지 확인했습니다. 계정권한·잔액·수업당일의지원상태는실제사전검수대상입니다. SDK설치와실제서버호출을성공했다고표시하지않습니다.

## 제작 편의와 수업정책
20회개인장부·명시적과금확인·순차실행·검토후캐시는수업용운영정책입니다. 모든현업서비스의보편적규칙이라는뜻이아닙니다. 재시도예산은교안34~35·77장을따릅니다.
