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


def main():
    with get_session_factory()() as db:
        records=db.scalars(select(Report).order_by(Report.report_id)).all()
        values=[(r.report_id,r.overview,r.revision,r.index_status) for r in records]
        db.rollback()
    print(f'대상 보고서: {len(values)}개 / model={settings.embedding_model}')
    if not values:raise RuntimeError('먼저 sql/seed.sql을 실행하세요.')
    # 동일 model의 동일 Overview를 재실행해도 보고서당 Vector 1건 유지.
    for start in range(0,len(values),16):
        batch=values[start:start+16]
        vectors=emb.encode([row[1] for row in batch],kind='passage')
        with get_session_factory()() as db:
            with db.begin():
                for (rid,overview,rev,oldstatus),vector in zip(batch,vectors):
                    report=db.scalar(select(Report).where(Report.report_id==rid).with_for_update())
                    if report is None:continue
                    if report.revision!=rev or report.overview!=overview:
                        # 동시 변경이 있다면 잘못된 벡터를 덮어쓰지 않고 다음 배치/재실행 때 처리.
                        print(f'SKIP 변경된 보고서 {rid}');continue
                    target=db.get(ReportEmbedding,rid)
                    if target is None:target=ReportEmbedding(report_id=rid);db.add(target)
                    target.embedding=vector
                    target.model_name=settings.embedding_model
                    target.overview_hash=emb.overview_hash(overview)
                    target.indexed_revision=rev
                    target.indexed_at=datetime.now(timezone.utc)
                    report.index_status='ready'
        print(f'완료: {min(start+len(batch),len(values))}/{len(values)}')
    with get_session_factory()() as db:
        count=db.query(ReportEmbedding).count()
        ready=db.query(Report).filter(Report.index_status=='ready').count()
    print(f'검증: vectors={count}, ready={ready}; seed 초기 상태라면 각각 180이어야 합니다.')

if __name__=='__main__':main()
