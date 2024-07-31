from uuid import UUID
from typing import Literal, Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr
from .api_gateway_types import Commands
from database.database_types import FileExtension, ServiceType


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    firstname: str
    lastname: str


class UserChangeDataSchema(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr


class ReturnUserSchema(BaseModel):
    username: str
    email: EmailStr
    firstname: str
    lastname: str
    registered_at: datetime


class TokenData(BaseModel):
    user_id: int
    username: str


class Token(BaseModel):
    access_token: str
    token_type: Literal["Bearer"]


class UploadedFileMetadata(BaseModel):
    filename: str
    user_id: str


class Pair(BaseModel):
    user_id: int
    service_type: ServiceType

    raw_download_link: str
    raw_filename: str
    raw_file_extension: FileExtension
    raw_created_at: datetime

    converted_download_link: Optional[str] = None
    converted_filename: Optional[str] = None
    converted_file_extension: Optional[FileExtension] = None
    converted_created_at: Optional[datetime] = None


class ProcessFileSchema(BaseModel):
    file_uuid: str
    from_extension: FileExtension
    to_extension: FileExtension


class ProcessedFileSchema(BaseModel):
    file_uuid: UUID
    filename: str
    file_extension: FileExtension
    user_id: str
    service_type: ServiceType


class ActionSchema(BaseModel):
    raw_file_uuid: UUID
    processed_file_uuid: UUID
    user_id: str
    service_type: ServiceType
