# Day22 · 2026-11-17 · LLM API 클라이언트 실습

**mentee: TODO를 완성하는 수강생용**

16일에 만든 Prompt·Context·출력 검증을 유지하고 응답 수집을 실제 API 호출로 바꿉니다. 새 웹서버·DB·RAG·Agent는 만들지 않습니다.

먼저 [실행 준비](docs/SETUP.md)를 읽고 `01_basic`·`02_intermediate`·`03_advanced` 중 하나를 선택합니다. [명령 모음](docs/COMMANDS.md), [오류 해결](docs/TROUBLESHOOTING.md), [교안과의 대응](docs/PPT_MAP.md)을 함께 사용합니다.

| 수준 | TODO | 학습 범위 |
|---|---:|---|
| [기본필수](01_basic/README.md) |26|변수·자료구조·호출 골격에서 핵심완성|
| [응용](02_intermediate/README.md)|38|조건·비교·오류·검증을조금더직접작성|
| [심화](03_advanced/README.md)|50|필요한책임분리·경계테스트·재현성|

코드는UTF-8,파일·폴더명은ASCII입니다. 질문·응답은가상의수업자료만사용합니다. AI도구사용은가능하지만왜필요한코드인지설명할수있어야합니다.

**실제 실행은 `--source live --allow-paid`, 모의는 `--source simulated`입니다.** source를생략하면live지만과금확인이없으면전송하지않습니다. API키가자료에들어있지않습니다.

교시마다독립시작점이있습니다. `coursekit`은이전단계가미완성인학생을위한제공기반입니다. 각실습에서는자신이작성한함수를hooks/인자로전달하여실제로사용합니다. 공통helper를수정하는것이이번TODO의해결책은아닙니다.

**파일 선택:** 통합본의mentor는정답입니다. 학생에게는mentee만배포합니다. 미완성TODO가있으면실제요청전에중단합니다.

## 빠른 점검
`python tools/selfcheck.py`는 제공 공통 코드만 모의 검사합니다. 각 교시 TODO 완성 여부는 해당 `main.py`로 따로 확인하세요.
실제 호출은 `--source live --allow-paid`, 모의 연습은 `--source simulated`입니다. 모의 성공을 실제 인증 성공으로 기록하지 않습니다.
