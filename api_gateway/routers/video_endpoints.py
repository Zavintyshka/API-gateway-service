import shutil
import uuid
from typing import List

from fastapi import UploadFile, File, Form, HTTPException, status, Depends
from fastapi.responses import FileResponse
from fastapi.routing import APIRouter
from pydantic import ValidationError
from sqlalchemy.orm import Session
from database.database import get_db
from database.database_types import ServiceType, FileExtension
from database.models import Users, RawStorage, ProcessedStorage, Actions
from ..schemas import UploadedFileMetadata, ProcessFileSchema, ActionSchema, Pair
from ..oauth2 import get_current_user
from ..api_gateway_types import FileStatePath, FileState, MicroservicesStoragePath
from ..api_gateway_tools import generate_path, get_file_extension, get_file_location, create_record
from ..settings import settings

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
    return {"file_uuid": file_uuid}


@video_router.get("/pairs_list/", status_code=status.HTTP_200_OK, response_model=List[Pair])
async def get_pairs_list(user: Users = Depends(get_current_user), db: Session = Depends(get_db)) -> List[Pair]:
    def get_download_link(service_type: ServiceType, file_state: FileState, file_uuid: str) -> str:
        return f"{settings.HOST}:{settings.PORT}/{service_type.value}/file/{file_state.value}/{file_uuid}"

    file_list = db.query(RawStorage).filter(user.id == RawStorage.user_id)
    pairs = []
    for row in file_list:
        row: RawStorage
        dict_for_schema = {"user_id": row.user_id,
                           "service_type": row.service_type,
                           "raw_download_link": get_download_link(ServiceType.video, FileState.raw, row.file_uuid),
                           "raw_filename": row.filename,
                           "raw_file_extension": row.file_extension,
                           "raw_created_at": row.created_at
                           }
        if row.action and row.action.processed_file:
            converted_row: ProcessedStorage = row.action.processed_file
            dict_for_schema.update(
                {"converted_download_link": get_download_link(ServiceType.video, FileState.processed,
                                                              converted_row.file_uuid),
                 "converted_filename": converted_row.filename,
                 "converted_file_extension": converted_row.file_extension,
                 "converted_created_at": converted_row.created_at, })
        pairs.append(Pair(**dict_for_schema))
    return pairs


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


@video_router.post("/processes_file/", status_code=status.HTTP_201_CREATED)
async def processes_file(process_form: ProcessFileSchema, user: Users = Depends(get_current_user),
                         db: Session = Depends(get_db)):
    video_microservice_grpc = VideoMicroserviceGrpc(from_extension=process_form.from_extension,
                                                    to_extension=process_form.to_extension,
                                                    user_id=str(user.id))
    processed_file_data = video_microservice_grpc.make_request(raw_file_uuid=process_form.file_uuid)
    action_data = ActionSchema(raw_file_uuid=process_form.file_uuid,
                               processed_file_uuid=processed_file_data.file_uuid,
                               user_id=str(user.id),
                               service_type=video_microservice_grpc.service_type)

    create_record(db_session=db, schema=processed_file_data)  # processed_storage
    create_record(db_session=db, schema=action_data)  # processed_storage

    return {"detail": "success"}
