from backend.db.base_class import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from backend.core.config import env_config
from sqlalchemy.dialects.postgresql import UUID


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
        ), index=True, unique=True, nullable=False)
    description = Column(
        String(
            int(env_config.get('VITE_MAX_DESCRIPTION_LENGTH'))
        ), nullable=True)
    site = Column(
        String(
            int(env_config.get('VITE_MAX_SITE_LENGTH'))
        ), nullable=True)
    hashed_password = Column(String, index=True, nullable=False)
    is_superuser = Column(Boolean, default=False)
    picture_id = Column(UUID(as_uuid=True), ForeignKey(
        "images.id", ondelete='SET NULL'))
    picture = relationship("Image", foreign_keys=[picture_id], cascade="all,delete",
                           backref="user_profile")


class PersonalInformation(Base):
    __tablename__ = 'personal_information'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    gender = Column(
        String(
            int(env_config.get('VITE_MAX_GENDER_LENGTH'))
        ), nullable=False)
