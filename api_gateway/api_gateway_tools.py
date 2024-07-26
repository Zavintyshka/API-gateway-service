from pathlib import Path

from .settings import STORAGE_PATH
from .api_gateway_types import FileStatePath, MicroservicesStoragePath
from database.database_types import FileExtension


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
