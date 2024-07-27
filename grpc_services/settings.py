from pydantic_settings import BaseSettings, SettingsConfigDict


class GrpcSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file="grpc_services/.env", env_file_encoding="UTF-8")

    VIDEO_IP_ADDR: str
    AUDIO_IP_ADDR: str
    IMAGE_IP_ADDR: str
    VIDEO_PORT: str
    AUDIO_PORT: str
    IMAGE_PORT: str


settings = GrpcSettings()

VIDEO_MICROSERVICE_URL = settings.VIDEO_IP_ADDR + ":" + settings.VIDEO_PORT
AUDIO_MICROSERVICE_URL = settings.AUDIO_IP_ADDR + ":" + settings.AUDIO_PORT
IMAGE_MICROSERVICE_URL = settings.IMAGE_IP_ADDR + ":" + settings.IMAGE_PORT
