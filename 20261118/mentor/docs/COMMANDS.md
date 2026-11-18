# Day23 · 실행 순서 (Windows VS Code · 기존 환경)

모든 명령은 각 실습 폴더에서 `python main.py --mode fixture`로 시작해도 됩니다.
실제 DB 연결은 실습별 `.env.example` → `.env` 복사 후 `--mode live`를 사용합니다.

## 1~8교시별 폴더 명령 (배포 폴더가 현재 위치)

### 01_basic (기본필수)
```bash
python 01_basic/01_knowledge/main.py --mode fixture
python 01_basic/02_similarity/main.py --mode fixture
python 01_basic/03_e5_embeddings/main.py --mode fixture
python 01_basic/04_pgvector_setup/main.py --mode fixture
python 01_basic/05_topk_storage/main.py --mode fixture
python 01_basic/06_hnsw/main.py --mode fixture
python 01_basic/07_relevance/main.py --mode fixture
python 01_basic/08_retriever_project/main.py --mode fixture
```

### 02_intermediate (응용)
```bash
python 02_intermediate/01_knowledge/main.py --mode fixture
python 02_intermediate/02_similarity/main.py --mode fixture
python 02_intermediate/03_e5_embeddings/main.py --mode fixture
python 02_intermediate/04_pgvector_setup/main.py --mode fixture
python 02_intermediate/05_topk_storage/main.py --mode fixture
python 02_intermediate/06_hnsw/main.py --mode fixture
python 02_intermediate/07_relevance/main.py --mode fixture
python 02_intermediate/08_retriever_project/main.py --mode fixture
```

### 03_advanced (심화)
```bash
python 03_advanced/01_knowledge/main.py --mode fixture
python 03_advanced/02_similarity/main.py --mode fixture
python 03_advanced/03_e5_embeddings/main.py --mode fixture
python 03_advanced/04_pgvector_setup/main.py --mode fixture
python 03_advanced/05_topk_storage/main.py --mode fixture
python 03_advanced/06_hnsw/main.py --mode fixture
python 03_advanced/07_relevance/main.py --mode fixture
python 03_advanced/08_retriever_project/main.py --mode fixture
```

## 실제 E5 / PostgreSQL 연동 (예: 기본필수)
아래 명령은 Windows pgvector 0.8.7 설치 + 정확한 DB 확장 활성화 후 실행합니다.
04~08 각 폴더의 `.env.example`을 `.env`로 복사하고 실제 pgAdmin DB 정보로 수정해야 합니다.
```bash
python 01_basic/03_e5_embeddings/main.py --mode live
python 01_basic/04_pgvector_setup/main.py --mode live
python 01_basic/05_topk_storage/main.py --mode live
python 01_basic/06_hnsw/main.py --mode live
python 01_basic/06_hnsw/main.py --mode live --create-index # 명시적으로 인덱스를 만들 때만
python 01_basic/07_relevance/main.py --mode live
python 01_basic/08_retriever_project/main.py --mode live
python 02_intermediate/08_retriever_project/main.py --mode live --k 3 --category development --question "서버를 어디서 켜나요?"
```

주의: 실습 05가 실제 E5 벡터 9건을 DB에 저장한 뒤 06~08을 실행합니다. 다른 수준의 05에서 같은 스냅샷을 저장했다면 재사용 가능하나 DB/모델/버전을 확인하세요.
실습 04와 06은 수동 pgAdmin 확인 과정도 포함됩니다. SQL 단계의 성공을 fixture 실행으로 판정하지 않습니다.
