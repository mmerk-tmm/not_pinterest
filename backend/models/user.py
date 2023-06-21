from backend.db.base_class import Base
from sqlalchemy import Column, DateTime, Integer, String, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship, backref, object_session
from backend.core.config import env_config
from sqlalchemy.dialects.postgresql import UUID


class User(Base):
    __tablename__ = "users"

    def __init__(self, current_user_id=None, is_liked=False, posts_page=1, **kwargs):
        super().__init__(**kwargs)
        self.current_user_id = current_user_id
        self.is_liked = is_liked
        self.posts_page = posts_page

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(
        String(int(env_config.get("VITE_MAX_FIRSTNAME_LENGTH"))), nullable=True
    )
    last_name = Column(
        String(int(env_config.get("VITE_MAX_LASTNAME_LENGTH"))), nullable=True
    )
    username = Column(
        String(int(env_config.get("VITE_MAX_LOGIN_LENGTH"))),
        index=True,
        unique=True,
        nullable=False,
    )
    description = Column(
        String(int(env_config.get("VITE_MAX_DESCRIPTION_LENGTH"))), nullable=True
    )
    site = Column(String(int(env_config.get("VITE_MAX_SITE_LENGTH"))), nullable=True)
    hashed_password = Column(String, index=True, nullable=False)
    is_superuser = Column(Boolean, default=False)
    picture_id = Column(
        UUID(as_uuid=True),
        ForeignKey("images.id", name="users_picture_id_fkey", ondelete="SET NULL"),
    )
    picture = relationship(
        "Image", foreign_keys=[picture_id], cascade="all,delete", backref="user_profile"
    )

    @property
    def followers_count(self):
        return (
            object_session(self)
            .query(User)
            .join(UserLike, UserLike.user_id == self.id)
            .count()
        )

    @property
    def liked(self):
        is_liked = self.is_liked if hasattr(self, "is_liked") else False
        if is_liked:
            return True
        current_user_id = (
            self.current_user_id if hasattr(self, "current_user_id") else None
        )
        if current_user_id is None:
            return False
        return (
            object_session(self)
            .query(UserLike)
            .filter(
                UserLike.user_id == current_user_id, UserLike.liked_user_id == self.id
            )
            .first()
            is not None
        )

    @property
    def posts(self):
        end = self.posts_page * 30
        db_posts = (
            object_session(self)
            .query(Post)
            .filter(Post.user_id == self.id)
            .order_by(Post.time_created.desc())
            .slice(end - 30, end)
            .all()
        )
        for post in db_posts:
            post.current_user_id = self.current_user_id
        return db_posts


class UserLike(Base):
    __tablename__ = "users_likes"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True, nullable=False)
    liked_user_id = Column(
        Integer, ForeignKey("users.id"), primary_key=True, nullable=False
    )
    user = relationship("User", foreign_keys=[user_id])
    liked_user = relationship(
        "User",
        foreign_keys=[liked_user_id],
        backref=backref("likes", cascade="all,delete"),
    )


class PersonalInformation(Base):
    __tablename__ = "personal_information"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    gender = Column(
        String(int(env_config.get("VITE_MAX_GENDER_LENGTH"))), nullable=False
    )


class Post(Base):
    __tablename__ = "posts"

    def __init__(self, current_user_id=None, is_liked=False, **kwargs):
        super().__init__(**kwargs)
        self.current_user_id = current_user_id
        self.is_liked = is_liked

    id = Column(Integer, primary_key=True, index=True)
    title = Column(
        String(int(env_config.get("VITE_MAX_POST_NAME_LENGTH"))), nullable=True
    )
    description = Column(String(500), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    time_created = Column(DateTime(timezone=True), server_default=func.now())
    idea_id = Column(
        Integer, ForeignKey("ideas.id", ondelete="SET NULL"), nullable=True
    )
    idea = relationship("Idea", foreign_keys=[idea_id])
    image_id = Column(UUID(as_uuid=True), ForeignKey("images.id"), nullable=False)
    picture = relationship("Image", cascade="all,delete", backref="post")
    url = Column(String, nullable=True)
    keywords = relationship(
        "Keyword", secondary="posts_keywords", backref=backref("posts", lazy=True)
    )

    @property
    def user(self):
        db_user = (
            object_session(self).query(User).filter(User.id == self.user_id).first()
        )
        db_user.current_user_id = self.current_user_id
        return db_user

    @property
    def liked(self):
        is_liked = self.is_liked if hasattr(self, "is_liked") else False
        if is_liked:
            return True
        current_user_id = (
            self.current_user_id if hasattr(self, "current_user_id") else None
        )
        if current_user_id is None:
            return False
        return (
            object_session(self)
            .query(PostLike)
            .filter(PostLike.user_id == current_user_id, PostLike.post_id == self.id)
            .first()
            is not None
        )

    @property
    def comments(self):
        db_comments = (
            object_session(self)
            .query(PostComment)
            .filter(PostComment.post_id == self.id)
            .all()
        )
        for db_comment in db_comments:
            db_comment.user.current_user_id = self.current_user_id
        return db_comments


class PostLike(Base):
    __tablename__ = "posts_likes"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True, nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), primary_key=True, nullable=False)
    post = relationship(Post, backref=backref("likes", cascade="all,delete"))


class PostComment(Base):
    __tablename__ = "posts_comments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_edited = Column(
        DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now()
    )
    content = Column(
        String(int(env_config.get("VITE_MAX_POST_COMMENT_LENGTH"))), nullable=True
    )
    post = relationship(Post, foreign_keys=[post_id], overlaps="posts,comments")
    user = relationship(User, foreign_keys=[user_id], overlaps="users,comments")


class PostKeyword(Base):
    __tablename__ = "posts_keywords"

    post_id = Column(Integer, ForeignKey("posts.id"), primary_key=True, nullable=False)
    keyword_id = Column(
        Integer, ForeignKey("keywords.id"), primary_key=True, nullable=False
    )
    keyword = relationship(
        "Keyword", foreign_keys=[keyword_id], overlaps="keywords,posts"
    )
    post = relationship(Post, foreign_keys=[post_id], overlaps="keywords,posts")
