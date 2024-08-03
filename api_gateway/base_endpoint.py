from fastapi import APIRouter, status, HTTPException
from pathlib import Path

from fastapi.responses import FileResponse

from api_gateway.api_gateway_tools import get_file_location

base_router = APIRouter(prefix="/base", tags=["Base"])


class BaseEndpoint:
    def __init__(self, router: APIRouter = base_router):
        self.router = router
        self.add_endpoints()

    def add_endpoints(self):
        @self.router.get("/file/{image_name}/", status_code=status.HTTP_200_OK)
        async def get_file(image_name: str):
            image_path = Path(f"server_storage/achievements/{image_name}")
            if not image_path.exists():
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not Found")
            return FileResponse(image_path)

    def get_router(self):
        return self.router
