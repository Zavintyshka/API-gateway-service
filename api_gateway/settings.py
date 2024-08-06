from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # not implemented
    SCHEMA: str
    HOST: str
    PORT: str

    model_config = SettingsConfigDict(env_file="api_gateway/.env", env_file_encoding="UTF8")
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int


settings = Settings()

STORAGE_PATH = "./storage"
