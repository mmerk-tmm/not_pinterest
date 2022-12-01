from backend.db.base_class import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from backend.core.config import env_config
from sqlalchemy.sql import func


class Idea(Base):
    __tablename__ = 'ideas'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(
        String(
            int(env_config.get('VITE_MAX_IDEA_NAME_LENGTH'))
        ), nullable=True, unique=True)
    description = Column(
        String(
            int(env_config.get('VITE_MAX_IDEA_DESCRIPTION_LENGTH'))
        ), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", foreign_keys=[user_id])


class IdeaLike(Base):
    __tablename__ = 'ideas_likes'

    user_id = Column(Integer, ForeignKey("users.id"),
                     primary_key=True, nullable=False)
    idea_id = Column(Integer, ForeignKey("ideas.id"),
                     primary_key=True, nullable=False)
    user = relationship("User", foreign_keys=[user_id])


class Topic(Base):
    __tablename__ = 'topics'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(
        String(
            int(env_config.get('VITE_MAX_TOPIC_NAME_LENGTH'))
        ), nullable=True, unique=True)
