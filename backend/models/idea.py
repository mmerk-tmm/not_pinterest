from backend.db.base_class import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, object_session
from backend.core.config import env_config
from sqlalchemy.sql import func
from backend.models.keywords import Keyword
from backend.models.user import Post


class Idea(Base):
    __tablename__ = "ideas"

    def __init__(self, current_user_id=None, is_liked=False, posts_page=1, **kwargs):
        super().__init__(**kwargs)
        self.current_user_id = current_user_id
        self.is_liked = is_liked
        self.posts_page = posts_page

    id = Column(Integer, primary_key=True, index=True)
    name = Column(
        String(int(env_config.get("VITE_MAX_IDEA_NAME_LENGTH"))),
        nullable=True,
        unique=True,
    )
    description = Column(
        String(int(env_config.get("VITE_MAX_IDEA_DESCRIPTION_LENGTH"))), nullable=True
    )
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", foreign_keys=[user_id])

    @property
    def keywords(self):
        if not hasattr(self, "_keywords"):
            self._keywords = (
                object_session(self)
                .query(Keyword)
                .join(IdeaKeyword, Keyword.id == IdeaKeyword.keyword_id)
                .filter(IdeaKeyword.idea_id == self.id)
                .all()
            )
        return self._keywords

    @property
    def likes(self):
        if not hasattr(self, "_likes"):
            self._likes = (
                object_session(self).query(IdeaLike).filter_by(idea_id=self.id).count()
            )
        return self._likes

    @property
    def posts(self):
        if not hasattr(self, "_posts"):
            end = self.posts_page * 30
            self._posts = (
                object_session(self)
                .query(Post)
                .filter(Post.idea_id == self.id)
                .order_by(Post.time_created.desc())
                .slice(end - 30, end)
                .all()
            )
            for post in self._posts:
                post.current_user_id = self.current_user_id
        return self._posts


class IdeaLike(Base):
    __tablename__ = "ideas_likes"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True, nullable=False)
    idea_id = Column(Integer, ForeignKey("ideas.id"), primary_key=True, nullable=False)
    user = relationship("User", foreign_keys=[user_id])
    idea = relationship(Idea, foreign_keys=[idea_id])


class IdeaKeyword(Base):
    __tablename__ = "ideas_keywords"

    idea_id = Column(Integer, ForeignKey("ideas.id"), primary_key=True, nullable=False)
    keyword_id = Column(
        Integer, ForeignKey("keywords.id"), primary_key=True, nullable=False
    )
    idea = relationship(Idea, foreign_keys=[idea_id])
    keyword = relationship("Keyword", foreign_keys=[keyword_id])
