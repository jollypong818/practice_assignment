# 고정 입력과 검증용 fixture
`knowledge_v1.json`은 PPT 6장과 동일한 101~103 스냅샷입니다. 실제 DB ID를 재번호 부여한 데이터가 아닙니다.
`dev_v1.json`은 D01~D03 개선용, `holdout_v1.json`은 H01~H03 최종 확인용입니다(PPT 38장).
H 질문은 PPT에 공개되어 있습니다. 숨겨진 벤치마크라고 주장하지 않습니다. D로 개선하고 A/B를 고정한 다음 H를 실행합니다.
`expected_behavior`는 사람 평가용 안내이며 Prompt에 삽입하지 않습니다.
`decomposition_cards.json`의 required/supported/conflicts는 교사가 작성한 학습용 판단 카드입니다. 프로그램이 자연어에서 사실성을 자동 판정한 결과가 아닙니다.
`validation_fixtures.json`의 모든 응답은 작성한 샘플입니다. 실제 ChatGPT 응답, Prompt A/B의 성능 증거가 아닙니다.
`duplicate_key`, `nonstandard_number`는 PPT 77장의 엄격 파서 확장 사례입니다. 기본필수는 제공 함수를 사용합니다.
입력 파일을 변경해 새 실험을 할 때는 버전도 변경합니다. 실행 중인 실험의 스냅샷은 변경하지 않습니다.
