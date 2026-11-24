# Day27 연습 데이터

- `corpus.json`: 24개 교육용 문서 청크. 실제 기업 규정이 아니며 모두 허구입니다.
- `questions.json`: 질문 8개와 대화 History.
- `gold_labels.json`: 평가용 정답 chunk ID. **검색이나 모델 입력에 전달하지 않습니다.**
- `fixture_rankings.json`: 오프라인 결과 비교용 **고정 순위**. 실제 E5 검색 결과로 간주하지 않습니다.
- `ready=false`, `is_current=false`, `access_level=staff` 문서는 일반 사용자 검색에서 제외합니다.
- 실제 DB에서는 citation_id가 DB에서 새로 생성됩니다. 정확한 비교 키는 `chunk_id`입니다.
