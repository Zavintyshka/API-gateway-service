from uuid import UUID
from typing import Literal
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


class FileRow(BaseModel):
    file_uuid: UUID
    filename: str
    file_extension: FileExtension
    user_id: int
    service_type: ServiceType
    created_at: datetime


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
