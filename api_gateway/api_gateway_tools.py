from pathlib import Path

import redis.exceptions
import sqlalchemy
from sqlalchemy.orm import Session
from redis import Redis
from .schemas import ProcessedFileSchema, ActionSchema, ProcessFileSchema, ComponentStatus
from .settings import STORAGE_PATH, settings
from .api_gateway_types import FileStatePath, MicroservicesStoragePath, VideoActionType, StatusType
from database.database_types import FileExtension
from database.models import RawStorage, ProcessedStorage, Actions, UserAchievementProgress, Users


def check_db(db: Session):
    is_available: StatusType
    try:
        db.query(Users)
    except Exception:
        is_available = StatusType.not_serving
    else:
        is_available = StatusType.serving
    return ComponentStatus(component_name="Postgres DB", status=is_available)


def check_redis():
    redis_client = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)
    is_available: StatusType
    try:
        redis_client.execute_command("ping")
    except redis.exceptions.ConnectionError:
        is_available = StatusType.not_serving
    else:
        is_available = StatusType.serving
    return ComponentStatus(component_name="Redis", status=is_available)


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


def increment_achievement_progress(db: Session, user_id: int, transaction_data: ProcessFileSchema) -> None:
    achievement_name: str
    match transaction_data.action_type:
        case VideoActionType.cut:
            achievement_name = "YT Shorts Lover"
        case VideoActionType.convert:
            to_ext = transaction_data.action.split(";")[1]
            if to_ext == FileExtension.mp3.value:
                achievement_name = "MP3 Fan"
            elif to_ext == FileExtension.wav.value:
                achievement_name = "WAV Devotee"
    entry: UserAchievementProgress = db.query(UserAchievementProgress).filter(
        UserAchievementProgress.achievement_name == achievement_name,
        UserAchievementProgress.user_id == user_id).first()
    entry.progress += 1
