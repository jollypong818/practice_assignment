# 11월 18일 HTML → 코드/데이터 매핑

기준: `Day23_Embedding_pgvector_Interactive_20261118_80p(1).html` (80개 화면, 8개 교시).
원래 174장 PPT·FAQ 12건·MiniLM 예제는 사용하지 않습니다.

| HTML 실습 | 해당 폴더 | 구체적인 연결 |
|---|---|---|
| 실습01 `practice-1` | `01_knowledge` | 지식 101~109 원문, 101~103 보존, passage 입력/버전 |
| 실습02 `practice-2` | `02_similarity` | q=(1,0), A=(0.8,0.6), Dot·Cosine·L2 |
| 실습03 `practice-3` | `03_e5_embeddings` | `intfloat/multilingual-e5-small`, query/passage, (n,384) |
| 실습04 `practice-4` | `04_pgvector_setup` | Windows PG18.6, 공식 v0.8.7 빌드·현재 DB·Python 검증 |
| 실습05 `practice-5` | `05_topk_storage` | `day23_search_docs`, 9개 지식, Cosine <=> ASC, Metadata |
| 실습06 `practice-6` | `06_hnsw` | HNSW index, Exact, EXPLAIN, 필터·후보 누락 |
| 실습07 `practice-7` | `07_relevance` | 관련/부분/무관, 빈 결과와 DB 장애, 버전 차이 |
| 실습08 `practice-8` | `08_retriever_project` | 질문→Embedding→Top-k→지식 ID·원문·거리 (GPT 생성 없음) |

**원문 계약**: `common/data/knowledge_search_v2.json`은 HTML의 101~109 `id/title/content/category/source_version`과 동일합니다.
**모델 계약**: E5-small / 384 dimensions / `query: ` / `passage: ` + title + space + content / normalize=True.
**DB 계약**: 기존 PostgreSQL·기존 knowledge 테이블 보존, 별도 `day23_search_docs` 사용.

`--mode fixture`는 수학·흐름 모의 실행만 하며 PostgreSQL이나 E5 모델을 사용한 적이 없습니다.
`--mode live`만 실제 E5/DB에 접속합니다. 이 경로는 수업 PC에서 별도로 확인해야 합니다.
