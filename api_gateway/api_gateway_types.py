from enum import Enum
from pathlib import Path


class FileStatePath(Enum):
    raw = Path("raw_files")
    processed = Path("processed_files")


class FileState(Enum):
    raw = "raw"
    processed = "processed"


class MicroservicesStoragePath(Enum):
    video_service = Path("video_files")
    audio_service = Path("audio_files")
    image_service = Path("image_files")


class VideoActionType(Enum):
    cut = "cut"
    convert = "convert"


class ImageAction(Enum):
    pass


class AudioAction(Enum):
    pass


class StatusType(Enum):
    serving = "serving"
    not_serving = "not_serving"
