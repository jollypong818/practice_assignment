# 제작 검수 환경과 버전

제작 검수일: 2026-11-20. 기본 실행 환경: Python 3.12, Linux. 배포 안내와 경로 처리는 Windows 11·VS Code·Git Bash를 기준으로 작성했습니다. Windows PC에서의 설치 실행과 실제 외부 연동은 별도 확인 범위입니다.

| 패키지 | 제작 환경에서 사용한 버전 |
|---|---|
| langchain-core | 1.8.4 |
| langchain-openai | 1.8.5 |
| openai | 3.57.0 |
| pydantic | 2.13.4 |
| fastapi | 0.141.1 |
| httpx | 0.28.1 |
| uvicorn | 0.52.1 |
| python-dotenv | 1.2.2 |
| numpy | 2.3.5 |
| psycopg / psycopg-binary | 3.3.9 |
| pgvector Python | 0.5.1 |
| pytest | 9.2.0 |

위 버전은 실제 검수 환경의 패키지 메타데이터에서 확인했습니다. 무조건 최신 버전이라는 의미는 아닙니다. LangChain의 provider 어댑터와 core를 서로 맞지 않는 버전으로 바꾸면 반환 형태가 달라질 수 있으므로 변경 후 로컬 검사를 다시 수행합니다.

실제 E5 모델 다운로드·임베딩, PostgreSQL 서버 접속/저장, 유료 LLM API 호출은 제작 환경에서 수행하지 않았습니다. 관련 코드는 모의 의존성과 입력·출력 계약으로 검사하고, 실측 성공 여부는 수업 PC에서 확인하도록 명시했습니다. 오프라인 Fixture는 검색 품질이나 LLM 성능 측정값이 아닙니다.

공식 자료:

- [LangChain Document](https://reference.langchain.com/python/langchain-core/documents/base/Document)
- [ChatPromptTemplate](https://reference.langchain.com/python/langchain-core/prompts/chat/ChatPromptTemplate)
- [ChatOpenAI Structured Output](https://reference.langchain.com/python/langchain-openai/chat_models/base/ChatOpenAI/with_structured_output)
- [E5-small 모델 카드](https://huggingface.co/intfloat/multilingual-e5-small)
- [Psycopg SQL parameter와 Identifier](https://www.psycopg.org/psycopg3/docs/api/sql.html)
- [FastAPI 테스트](https://fastapi.tiangolo.com/tutorial/testing/)
