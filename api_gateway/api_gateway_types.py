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


class Commands(Enum):
    mp4_to_mp3 = "mp4_to_mp3"
