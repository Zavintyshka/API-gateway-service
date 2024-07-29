from pathlib import Path

from sqlalchemy.orm import Session

from .schemas import ProcessedFileSchema, ActionSchema
from .settings import STORAGE_PATH
from .api_gateway_types import FileStatePath, MicroservicesStoragePath
from database.database_types import FileExtension
from database.models import RawStorage, ProcessedStorage, Actions


def generate_path(microservice_path: MicroservicesStoragePath,
                  user_id: str,
                  file_state_path: FileStatePath,
                  filename: str) -> Path:
    user_folder = STORAGE_PATH / microservice_path.value / user_id
    if not user_folder.exists():
        init_path(microservice_path=microservice_path, user_id=user_id)
    file_path = user_folder / file_state_path.value / filename
    return file_path


def init_path(microservice_path: MicroservicesStoragePath, user_id: str) -> None:
    for file_state in FileStatePath:
        file_state_path = file_state.value
        (STORAGE_PATH / microservice_path.value / user_id / file_state_path).mkdir(parents=True, exist_ok=True)


def get_file_extension(filename_str: str) -> FileExtension:
    filename = Path(filename_str)
    file_extension = filename.suffix[1:]
    return FileExtension[file_extension]


def get_file_location(db_row: RawStorage | ProcessedStorage) -> Path:
    # STORAGE_PATH/{service_type}/{user_id}/{file_state}/{file_uuid}+"."+{file_extension}
    file_state = FileStatePath.raw.value if isinstance(db_row, RawStorage) else FileStatePath.processed.value
    service_type = db_row.service_type.value + "_files"
    user_id = str(db_row.user_id)
    file_uuid = str(db_row.file_uuid)
    file_extension = db_row.file_extension.value
    filename = f"{file_uuid}.{file_extension}"
    return Path(STORAGE_PATH) / service_type / user_id / file_state / filename


def create_record(db_session: Session, schema: ProcessedFileSchema | ActionSchema) -> None:
    model = ProcessedStorage if isinstance(schema, ProcessedFileSchema) else Actions
    data = dict(schema)
    row = model(**data)
    db_session.add(row)
    db_session.commit()
