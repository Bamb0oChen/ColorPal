"""SQLAlchemy 数据库引擎"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.config import settings

engine = create_engine(settings.DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    """FastAPI 依赖注入：获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """创建所有表（首次启动时调用）"""
    import app.models.user  # noqa
    import app.models.photo  # noqa
    import app.models.task   # noqa
    import app.models.collection  # noqa
    Base.metadata.create_all(bind=engine)
