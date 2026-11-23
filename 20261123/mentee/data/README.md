# 강의와 같은 세 문서

가상 교육센터의 예제이며 실제 기관의 규정이 아닙니다. 원문 내용은 Day26 HTML과 같습니다.

- `lecture_hits.json`: 교육용 Hit. citation_id 201/202/203은 고정 설명용 ID입니다.
- `raw/`: 사람이 숫자·조건·출처를 대조할 문서. locator의 # 뒤는 문서 내부 위치입니다.
- `questions.json`: 강의의 다섯 질문과 기대 판단. 모델의 실측 응답이나 검색 순위가 아닙니다.
- 실제 DB 준비 시 이 본문을 실제 E5로 임베딩하고 DB가 새 정수 ID를 부여합니다.
- live ID를 201/202/203으로 바꾸지 마세요. 같은 doc_id/source_version/source_locator로 원문을 찾습니다.

이 데이터는 이미 정리된 짧은 청크입니다. 오늘은 Parsing/Chunking을 다시 구현하지 않고 RAG 연결을 학습합니다.
