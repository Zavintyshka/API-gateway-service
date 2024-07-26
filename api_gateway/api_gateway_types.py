from enum import Enum
from pathlib import Path


class FileStatePath(Enum):
    raw = Path("raw_files")
    processed = Path("processed_files")


class MicroservicesStoragePath(Enum):
    video_service = Path("video_files")
    audio_service = Path("audio_files")
    image_service = Path("image_files")
