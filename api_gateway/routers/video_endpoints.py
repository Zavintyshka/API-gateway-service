import shutil
from fastapi import UploadFile, File, Form, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.routing import APIRouter
from pydantic import ValidationError
from ..schemas import UploadedFileMetadata
from ..api_gateway_types import FileStatePath, MicroservicesStoragePath
from ..api_gateway_tools import generate_path

__all__ = ["video_router"]

video_router = APIRouter(prefix="/video", tags=["Video"])


@video_router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_file(filename: str = Form(...),
                      user_id: str = Form(...),
                      file: UploadFile = File(...)):
    input_path = generate_path(microservice_path=MicroservicesStoragePath.video_service,
                               user_id=user_id,
                               file_state_path=FileStatePath.raw,
                               filename=filename)

    try:
        file_metadata = UploadedFileMetadata(filename=filename, user_id=user_id)
    except ValidationError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid File Metadata")

    with input_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"detail": "success"}


@video_router.get("/upload/{filename}", status_code=status.HTTP_200_OK)
async def get_file(filename: str):
    file_path = f"./user_files/{filename}"
    return FileResponse(file_path)
