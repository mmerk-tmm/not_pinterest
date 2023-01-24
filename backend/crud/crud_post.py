from typing import List
from backend.db.base import CRUDBase
from backend.models.post import Post, PostLike, Keyword
from backend.models.idea import Idea


class PostCruds(CRUDBase):

    def create_post(self, name: str, description: str, user_id: int, idea_id: int):
        return self.create(Post(name=name, description=description, user_id=user_id, idea_id=idea_id))

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


post_cruds = PostCruds()
