from pydantic_settings import BaseSettings, SettingsConfigDict
from alembic.config import Config


class DBSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file="database/.env", env_file_encoding="UTF-8")
    DB_USER: str
    DB_PASSWORD: int
    HOST: str
    DB_NAME: str


settings = DBSettings()
alembic_config = Config("alembic.ini")
