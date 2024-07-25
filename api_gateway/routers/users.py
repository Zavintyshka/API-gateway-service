from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schemas import ReturnUserSchema, UserChangeDataSchema
from database.database import get_db
from ..oauth2 import get_current_user
from database.models import Users

__all__ = ["users_router"]

users_router = APIRouter(prefix="/user", tags=["Account"])


@users_router.get("/account/", response_model=ReturnUserSchema)
def get_user_data(db: Session = Depends(get_db), user: Users = Depends(get_current_user)):
    return user


@users_router.put("/account/", response_model=ReturnUserSchema)
def update_user_data(new_user_data: UserChangeDataSchema,
                     db: Session = Depends(get_db),
                     user: Users = Depends(get_current_user)):
    user_row = db.query(Users).filter(user.id == Users.id)
    user_row.update(dict(new_user_data), synchronize_session=False)
    db.commit()
    return user
