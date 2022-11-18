from backend.db.base_class import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from backend.core.config import env_config


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
    picture_id = Column(Integer, ForeignKey("files.id", ondelete='SET NULL'))
    picture = relationship("File", foreign_keys=[picture_id])
