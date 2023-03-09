from backend.db.base_class import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from backend.core.config import env_config
from sqlalchemy import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import backref


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(
        int(env_config.get('VITE_MAX_POST_NAME_LENGTH'))), nullable=True)
    description = Column(String(500), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", foreign_keys=[user_id])
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    idea_id = Column(Integer, ForeignKey(
        "ideas.id", ondelete='SET NULL'), nullable=True)
    idea = relationship("Idea", foreign_keys=[idea_id])
    image_id = Column(UUID(as_uuid=True), ForeignKey(
        "images.id"), nullable=False)
    picture = relationship("Image", cascade="all,delete", backref="post")
    url = Column(String, nullable=True)
    keywords = relationship(
        "Keyword", secondary="posts_keywords")


class PostLike(Base):
    __tablename__ = 'posts_likes'

    user_id = Column(Integer, ForeignKey("users.id"),
                     primary_key=True, nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"),
                     primary_key=True, nullable=False)
    post = relationship(Post, backref=backref(
        "likes", cascade="all,delete"))


class PostComment(Base):
    __tablename__ = 'posts_comments'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_edited = Column(DateTime(timezone=True),
                         server_default=func.now(), server_onupdate=func.now())
    content = Column(String(
        int(env_config.get('VITE_MAX_POST_COMMENT_LENGTH'))
    ), nullable=True)
    post = relationship(Post, backref=backref(
        "comments", cascade="all,delete"))


class PostKeyword(Base):
    __tablename__ = 'posts_keywords'

    post_id = Column(Integer, ForeignKey("posts.id"),
                     primary_key=True, nullable=False)
    keyword_id = Column(Integer, ForeignKey("keywords.id"),
                        primary_key=True, nullable=False)
    keyword = relationship("Keyword", foreign_keys=[
                           keyword_id])
    post = relationship(Post, foreign_keys=[post_id])
