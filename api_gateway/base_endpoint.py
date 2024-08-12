from fastapi import APIRouter, status, HTTPException, Request
from pathlib import Path

from fastapi.responses import FileResponse
from .cache import CacheValidator

base_router = APIRouter(prefix="/base", tags=["Base"])


class BaseEndpoint:
    def __init__(self, router: APIRouter = base_router):
        self.router = router
        self.add_endpoints()

    def add_endpoints(self):
        @self.router.get("/file/{image_name}/", status_code=status.HTTP_200_OK)
        async def get_file(request: Request, image_name: str):
            image_path = Path(f"server_storage/achievements/{image_name}")
            if not image_path.exists():
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not Found")

            cache_validator = CacheValidator(request, image_path)
            etag = cache_validator.file_etag

            if cache_validator.validate_cache_headers():
                return cache_validator.get_304_response()

            return FileResponse(image_path, headers={"Cache-Control": "max-age=3600-", "ETag": etag})

    def get_router(self):
        return self.router
