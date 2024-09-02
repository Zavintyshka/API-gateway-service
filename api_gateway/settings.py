from pydantic_settings import BaseSettings, SettingsConfigDict
from fastapi_mail import ConnectionConfig


class Settings(BaseSettings):
    # not implemented
    SCHEMA: str
    HOST: str
    PORT: str

    model_config = SettingsConfigDict(env_file="api_gateway/.env", env_file_encoding="UTF8")
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    EMAIL_HOST: str
    EMAIL_PORT: int
    IS_SSL: bool
    EMAIL_SENDER: str
    EMAIL_PASSWORD: str

    REDIS_HOST: str
    REDIS_PORT: int


settings = Settings()
STORAGE_PATH = "./storage"

email_config = ConnectionConfig(
    MAIL_USERNAME=settings.EMAIL_SENDER,
    MAIL_PASSWORD=settings.EMAIL_PASSWORD,
    MAIL_PORT=settings.EMAIL_PORT,
    MAIL_SERVER=settings.EMAIL_HOST,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=settings.IS_SSL,
    MAIL_FROM=settings.EMAIL_SENDER
)
