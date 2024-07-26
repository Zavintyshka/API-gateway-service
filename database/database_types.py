from enum import Enum


class FileState(Enum):
    raw = "raw"
    processed = "processed"


class ServiceType(Enum):
    audio = "audio_files"
    image = "image_files"
    video = "video_files"


class FileExtension(Enum):
    # video
    mp4 = "mp4"
    mov = "mov"

    # audio
    mp3 = "mp3"
    wav = "wav"
    ogg = "ogg"

    # image
    png = "png"
    jpg = "jpg"
    jpeg = "jpeg"
