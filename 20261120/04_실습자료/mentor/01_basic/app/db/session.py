"""SQLAlchemy DB 연결과 세션 수명 관리. HTTP 요청당 세션을 하나 사용합니다."""
from functools import lru_cache
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.services.errors import DomainError

@lru_cache(maxsize=1)
def get_engine():
    if not settings.database_url or 'CHANGE_ME' in settings.database_url:
        raise DomainError(503,'DB_UNAVAILABLE','DATABASE_URL에 PostgreSQL 접속 정보를 설정하세요 (.env).')
    return create_engine(settings.database_url, pool_pre_ping=True, pool_size=5, max_overflow=5)

@lru_cache(maxsize=1)
def get_session_factory():
    return sessionmaker(bind=get_engine(), expire_on_commit=False, autoflush=False)

def get_db():
    # Router에서 Depends(get_db)로 사용. 서비스에서 commit 또는 rollback합니다.
    with get_session_factory()() as db:
        yield db
