from backend.db.base_class import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from backend.core.config import env_config


class Keyword(Base):
    __tablename__ = 'keywords'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(
        int(env_config.get('VITE_MAX_KEYWORD_NAME_LENGTH'))), nullable=False)


class KeywordLike(Base):
    __tablename__ = 'keywords_likes'

    user_id = Column(Integer, ForeignKey("users.id"),
                     primary_key=True, nullable=False)
    keyword_id = Column(Integer, ForeignKey("keywords.id"),
                        primary_key=True, nullable=False)
    keyword = relationship(Keyword, backref=backref(
        "likes", cascade="all,delete"))
