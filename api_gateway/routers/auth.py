from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import Users
from ..security import is_password_legit
from ..oauth2 import create_access_token
from ..schemas import Token

__all__ = ["auth_router"]

auth_router = APIRouter(prefix="/login", tags=["Login"])


@auth_router.post("/", response_model=Token)
def login(user_credential: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    username = user_credential.username
    password = user_credential.password
    user = db.query(Users).filter(Users.username == username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")

    if not is_password_legit(password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect password")

    payload = {"user_id": user.id, "username": user.username}
    jwt_token = create_access_token(payload=payload)
    token = Token(access_token=jwt_token, token_type="Bearer")
    return token
