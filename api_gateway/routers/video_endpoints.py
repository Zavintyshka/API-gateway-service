import shutil
import uuid
from typing import List

from fastapi import UploadFile, File, Form, HTTPException, status, Depends
from fastapi.responses import FileResponse
from fastapi.routing import APIRouter
from pydantic import ValidationError
from sqlalchemy.orm import Session
from database.database import get_db
from database.database_types import ServiceType
from database.models import Users, RawStorage, ProcessedStorage, Actions
from ..schemas import UploadedFileMetadata, FileRow
from ..oauth2 import get_current_user
from ..api_gateway_types import FileStatePath, FileState, MicroservicesStoragePath
from ..api_gateway_tools import generate_path, get_file_extension, get_file_location

from grpc_services.api_gateway_grpc import VideoMicroserviceGrpc

__all__ = ["video_router"]

video_router = APIRouter(prefix="/video", tags=["Video"])


@video_router.post("/file/", status_code=status.HTTP_201_CREATED)
async def upload_file(filename: str = Form(...),
                      file: UploadFile = File(...),
                      user: Users = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    try:
        file_metadata = UploadedFileMetadata(filename=filename, user_id=str(user.id))
    except ValidationError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid File Metadata")

    try:
        file_extension = get_file_extension(filename_str=filename)
    except KeyError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Unsupported File Extension")

    file_uuid = uuid.uuid4()
    storage_filename = str(file_uuid) + "." + file_extension.value

    # Downloading File
    input_path = generate_path(microservice_path=MicroservicesStoragePath.video_service,
                               user_id=file_metadata.user_id,
                               file_state_path=FileStatePath.raw,
                               filename=storage_filename)
    with input_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Creating DB Row
    file_row = RawStorage(file_uuid=file_uuid,
                          filename=file_metadata.filename,
                          file_extension=file_extension,
                          user_id=user.id,
                          service_type=ServiceType.video)
    db.add(file_row)
    db.commit()
    return {"detail": "success"}


@video_router.get("/file_row_list/", status_code=status.HTTP_200_OK, response_model=List[FileRow])
async def get_file_row_list(user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    file_list = db.query(RawStorage).filter(user.id == RawStorage.user_id)
    return file_list


@video_router.get("/file/{file_state}/{file_uuid}", status_code=status.HTTP_200_OK)
async def get_file(file_state: str, file_uuid: str, user: Users = Depends(get_current_user),
                   db: Session = Depends(get_db)):
    try:
        uuid.UUID(file_uuid)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file identifier")

    try:
        FileState[file_state]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid File state")

    storage_model = RawStorage if FileState[file_state].value == "raw" else ProcessedStorage

    db_row = db.query(storage_model).filter(file_uuid == storage_model.file_uuid).first()
    if not db_row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

    if not db_row.user_id == user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only the owner can view the file")

    file_path = get_file_location(db_row)
    return FileResponse(file_path)


@video_router.get("/processes_file/", status_code=status.HTTP_201_CREATED)
async def processes_file():
    video_microservice_grpc = VideoMicroserviceGrpc()
    video_microservice_grpc.make_requests()
    return {"detail": "success"}

# # --FOR TEST--
# processed_file_uuid = uuid.uuid4()
# processed_file_row = ProcessedStorage(file_uuid=processed_file_uuid,
#                                       filename=file_metadata.filename,
#                                       file_extension=file_extension,
#                                       user_id=user.id,
#                                       service_type=ServiceType.video)
# db.add(processed_file_row)
# action_row = Actions(raw_file_uuid=file_uuid,
#                      processed_file_uuid=processed_file_uuid,
#                      user_id=user.id,
#                      service_type=ServiceType.video)
# db.add(action_row)
# # --FOR TEST--
