from sqlalchemy.sql import func
from db.base_class import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, ARRAY, DateTime
from sqlalchemy.orm import relationship
from core.config import env_config


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(
        String(
            int(env_config.get('VITE_MAX_FIRSTNAME_LENGTH'))
        ), nullable=True)
    last_name = Column(
        String(
            int(env_config.get('VITE_MAX_LASTNAME_LENGTH'))
        ), nullable=True)
    username = Column(
        String(
            int(env_config.get('VITE_MAX_LOGIN_LENGTH'))
        ), index=True, nullable=False)
    hashed_password = Column(String, index=True, nullable=False)
    is_superuser = Column(Boolean, default=False)
    files = relationship("File")
    picture = relationship("File", uselist=False, overlaps="files")


class File(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String)
    original_file_name = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="files",
                        foreign_keys=[user_id], overlaps="picture")
    type = Column(String, default='file')
