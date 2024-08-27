from fastapi import APIRouter, Depends, status, HTTPException, Form
from fastapi_mail import FastMail, MessageSchema
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import Users
from .oauth2 import create_reset_token
from .settings import email_config

email_router = APIRouter(prefix="/email", tags=["E-mail"])

reset_password_message = """
You are receiving this email because you requested a password reset for your account. If you did not request this, please ignore this email.

To reset your password, follow this link:

{reset_link}

This link will be valid for 60 minutes. After that, you will need to request a new password reset link.

---

Having trouble resetting your password?

If you're having trouble resetting your password or have any other questions, please contact our support team: support@mediaconverterapp.com.

---

Best regards,
MediaConverterApp
"""


@email_router.post("/reset-password/", status_code=status.HTTP_200_OK)
async def reset_password(email=Form(...), username=Form(...), db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.email == email, Users.username == username).first()
    if not user:
        return {"detail": "success"}

    fm = FastMail(email_config)
    reset_token = create_reset_token({"email": email, "username": username})
    reset_link = f"http://192.168.0.176:5050/change-password/{reset_token}"
    message = MessageSchema(
        subject="Password Reset",
        recipients=[email],
        body=reset_password_message.format(reset_link=reset_link),
        subtype="plain"
    )
    await fm.send_message(message)
    return {"detail": "success"}
