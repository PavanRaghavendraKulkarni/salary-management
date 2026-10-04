from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import get_settings
from app.constants.api_constants import API_TITLE, API_V1_PREFIX, API_VERSION


def create_app() -> FastAPI:
    """Build the app in a factory so tests get a fresh instance with their own overrides."""
    settings = get_settings()
    application = FastAPI(title=API_TITLE, version=API_VERSION)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return application


app = create_app()
