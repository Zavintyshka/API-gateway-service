from enum import Enum


class FileState(Enum):
    raw = "raw"
    processed = "processed"


class ServiceType(Enum):
    audio = "audio_files"
    image = "image_files"
    video = "video_files"
