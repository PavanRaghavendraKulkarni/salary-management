from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.models import Base

SQLITE_URL_PREFIX = "sqlite"


def build_engine(database_url: str) -> Engine:
    connect_args = (
        {"check_same_thread": False} if database_url.startswith(SQLITE_URL_PREFIX) else {}
    )
    return create_engine(database_url, connect_args=connect_args)


def build_session_factory(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def create_tables(target_engine: Engine) -> None:
    """Create missing tables; a migration tool is unnecessary while the schema is one table."""
    Base.metadata.create_all(target_engine)
