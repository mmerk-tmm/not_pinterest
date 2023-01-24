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
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)


class IdeaLike(Base):
    __tablename__ = 'ideas_likes'

    user_id = Column(Integer, ForeignKey("users.id"),
                     primary_key=True, nullable=False)
    idea_id = Column(Integer, ForeignKey("ideas.id"),
                     primary_key=True, nullable=False)
    user = relationship("User", foreign_keys=[user_id])


# class Topic(Base):
#     __tablename__ = 'topics'
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(
#         String(
#             int(env_config.get('VITE_MAX_TOPIC_NAME_LENGTH'))
#         ), nullable=True, unique=True)


# class IdeaTopic(Base):
#     __tablename__ = 'ideas_topics'
#     idea_id = Column(Integer, ForeignKey("ideas.id"),
#                      primary_key=True, nullable=False)
#     topic_id = Column(Integer, ForeignKey("topics.id"),
#                       primary_key=True, nullable=False)
#     topic = relationship("Topic", foreign_keys=[topic_id])


# class IdeaKeyword(Base):
#     __tablename__ = 'ideas_keywords'
#     idea_id = Column(Integer, ForeignKey("ideas.id"),
#                      primary_key=True, nullable=False)
#     keyword_id = Column(Integer, ForeignKey("keywords.name"),
#                         primary_key=True, nullable=False)
#     keyword = relationship("Keyword", foreign_keys=[keyword_id])


# class Keyword(Base):
#     __tablename__ = 'keywords'

#     name = Column(
#         String(
#             int(env_config.get('VITE_MAX_KEYWORD_NAME_LENGTH'))
#         ), nullable=False, unique=True, primary_key=True)
#     uses = Column(Integer, default=0)
