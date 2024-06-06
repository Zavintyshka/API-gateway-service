from pydantic import BaseModel, EmailStr
from typing import Literal


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    firstname: str
    lastname: str


class TokenData(BaseModel):
    user_id: int
    username: str


class Token(BaseModel):
    access_token: str
    token_type: Literal["Bearer"]
