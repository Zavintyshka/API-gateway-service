# 3rd Party
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Project's modules
from .settings import settings

SQLALCHEMY_DB_URL = f"postgresql+psycopg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.HOST}/{settings.DB_NAME}"
SQLALCHEMY_ENGINE = create_engine(SQLALCHEMY_DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=SQLALCHEMY_ENGINE)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
