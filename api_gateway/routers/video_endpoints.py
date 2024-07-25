import shutil

from fastapi import UploadFile, File, Form, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.routing import APIRouter
from pydantic import ValidationError

from ..schemas import UploadedFileMetadata

__all__ = ["video_router"]

video_router = APIRouter(prefix="/video", tags=["Video"])


@video_router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_file(filename: str = Form(...),
                      user_id: int = Form(...),
                      file: UploadFile = File(...)):
    location = "./user_files/{}"

    try:
        file_metadata = UploadedFileMetadata(filename=filename, user_id=user_id)
    except ValidationError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid File Metadata")

    file_path = location.format(file_metadata.filename)
    user_id = file_metadata.user_id
    print(f"Запись в дб {file_path=}, {user_id=}")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"detail": "success"}


@video_router.get("/upload/{filename}", status_code=status.HTTP_200_OK)
async def get_file(filename: str):
    file_path = f"./user_files/{filename}"
    return FileResponse(file_path)
