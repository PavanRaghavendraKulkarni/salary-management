from collections.abc import Iterator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.config.settings import Settings
from app.dependencies.providers import get_session
from app.main import create_app
from app.models.base_model import Base

IN_MEMORY_DATABASE_URL = "sqlite://"


@pytest.fixture
def engine() -> Iterator[Engine]:
    test_engine = create_engine(
        IN_MEMORY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(test_engine)
    yield test_engine
    test_engine.dispose()


@pytest.fixture
def session(engine: Engine) -> Iterator[Session]:
    session_factory = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    with session_factory() as test_session:
        yield test_session


@pytest.fixture
def app(session: Session) -> FastAPI:
    application = create_app(Settings(frontend_dist_dir=None))
    application.dependency_overrides[get_session] = lambda: session
    return application


@pytest.fixture
def client(app: FastAPI) -> Iterator[TestClient]:
    with TestClient(app) as test_client:
        yield test_client
