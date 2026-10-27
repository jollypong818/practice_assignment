# 실패·경계 입력
공통100건과 별도인 작은 입력입니다. 모델을 다시 학습하려는 자료가 아닙니다.
missing_priority: 필수 열 누락. forbidden_status: 금지 열 추가. infinite_numeric/negative_numeric: 수치 계약 위반.
duplicate_id: ID 중복. empty_input: 빈 행. all_numeric_missing_new: 새 입력의 수치 결측(학습 대표값으로 처리).
overlap_manifest: 분할표 중복 검사용. 원본을 직접 덮어쓰지 말고 임시 폴더에 복사해 테스트합니다.
실패 케이스의 ValueError는 기대 동작입니다. 무조건 예외를 숨기거나 결측을0으로 채우지 않습니다.
