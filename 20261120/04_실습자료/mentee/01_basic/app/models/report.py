"""ERD와 1:1 대응하는 10개 물리 테이블의 SQLAlchemy ORM 선언."""
from datetime import datetime, date
from sqlalchemy import (BigInteger, Integer, String, Text, Date, DateTime, ForeignKey,
                        Identity, CheckConstraint, UniqueConstraint, func)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from pgvector.sqlalchemy import VECTOR

class Base(DeclarativeBase):
    pass

class ReportCategory(Base):
    __tablename__='report_categories'
    category_id: Mapped[int] = mapped_column(Integer,primary_key=True)
    code: Mapped[str] = mapped_column(Text,unique=True,nullable=False)
    name: Mapped[str] = mapped_column(Text,nullable=False)
    description: Mapped[str | None] = mapped_column(Text)

class Report(Base):
    __tablename__='reports'
    report_id: Mapped[int] = mapped_column(BigInteger, Identity(),primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('report_categories.category_id',ondelete='RESTRICT'),nullable=False)
    overview: Mapped[str] = mapped_column(String(1000),nullable=False)
    index_status: Mapped[str] = mapped_column(String(20),default='pending',nullable=False)
    revision: Mapped[int] = mapped_column(Integer,default=1,nullable=False)

class ReportEmbedding(Base):
    __tablename__='report_embeddings'
    report_id: Mapped[int] = mapped_column(ForeignKey('reports.report_id',ondelete='CASCADE'),primary_key=True)
    embedding: Mapped[list[float]] = mapped_column(VECTOR(384),nullable=False)
    model_name: Mapped[str] = mapped_column(Text,nullable=False)
    overview_hash: Mapped[str] = mapped_column(String(64),nullable=False)
    indexed_revision: Mapped[int] = mapped_column(Integer,nullable=False)
    indexed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(),nullable=False)

# 공통 필드를 종류별로 실제 보유한다는 요구사항에 맞춰 6개 상세 엔터티에 같은 Mixin 사용.
class DetailMixin:
    title: Mapped[str] = mapped_column(String(200),nullable=False)
    content: Mapped[str] = mapped_column(Text,nullable=False)
    author: Mapped[str] = mapped_column(String(100),nullable=False)
    create_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    update_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(),nullable=False)

class ExperimentReport(DetailMixin,Base):
    __tablename__='experiment_reports'
    report_id: Mapped[int] = mapped_column(ForeignKey('reports.report_id',ondelete='CASCADE'),primary_key=True)
    experiment_date: Mapped[date] = mapped_column(Date,nullable=False)
    hypothesis: Mapped[str] = mapped_column(Text,nullable=False)
    result_summary: Mapped[str] = mapped_column(Text,nullable=False)

class DailyWorkReport(DetailMixin,Base):
    __tablename__='daily_work_reports'
    report_id: Mapped[int] = mapped_column(ForeignKey('reports.report_id',ondelete='CASCADE'),primary_key=True)
    work_date: Mapped[date] = mapped_column(Date,nullable=False)
    progress: Mapped[str] = mapped_column(Text,nullable=False)
    blockers: Mapped[str] = mapped_column(Text,default='',nullable=False)

class ResearchPlan(DetailMixin,Base):
    __tablename__='research_plans'
    report_id: Mapped[int] = mapped_column(ForeignKey('reports.report_id',ondelete='CASCADE'),primary_key=True)
    research_goal: Mapped[str] = mapped_column(Text,nullable=False)
    methodology: Mapped[str] = mapped_column(Text,nullable=False)
    target_date: Mapped[date] = mapped_column(Date,nullable=False)

class DataProcessingReport(DetailMixin,Base):
    __tablename__='data_processing_reports'
    report_id: Mapped[int] = mapped_column(ForeignKey('reports.report_id',ondelete='CASCADE'),primary_key=True)
    dataset_name: Mapped[str] = mapped_column(Text,nullable=False)
    processing_steps: Mapped[str] = mapped_column(Text,nullable=False)
    quality_notes: Mapped[str] = mapped_column(Text,default='',nullable=False)

class PromptReport(DetailMixin,Base):
    __tablename__='prompt_reports'
    report_id: Mapped[int] = mapped_column(ForeignKey('reports.report_id',ondelete='CASCADE'),primary_key=True)
    purpose: Mapped[str] = mapped_column(Text,nullable=False)
    active_version_no: Mapped[int] = mapped_column(Integer,default=1,nullable=False)

class MeetingMinute(DetailMixin,Base):
    __tablename__='meeting_minutes'
    report_id: Mapped[int] = mapped_column(ForeignKey('reports.report_id',ondelete='CASCADE'),primary_key=True)
    meeting_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=False)
    attendees: Mapped[str] = mapped_column(Text,nullable=False)
    decisions: Mapped[str] = mapped_column(Text,nullable=False)

class PromptVersion(Base):
    __tablename__='prompt_versions'
    __table_args__=(UniqueConstraint('report_id','version_no',name='uq_prompt_versions_report_no'),)
    prompt_version_id: Mapped[int] = mapped_column(BigInteger,Identity(),primary_key=True)
    report_id: Mapped[int] = mapped_column(ForeignKey('prompt_reports.report_id',ondelete='CASCADE'),nullable=False)
    version_no: Mapped[int] = mapped_column(Integer,nullable=False)
    prompt_text: Mapped[str] = mapped_column(Text,nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(),nullable=False)

# 추가 테이블은 만들지 않는다. 보고서 종류마다 Detail Class만 매핑한다.
DETAIL_MODELS={
 'EXPERIMENT':ExperimentReport,'DAILY_WORK':DailyWorkReport,
 'RESEARCH_PLAN':ResearchPlan,'DATA_PROCESSING':DataProcessingReport,
 'PROMPT':PromptReport,'MEETING':MeetingMinute,
}
DETAIL_FIELDS={
 'EXPERIMENT':('experiment_date','hypothesis','result_summary'),
 'DAILY_WORK':('work_date','progress','blockers'),
 'RESEARCH_PLAN':('research_goal','methodology','target_date'),
 'DATA_PROCESSING':('dataset_name','processing_steps','quality_notes'),
 'PROMPT':('purpose','active_version_no'),
 'MEETING':('meeting_at','attendees','decisions'),
}
