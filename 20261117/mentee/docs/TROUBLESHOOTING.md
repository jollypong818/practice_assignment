# 흔한 문제와 확인 순서

| 증상 | 먼저 확인 | 피해야 할 대응 |
|---|---|---|
| 미완성 TODO 메시지 | 주석의 요구사항→빈값완성→해당raise제거 | raise만지우고무작정유료실행 |
| ModuleNotFoundError | 같은Python에requirements설치,압축해제여부 | 전역Python과venv를혼용 |
| 키 미설정 | role 폴더의.env, OS환경변수우선순위 | 키를코드/메신저에붙이기 |
| 401/403 | 프로젝트·키·권한·모델접근 | 다른사람키로우회·반복전송 |
| quota/billing429 | 잔액·지출한도확인 | 짧은sleep무한반복 |
| rate_limit429 | Retry-After·공유한도·시도번호 | 실제제한을재현하려고폭주 |
| timeout/연결중단 | 원래요청상태·과금여부미확인기록 | 무료실패라보고즉시재전송 |
| incomplete | max_output_tokens·모델설정과종료이유 | 부분JSON을성공으로고치기 |
| 출처오류 | 이번selected의ID와본문 | DB전체에ID가있다는이유로허용 |
| 키변경후캐시미스 | 모델·Prompt·문맥·scope·Schema·TTL | 오래된답을강제로반환 |
| review_hash불일치 | 리뷰뒤run.json수정여부 | 과거응답을수정후실측으로유지 |
| price unknown | 실제모델·서비스tier·usage상세·단가표 | 값을0으로채우기 |
| 장부lock | 모든프로세스가종료됐는지강사와확인 | 실행중다른터미널에서잠금삭제 |

10분이상환경문제로멈추면오류종류·실행위치·시도한내용만기록하고모의검사로이동합니다. 키나Authorization을포함하는전체로그는공유하지않습니다. 모의검사로넘어갔다면실제인증성공으로표시하지않습니다.
