from uuid import uuid4
from sqlalchemy import Column, Integer, String, func, TIMESTAMP, UUID, ForeignKey, Enum
from sqlalchemy.orm import relationship

from .database import Base
from .database_types import ServiceType, FileExtension


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP(timezone=True), server_default=func.now())


class RawStorage(Base):
    __tablename__ = "raw_storage"
    file_id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    file_uuid = Column(UUID(as_uuid=True), nullable=False, unique=True)
    filename = Column(String, nullable=False)
    file_extension = Column(Enum(FileExtension), nullable=False)
    # ON_DELETE ON_UPDATE
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    service_type = Column(Enum(ServiceType), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # relationships
    action = relationship("Actions", uselist=False, back_populates="raw_file")


class ProcessedStorage(Base):
    __tablename__ = "processed_storage"
    file_id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    file_uuid = Column(UUID(as_uuid=True), nullable=False, unique=True)
    filename = Column(String, nullable=False)
    file_extension = Column(Enum(FileExtension), nullable=False)
    # ON_DELETE ON_UPDATE
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    service_type = Column(Enum(ServiceType), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # relationships
    action = relationship("Actions", uselist=False, back_populates="processed_file")


class Actions(Base):
    __tablename__ = "actions"
    action_id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    raw_file_uuid = Column(UUID(as_uuid=True), ForeignKey("raw_storage.file_uuid"), nullable=False, unique=True)
    processed_file_uuid = Column(UUID(as_uuid=True), ForeignKey("processed_storage.file_uuid"), nullable=False,
                                 unique=True)
    # ON_DELETE ON_UPDATE
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    service_type = Column(Enum(ServiceType), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # relationships
    raw_file = relationship("RawStorage", uselist=False, back_populates="action")
    processed_file = relationship("ProcessedStorage", uselist=False, back_populates="action")
