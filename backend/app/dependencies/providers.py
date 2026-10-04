from collections.abc import Iterator

from sqlalchemy.orm import Session

from app.config.database import SessionFactory


def get_session() -> Iterator[Session]:
    with SessionFactory() as session:
        yield session
