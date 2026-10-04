from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse

from app.constants.api_constants import API_V1_PREFIX, FRONTEND_INDEX_FILE, FRONTEND_ROUTE_PATH
from app.exceptions.domain_exceptions import RouteNotFoundError

API_PATH_PREFIX = API_V1_PREFIX.lstrip("/")


def build_frontend_router(dist_dir: Path) -> APIRouter:
    """Serve the built React app; unknown non-API paths get index.html so client routing works."""
    router = APIRouter(include_in_schema=False)
    root = dist_dir.resolve()
    index_file = root / FRONTEND_INDEX_FILE

    @router.get(FRONTEND_ROUTE_PATH)
    def serve_frontend(requested_path: str) -> FileResponse:
        if requested_path.startswith(API_PATH_PREFIX):
            raise RouteNotFoundError(requested_path)
        candidate = (root / requested_path).resolve()
        if candidate.is_file() and candidate.is_relative_to(root):
            return FileResponse(candidate)
        return FileResponse(index_file)

    return router
