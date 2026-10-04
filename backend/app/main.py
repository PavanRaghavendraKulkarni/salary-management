from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import get_settings
from app.constants.api_constants import API_TITLE, API_V1_PREFIX, API_VERSION
from app.controllers import employee_controller, health_controller
from app.exceptions.exception_handlers import register_exception_handlers


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
    register_exception_handlers(application)
    application.include_router(health_controller.router, prefix=API_V1_PREFIX)
    application.include_router(employee_controller.router, prefix=API_V1_PREFIX)
    return application


app = create_app()
