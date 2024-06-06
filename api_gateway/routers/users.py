from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schemas import UserSchema
from database.database import get_db
from ..oauth2 import get_current_user
from database.models import Users

__all__ = ["users_router"]

users_router = APIRouter(prefix="/user", tags=["Account"])


@users_router.get("/account/", response_model=UserSchema)
def get_user_data(db: Session = Depends(get_db), user: Users = Depends(get_current_user)):
    return user
