from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..schemas import ReturnUserSchema, UserChangeDataSchema, AchievementSchema, AchievementInfo
from ..settings import settings
from database.database import get_db
from ..oauth2 import get_current_user
from database.models import Users, UserAchievement, Achievement
from typing import List

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


# TEST FUNC
@users_router.post("/achievement/", status_code=status.HTTP_201_CREATED)
def set_achievement_to_user(achievement: AchievementSchema, db: Session = Depends(get_db),
                            user: Users = Depends(get_current_user)):
    achievement_id = achievement.achievement_id
    row = UserAchievement(achievement_id=achievement_id, user_id=user.id)
    db.add(row)
    db.commit()
    return {"detail": "success"}


# TEST FUNC


@users_router.get("/achievement/", status_code=status.HTTP_200_OK, response_model=List[AchievementInfo])
def get_user_achievements(db: Session = Depends(get_db), user: Users = Depends(get_current_user)):
    achievements = db.query(Achievement).all()
    achievement_info_list = []
    for achievement in achievements:
        # Slow implementation
        unlocked = bool([row_user for row_user in achievement.users if row_user.user_id == user.id])
        image_download_link = f"{settings.SCHEMA}://{settings.HOST}:{settings.PORT}/base/file/{achievement.image_name}/"
        achievement_info_list.append(AchievementInfo(unlocked=unlocked, **achievement.__dict__,
                                                     image_link=image_download_link))
    return achievement_info_list
