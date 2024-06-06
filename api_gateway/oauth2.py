# Build in
from datetime import datetime, timedelta, UTC

# 3rd Party
from jose import JWTError, jwt
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

# Project's modules
from .schemas import TokenData
from database.database import get_db
from database.models import Users
from .settings import settings

OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(payload: dict):
    payload_to_encode = payload.copy()
    expire_time = datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload_to_encode.update({"exp": expire_time})
    encoded_jwt = jwt.encode(payload_to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        user_id, username, expire_time = (payload.get(data) for data in ("user_id", "username", "expire_time"))

        if user_id and username and expire_time:
            raise credentials_exception

        token_data = TokenData(user_id=user_id, username=username, expire_time=expire_time)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(OAUTH2_SCHEME), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})

    token: TokenData = verify_token(token, credentials_exception)
    user_id = token.user_id
    username = token.username
    user = db.query(Users).filter(Users.id == user_id, Users.username == username).first()
    if user is None:
        raise credentials_exception
    return user
