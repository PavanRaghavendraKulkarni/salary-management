from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.config.settings import get_settings

SQLITE_URL_PREFIX = "sqlite"


def build_engine(database_url: str) -> Engine:
    connect_args = (
        {"check_same_thread": False} if database_url.startswith(SQLITE_URL_PREFIX) else {}
    )
    return create_engine(database_url, connect_args=connect_args)


engine = build_engine(get_settings().database_url)
SessionFactory: sessionmaker[Session] = sessionmaker(
    bind=engine, autoflush=False, expire_on_commit=False
)
