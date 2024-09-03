from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import Users

stats_router = APIRouter(prefix="/stats", tags=["Stats"])


@stats_router.get("/")
def get_stats_all_user(db: Session = Depends(get_db)):
    total = db.query(func.sum(Users.total_processed)).scalar()
    total = total if total else 0
    return {"total": total}


@stats_router.get("/{user_id}")
def get_stats_user(user_id: int, db: Session = Depends(get_db)):
    try:
        total = db.query(Users).filter(Users.id == user_id).first().total_processed
    except AttributeError:
        total = "nan"
    return {"total": total}
