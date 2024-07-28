from enum import Enum


class ServiceType(Enum):
    audio = "audio"
    image = "image"
    video = "video"


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
