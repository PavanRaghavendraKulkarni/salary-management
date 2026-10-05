from collections.abc import AsyncIterator, Callable
from contextlib import AbstractAsyncContextManager, asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.engine import Engine

from app.config.database import build_engine, build_session_factory, create_tables
from app.config.settings import Settings, get_settings
from app.constants.api_constants import API_TITLE, API_V1_PREFIX, API_VERSION
from app.controllers import (
    employee_controller,
    health_controller,
    insight_controller,
    meta_controller,
)
from app.controllers.frontend_controller import build_frontend_router
from app.exceptions.exception_handlers import register_exception_handlers


def build_lifespan(engine: Engine) -> Callable[[FastAPI], AbstractAsyncContextManager[None]]:
    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        """Create missing tables at start-up so the API works before the seed has run."""
        create_tables(engine)
        yield
        engine.dispose()

    return lifespan


def create_app(settings: Settings | None = None) -> FastAPI:
    """Build the app in a factory so tests get a fresh instance with their own settings.

    Each app owns its engine, so requests always use the database its settings name.
    """
    settings = settings or get_settings()
    engine = build_engine(settings.database_url)
    application = FastAPI(title=API_TITLE, version=API_VERSION, lifespan=build_lifespan(engine))
    application.state.session_factory = build_session_factory(engine)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    register_exception_handlers(application)
    application.include_router(health_controller.router, prefix=API_V1_PREFIX)
    application.include_router(employee_controller.router, prefix=API_V1_PREFIX)
    application.include_router(meta_controller.router, prefix=API_V1_PREFIX)
    application.include_router(insight_controller.router, prefix=API_V1_PREFIX)
    if settings.frontend_dist_dir and settings.frontend_dist_dir.is_dir():
        application.include_router(build_frontend_router(settings.frontend_dist_dir))
    return application


app = create_app()
