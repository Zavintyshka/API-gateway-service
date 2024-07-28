from uuid import UUID
from typing import Literal
from datetime import datetime
from pydantic import BaseModel, EmailStr
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
