from sqlalchemy import Column, Integer, String, func, TIMESTAMP, UUID, ForeignKey, Enum

from .database import Base
from .database_types import FileState, ServiceType


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP(timezone=True), server_default=func.now())


class Storage(Base):
    __tablename__ = "storage"
    file_id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    file_uuid = Column(UUID, nullable=False, unique=True)
    filename = Column(String, nullable=False)
    # ON_DELETE ON_UPDATE
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    file_state = Column(Enum(FileState), nullable=False)
    service_type = Column(Enum(ServiceType), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
