# TODO 정답 대응표

|ID|파일|요구사항|
|---|---|---|
|D22-01-B01|`01_basic/01_first_call/main.py`|첫 요청의 model·instructions·input·출력 상한·store를 완성하세요.|
|D22-01-B02|`01_basic/01_first_call/main.py`|Responses API를 한 번 호출하고 반환값을 돌려주세요.|
|D22-01-B03|`01_basic/01_first_call/main.py`|키 없이 source·model·종료 상태·응답 ID를 요약하세요.|
|D22-02-B01|`01_basic/02_structured_output/main.py`|질문과 선택 지식만 user input으로 직렬화하세요.|
|D22-02-B02|`01_basic/02_structured_output/main.py`|공급자용 Schema를 요청의 text.format으로 연결하세요.|
|D22-02-B03|`01_basic/02_structured_output/main.py`|거절 콘텐츠와 미완료 상태를 먼저 구분하세요.|
|D22-02-B04|`01_basic/02_structured_output/main.py`|완료 응답에서도 빈 본문을 검사한 뒤 원문을 반환하세요.|
|D22-03-B01|`01_basic/03_streaming/main.py`|비어 있지 않은 첫 텍스트의 시간과 delta를 누적하세요.|
|D22-03-B02|`01_basic/03_streaming/main.py`|최종 이벤트의 Response를 보관하세요.|
|D22-03-B03|`01_basic/03_streaming/main.py`|실제 스트리밍을 요청하도록 선택값을 반환하세요.|
|D22-04-B01|`01_basic/04_errors_retry/main.py`|401·403은 중단하고, 429의 quota와 일시적 제한을 구분하세요.|
|D22-04-B02|`01_basic/04_errors_retry/main.py`|생성 최대2·생성별 전송최대2·전체 전송최대4를 설정하세요.|
|D22-04-B03|`01_basic/04_errors_retry/main.py`|제공된 대기 함수에 남은 예산을 전달하고 반환값을 유지하세요.|
|D22-05-B01|`01_basic/05_usage_cost/main.py`|사용량이 없으면 None, 있으면 입력·출력과부분 상세를 읽으세요.|
|D22-05-B02|`01_basic/05_usage_cost/main.py`|캐시를제외한 입력·캐시입력·출력 비용을 Decimal로 계산하세요.|
|D22-05-B03|`01_basic/05_usage_cost/main.py`|시도번호·실행출처·시간·사용량·비용을 같은 행에 남기세요.|
|D22-06-B01|`01_basic/06_response_cache/main.py`|질문뿐 아니라 모델·전체요청·Schema·검증버전·scope로 캐시키를 만드세요.|
|D22-06-B02|`01_basic/06_response_cache/main.py`|현재문맥·실행출처·scope와함께 제공된 안전한캐시검사를 호출하세요.|
|D22-06-B03|`01_basic/06_response_cache/main.py`|같은ID의본문변경이캐시키를바꾸는지확인하세요.|
|D22-07-B01|`01_basic/07_model_routing/main.py`|fast·quality만허용하고실제모델과선택이유를반환하세요.|
|D22-07-B02|`01_basic/07_model_routing/main.py`|어떤모델이든동일한결과필드로비교하세요.|
|D22-07-B03|`01_basic/07_model_routing/main.py`|명시적비교에서만fast·quality를한번씩선택하세요.|
|D22-08-B01|`01_basic/08_daily_project/main.py`|최종연동확인질문H01·H02·H03을같은순서로지정하세요.|
|D22-08-B02|`01_basic/08_daily_project/main.py`|각실행의상태·사용량·시간을표행으로연결하세요.|
|D22-08-B03|`01_basic/08_daily_project/main.py`|실제·모의·캐시·미실행을분리하여요약하세요.|
|D22-08-B04|`01_basic/08_daily_project/main.py`|자동검사후사람미평가None을유지하고전송상한을확인하세요.|
|D22-01-I01|`02_intermediate/01_first_call/logic.py`|첫 요청의 model·instructions·input·출력 상한·store를 완성하세요.|
|D22-01-I02|`02_intermediate/01_first_call/logic.py`|Responses API를 한 번 호출하고 반환값을 돌려주세요.|
|D22-01-I03|`02_intermediate/01_first_call/logic.py`|키 없이 source·model·종료 상태·응답 ID를 요약하세요.|
|D22-01-I04|`02_intermediate/01_first_call/logic.py`|키 미설정과 모델 접근 오류의 차이를 모의 비교표에 적으세요.|
|D22-02-I01|`02_intermediate/02_structured_output/logic.py`|질문과 선택 지식만 user input으로 직렬화하세요.|
|D22-02-I02|`02_intermediate/02_structured_output/logic.py`|공급자용 Schema를 요청의 text.format으로 연결하세요.|
|D22-02-I03|`02_intermediate/02_structured_output/logic.py`|거절 콘텐츠와 미완료 상태를 먼저 구분하세요.|
|D22-02-I04|`02_intermediate/02_structured_output/logic.py`|완료 응답에서도 빈 본문을 검사한 뒤 원문을 반환하세요.|
|D22-02-I05|`02_intermediate/02_structured_output/logic.py`|정상 질문 D02와 정보 부족 질문 D03의 순서를 지정하세요.|
|D22-03-I01|`02_intermediate/03_streaming/logic.py`|비어 있지 않은 첫 텍스트의 시간과 delta를 누적하세요.|
|D22-03-I02|`02_intermediate/03_streaming/logic.py`|최종 이벤트의 Response를 보관하세요.|
|D22-03-I03|`02_intermediate/03_streaming/logic.py`|실제 스트리밍을 요청하도록 선택값을 반환하세요.|
|D22-03-I04|`02_intermediate/03_streaming/logic.py`|동일 입력의 비스트리밍과 스트리밍 순서를 지정하세요.|
|D22-03-I05|`02_intermediate/03_streaming/logic.py`|첫 표시 시간과 전체 요청 시간을 분리해 요약하세요.|
|D22-04-I01|`02_intermediate/04_errors_retry/logic.py`|401·403은 중단하고, 429의 quota와 일시적 제한을 구분하세요.|
|D22-04-I02|`02_intermediate/04_errors_retry/logic.py`|생성 최대2·생성별 전송최대2·전체 전송최대4를 설정하세요.|
|D22-04-I03|`02_intermediate/04_errors_retry/logic.py`|헤더 최소 대기와 지수 대기 중 큰 값을 계산하세요.|
|D22-04-I04|`02_intermediate/04_errors_retry/logic.py`|대기시간이 남은 작업 예산 이상이면 None으로 중단하세요.|
|D22-04-I05|`02_intermediate/04_errors_retry/logic.py`|각 시도의 번호가 누락되지 않고 총4이하인지 확인하세요.|
|D22-05-I01|`02_intermediate/05_usage_cost/logic.py`|사용량이 없으면 None, 있으면 입력·출력과부분 상세를 읽으세요.|
|D22-05-I02|`02_intermediate/05_usage_cost/logic.py`|캐시를제외한 입력·캐시입력·출력 비용을 Decimal로 계산하세요.|
|D22-05-I03|`02_intermediate/05_usage_cost/logic.py`|시도번호·실행출처·시간·사용량·비용을 같은 행에 남기세요.|
|D22-05-I04|`02_intermediate/05_usage_cost/logic.py`|usage 없음과 모델 단가 미등록에서 비용이None인지 검사하세요.|
|D22-05-I05|`02_intermediate/05_usage_cost/logic.py`|전체비용미확인을보존하는 합산함수를 연결하세요.|
|D22-06-I01|`02_intermediate/06_response_cache/logic.py`|질문뿐 아니라 모델·전체요청·Schema·검증버전·scope로 캐시키를 만드세요.|
|D22-06-I02|`02_intermediate/06_response_cache/logic.py`|현재문맥·실행출처·scope와함께 제공된 안전한캐시검사를 호출하세요.|
|D22-06-I03|`02_intermediate/06_response_cache/logic.py`|같은ID의본문변경이캐시키를바꾸는지확인하세요.|
|D22-06-I04|`02_intermediate/06_response_cache/logic.py`|모델선택만바뀌어도다른키가되는지확인하세요.|
|D22-06-I05|`02_intermediate/06_response_cache/logic.py`|만료시간에같거나지난캐시가재사용되지않는지검사하세요.|
|D22-07-I01|`02_intermediate/07_model_routing/logic.py`|fast·quality만허용하고실제모델과선택이유를반환하세요.|
|D22-07-I02|`02_intermediate/07_model_routing/logic.py`|어떤모델이든동일한결과필드로비교하세요.|
|D22-07-I03|`02_intermediate/07_model_routing/logic.py`|명시적비교에서만fast·quality를한번씩선택하세요.|
|D22-07-I04|`02_intermediate/07_model_routing/logic.py`|잘못된mode가호출전에오류인지모의검사하세요.|
|D22-08-I01|`02_intermediate/08_daily_project/logic.py`|최종연동확인질문H01·H02·H03을같은순서로지정하세요.|
|D22-08-I02|`02_intermediate/08_daily_project/logic.py`|각실행의상태·사용량·시간을표행으로연결하세요.|
|D22-08-I03|`02_intermediate/08_daily_project/logic.py`|실제·모의·캐시·미실행을분리하여요약하세요.|
|D22-08-I04|`02_intermediate/08_daily_project/logic.py`|자동검사후사람미평가None을유지하고전송상한을확인하세요.|
|D22-08-I05|`02_intermediate/08_daily_project/logic.py`|최초시도와마지막시도의상태를분리하여보존하세요.|
|D22-01-A01|`03_advanced/01_first_call/app/client.py`|첫 요청의 model·instructions·input·출력 상한·store를 완성하세요.|
|D22-01-A02|`03_advanced/01_first_call/app/client.py`|Responses API를 한 번 호출하고 반환값을 돌려주세요.|
|D22-01-A03|`03_advanced/01_first_call/app/client.py`|키 없이 source·model·종료 상태·응답 ID를 요약하세요.|
|D22-01-A04|`03_advanced/01_first_call/app/client.py`|키 미설정과 모델 접근 오류의 차이를 모의 비교표에 적으세요.|
|D22-01-A05|`03_advanced/01_first_call/app/client.py`|기록할 필드를 허용 목록으로 제한하는 assertion을 완성하세요.|
|D22-02-A01|`03_advanced/02_structured_output/app/contracts.py`|질문과 선택 지식만 user input으로 직렬화하세요.|
|D22-02-A02|`03_advanced/02_structured_output/app/contracts.py`|공급자용 Schema를 요청의 text.format으로 연결하세요.|
|D22-02-A03|`03_advanced/02_structured_output/app/contracts.py`|거절 콘텐츠와 미완료 상태를 먼저 구분하세요.|
|D22-02-A04|`03_advanced/02_structured_output/app/contracts.py`|완료 응답에서도 빈 본문을 검사한 뒤 원문을 반환하세요.|
|D22-02-A05|`03_advanced/02_structured_output/app/contracts.py`|정상 질문 D02와 정보 부족 질문 D03의 순서를 지정하세요.|
|D22-02-A06|`03_advanced/02_structured_output/app/contracts.py`|Wire Schema의 네 필드 필수·추가 필드 금지를 검사하세요.|
|D22-03-A01|`03_advanced/03_streaming/app/streaming.py`|비어 있지 않은 첫 텍스트의 시간과 delta를 누적하세요.|
|D22-03-A02|`03_advanced/03_streaming/app/streaming.py`|최종 이벤트의 Response를 보관하세요.|
|D22-03-A03|`03_advanced/03_streaming/app/streaming.py`|실제 스트리밍을 요청하도록 선택값을 반환하세요.|
|D22-03-A04|`03_advanced/03_streaming/app/streaming.py`|동일 입력의 비스트리밍과 스트리밍 순서를 지정하세요.|
|D22-03-A05|`03_advanced/03_streaming/app/streaming.py`|첫 표시 시간과 전체 요청 시간을 분리해 요약하세요.|
|D22-03-A06|`03_advanced/03_streaming/app/streaming.py`|완료 이벤트가 없으면 최종 Response가 없는지 모의 검사하세요.|
|D22-04-A01|`03_advanced/04_errors_retry/app/policy.py`|401·403은 중단하고, 429의 quota와 일시적 제한을 구분하세요.|
|D22-04-A02|`03_advanced/04_errors_retry/app/policy.py`|생성 최대2·생성별 전송최대2·전체 전송최대4를 설정하세요.|
|D22-04-A03|`03_advanced/04_errors_retry/app/policy.py`|헤더 최소 대기와 지수 대기 중 큰 값을 계산하세요.|
|D22-04-A04|`03_advanced/04_errors_retry/app/policy.py`|대기시간이 남은 작업 예산 이상이면 None으로 중단하세요.|
|D22-04-A05|`03_advanced/04_errors_retry/app/policy.py`|각 시도의 번호가 누락되지 않고 총4이하인지 확인하세요.|
|D22-04-A06|`03_advanced/04_errors_retry/app/policy.py`|timeout·거절·할당량에서 전송이1번으로 끝났는지 확인하세요.|
|D22-04-A07|`03_advanced/04_errors_retry/app/policy.py`|통신2종과 형식수정이 공유한4회 기록의 generation 번호를 확인하세요.|
|D22-05-A01|`03_advanced/05_usage_cost/app/metrics.py`|사용량이 없으면 None, 있으면 입력·출력과부분 상세를 읽으세요.|
|D22-05-A02|`03_advanced/05_usage_cost/app/metrics.py`|캐시를제외한 입력·캐시입력·출력 비용을 Decimal로 계산하세요.|
|D22-05-A03|`03_advanced/05_usage_cost/app/metrics.py`|시도번호·실행출처·시간·사용량·비용을 같은 행에 남기세요.|
|D22-05-A04|`03_advanced/05_usage_cost/app/metrics.py`|usage 없음과 모델 단가 미등록에서 비용이None인지 검사하세요.|
|D22-05-A05|`03_advanced/05_usage_cost/app/metrics.py`|전체비용미확인을보존하는 합산함수를 연결하세요.|
|D22-05-A06|`03_advanced/05_usage_cost/app/metrics.py`|첫 실패비용이unknown이면 마지막성공만으로총비용을확정하지마세요.|
|D22-06-A01|`03_advanced/06_response_cache/app/cache.py`|질문뿐 아니라 모델·전체요청·Schema·검증버전·scope로 캐시키를 만드세요.|
|D22-06-A02|`03_advanced/06_response_cache/app/cache.py`|현재문맥·실행출처·scope와함께 제공된 안전한캐시검사를 호출하세요.|
|D22-06-A03|`03_advanced/06_response_cache/app/cache.py`|같은ID의본문변경이캐시키를바꾸는지확인하세요.|
|D22-06-A04|`03_advanced/06_response_cache/app/cache.py`|모델선택만바뀌어도다른키가되는지확인하세요.|
|D22-06-A05|`03_advanced/06_response_cache/app/cache.py`|만료시간에같거나지난캐시가재사용되지않는지검사하세요.|
|D22-06-A06|`03_advanced/06_response_cache/app/cache.py`|권한범위와검증버전의변경이키를바꾸는지검사하세요.|
|D22-06-A07|`03_advanced/06_response_cache/app/cache.py`|캐시히트는새전송0·현재사용량0·원래실행ID를남기는지확인하세요.|
|D22-07-A01|`03_advanced/07_model_routing/app/routing.py`|fast·quality만허용하고실제모델과선택이유를반환하세요.|
|D22-07-A02|`03_advanced/07_model_routing/app/routing.py`|어떤모델이든동일한결과필드로비교하세요.|
|D22-07-A03|`03_advanced/07_model_routing/app/routing.py`|명시적비교에서만fast·quality를한번씩선택하세요.|
|D22-07-A04|`03_advanced/07_model_routing/app/routing.py`|잘못된mode가호출전에오류인지모의검사하세요.|
|D22-07-A05|`03_advanced/07_model_routing/app/routing.py`|quality가미설정이면다른모델로자동대체하지않는지확인하세요.|
|D22-07-A06|`03_advanced/07_model_routing/app/routing.py`|자동검증결과를사람의근거승인으로만들지않는지확인하세요.|
|D22-08-A01|`03_advanced/08_daily_project/app/project.py`|최종연동확인질문H01·H02·H03을같은순서로지정하세요.|
|D22-08-A02|`03_advanced/08_daily_project/app/project.py`|각실행의상태·사용량·시간을표행으로연결하세요.|
|D22-08-A03|`03_advanced/08_daily_project/app/project.py`|실제·모의·캐시·미실행을분리하여요약하세요.|
|D22-08-A04|`03_advanced/08_daily_project/app/project.py`|자동검사후사람미평가None을유지하고전송상한을확인하세요.|
|D22-08-A05|`03_advanced/08_daily_project/app/project.py`|최초시도와마지막시도의상태를분리하여보존하세요.|
|D22-08-A06|`03_advanced/08_daily_project/app/project.py`|일일프로젝트에도교안과같은공유예산을반환하세요.|
|D22-08-A07|`03_advanced/08_daily_project/app/project.py`|미수신usage를0으로바꾸지않는지최종검사하세요.|
