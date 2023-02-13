from typing import List
from backend.db.base import CRUDBase
from backend.models.post import KeywordLike, Post, PostComment, PostLike, Keyword
from backend.models.idea import Idea, IdeaLike
from backend.models.files import Image
from backend.models.user import UserLike
from sqlalchemy import or_


class PostCRUD(CRUDBase):

    def get_user_posts(self, page, user_id, page_size=20):
        end = page * page_size
        return self.db.query(Post).filter(Post.user_id == user_id).order_by(Post.id.desc()).slice(end-page_size, end).all()

    def create_post(self, title: str, description: str, user_id: int, url: str, idea_id: int, db_picture: Image):
        return self.create(
            Post(
                title=title,
                url=url,
                description=description,
                user_id=user_id,
                idea_id=idea_id,
                image_id=db_picture.id
            )
        )

    def get_post_by_id(self, post_id: int) -> Post | None:
        return self.get(id=post_id, model=Post)

    def get_posts(self, page, page_size=20) -> List[Post]:
        end = page * page_size
        return self.db.query(Post).order_by(Post.id.desc()).slice(end-page_size, end).all()

    def get_post_like_by_user_id(self, user_id: int, post_id: int):
        return self.db.query(PostLike).filter(
            PostLike.post_id == post_id and PostLike.user_id == user_id).first()

    def count_post_likes(self, post_id: int):
        return self.db.query(PostLike).filter(PostLike.post_id == post_id).count()

    def toggle_like_post(self, user_id: int, post_id: int) -> bool:
        liked = self.get_post_like_by_user_id(user_id=user_id, post_id=post_id)
        if liked:
            self.delete(model=liked)
            return False
        else:
            self.create(model=PostLike(post_id=post_id, user_id=user_id))
            return True

    def search_idea(self, name: str, limit: int = 10):
        return self.db.query(Idea).filter(Idea.name.like("%{}%".format(name))).limit(limit).all()

    def search_keywords(self, name: str, limit: int = 10):
        return self.db.query(Keyword).filter(Keyword.name.like("%{}%".format(name))).limit(limit).all()

    def update_post(self, db_post: Post, title: str, description: str, url: str):
        db_post.title = title
        db_post.description = description
        db_post.url = url
        self.create(db_post)

    def delete_post(self, db_post: Post):
        self.delete(db_post)

    def create_comment(self, user_id, post, text):
        return self.create(PostComment(user_id=user_id, post=post, content=text))

    def get_comments(self, post_id, page, page_size=10):
        end = page * page_size
        return self.db.query(PostComment).filter(PostComment.post_id == post_id).order_by(PostComment.id.desc()).slice(end-page_size, end).all()

    def get_last_recommendations(self, user_id, page, page_size=10):
        end = page*page_size
        return self.db.query(Post).join(IdeaLike, UserLike, KeywordLike).filter(or_(IdeaLike.user_id == user_id, UserLike.user_id == user_id, KeywordLike.user_id == user_id)).order_by(Post.id.desc()).slice(end-page_size, end).all()
