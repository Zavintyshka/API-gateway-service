import sqlalchemy.exc
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..schemas import UserSchema
from database.database import get_db
from database.models import Users
from ..security import hash_password

__all__ = ["reg_router"]

reg_router = APIRouter(prefix="/registration", tags=["Login"])


@reg_router.post("/", status_code=status.HTTP_201_CREATED)
def registrate(user: UserSchema, db: Session = Depends(get_db)):
    user = dict(user)
    user["password"] = hash_password(user["password"])
    new_user = Users(**user)
    try:
        db.add(new_user)
        db.commit()
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=409,
                            detail="Some of your data was incorrect while registration process. Please try again.")
    return {"detail": "success"}
