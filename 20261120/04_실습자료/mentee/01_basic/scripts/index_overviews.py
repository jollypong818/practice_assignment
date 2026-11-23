"""실제 E5-small로 초기 개요 180건을 Vector(384)에 일괄 적재합니다."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from datetime import datetime,timezone
from sqlalchemy import select
from app.db.session import get_session_factory
from app.models.report import Report,ReportEmbedding
from app.integrations import embedding_client as emb
from app.core.config import settings


def index_overviews():
    """TODO B-10 · index_overviews() — mentor와 동일한 함수 계약을 완성하세요."""
    # TODO B-10: seed 적재 후 reports의 overview/revision을 읽어 실제 E5 passage 벡터를 batch
    # TODO B-10: 처리하세요. report_embeddings report_id PK를 기준으로 1행 유지,
    # TODO B-10: indexed_revision/overview_hash/ready를 갱신하고 180개를 확인하세요.
    # 입력·반환형과 예외·상태코드는 요구사항 명세서/API 계약을 참조합니다.
    # 정답 구현 후 아래 예외를 지우고 로직을 작성하세요.
    raise NotImplementedError("B-10 · index_overviews() TODO 미완성")

def main():
    """실행 진입점: 실제 적재 절차는 index_overviews()에서 수행합니다."""
    index_overviews()

if __name__=='__main__':main()
