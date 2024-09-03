from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session, contains_eager
from ..schemas import ReturnUserSchema, UserChangeDataSchema, AchievementInfo, PasswordResetSchema
from ..settings import settings
from database.database import get_db
from ..security import hash_password
from ..oauth2 import get_current_user, verify_reset_token
from database.models import Users, Achievement, UserAchievementProgress
from typing import List

__all__ = ["users_router"]

users_router = APIRouter(prefix="/user", tags=["Account"])


@users_router.get("/account/", response_model=ReturnUserSchema)
def get_user_data(user: Users = Depends(get_current_user)):
    return user


@users_router.put("/account/", response_model=ReturnUserSchema)
def update_user_data(new_user_data: UserChangeDataSchema,
                     db: Session = Depends(get_db),
                     user: Users = Depends(get_current_user)):
    user_row = db.query(Users).filter(user.id == Users.id)
    user_row.update(dict(new_user_data), synchronize_session=False)
    db.commit()
    return user


@users_router.get("/achievement/", status_code=status.HTTP_200_OK, response_model=List[AchievementInfo])
def get_user_achievements(db: Session = Depends(get_db), user: Users = Depends(get_current_user)):
    user_achievement_list = db.query(Achievement).join(UserAchievementProgress).filter(
        UserAchievementProgress.user_id == int(user.id)).options(contains_eager(Achievement.user_progress)).all()
    achievement_info_list = []
    for user_achievement in user_achievement_list:
        user_achievement_progress: UserAchievementProgress = user_achievement.user_progress[0]
        achievement_info = {"name": user_achievement.name,
                            "description": user_achievement.description,
                            "service": user_achievement.service,
                            "image_link": f"{settings.SCHEMA}://{settings.HOST}:{settings.PORT}/base/file/{user_achievement.image_name}/",
                            "unlocked": user_achievement_progress.completed,
                            "progress": user_achievement_progress.progress,
                            "target": user_achievement_progress.target}
        achievement_info_list.append(AchievementInfo(**achievement_info))
    return achievement_info_list


@users_router.get("/check-token/{reset_token:str}/", status_code=status.HTTP_200_OK)
def check_reset_token(reset_token: str):
    is_valid_token = verify_reset_token(reset_token)
    if not is_valid_token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="password-rest token isn't valid or it already expired")
    email, username = is_valid_token
    return {"email": email, "username": username}


@users_router.post("/reset-password/{reset_token:str}/", status_code=status.HTTP_200_OK)
def reset_user_password(user_data: PasswordResetSchema, reset_token: str, db: Session = Depends(get_db)):
    is_valid_token = verify_reset_token(reset_token)
    if not is_valid_token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="password-rest token isn't valid or it already expired")
    email, username = is_valid_token
    password, repeated_password = user_data.password, user_data.repeated_password

    if password != repeated_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="password not the same")

    hashed_password = hash_password(password)

    user: Users = db.query(Users).filter(Users.username == username, Users.email == email).first()
    user.password = hashed_password
    db.add(user)
    db.commit()
    return {"detail": "password reset successfully"}
