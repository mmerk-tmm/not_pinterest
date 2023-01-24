from backend.db.base_class import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from backend.core.config import env_config
from sqlalchemy import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(
        int(env_config.get('VITE_MAX_POST_NAME_LENGTH'))), nullable=True)
    description = Column(String(500), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    idea_id = Column(Integer, ForeignKey("ideas.id"), nullable=False)
    image_id = Column(UUID(as_uuid=True), ForeignKey(
        "images.id"), nullable=False)
    image = relationship("Image", foreign_keys=[image_id])
    url = Column(String, nullable=True)


class PostLike(Base):
    __tablename__ = 'posts_likes'

    user_id = Column(Integer, ForeignKey("users.id"),
                     primary_key=True, nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"),
                     primary_key=True, nullable=False)


class PostComment(Base):
    __tablename__ = 'posts_comments'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    content = Column(String(
        int(env_config.get('VITE_MAX_POST_COMMENT_LENGTH'))
    ), nullable=True)


class PostKeyword(Base):
    __tablename__ = 'posts_keywords'

    post_id = Column(Integer, ForeignKey("posts.id"),
                     primary_key=True, nullable=False)
    keyword = Column(String, ForeignKey("keywords.name"),
                     primary_key=True, nullable=False)


class Keyword(Base):
    __tablename__ = 'keywords'

    name = Column(String(
        int(env_config.get('VITE_MAX_KEYWORD_NAME_LENGTH'))), primary_key=True, nullable=False)
