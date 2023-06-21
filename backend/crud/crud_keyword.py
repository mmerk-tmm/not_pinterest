from typing import List
from backend.db.base import CRUDBase
from backend.models.user import Post, PostKeyword
from backend.models.keywords import KeywordLike, Keyword
from sqlalchemy import func


class KeywordCRUD(CRUDBase):
    def get_keyword_by_id(self, keyword_id: int) -> Keyword | None:
        return self.get(id=keyword_id, model=Keyword)

    def get_keywords(self, page, page_size=20) -> List[Keyword]:
        end = page * page_size
        return (
            self.db.query(Keyword)
            .order_by(Keyword.id.desc())
            .slice(end - page_size, end)
            .all()
        )

    def get_keyword_like_by_user_id(
        self, user_id: int, keyword_id: int
    ) -> KeywordLike | None:
        return (
            self.db.query(KeywordLike)
            .filter(
                KeywordLike.keyword_id == keyword_id and KeywordLike.user_id == user_id
            )
            .first()
        )

    def get_popular_keywords(self, page, page_size=20) -> List[Keyword]:
        end = page * page_size
        return (
            self.db.query(Keyword)
            .join(KeywordLike)
            .group_by(func.count(KeywordLike.keyword_id).desc())
            .slice(end - page_size, end)
            .all()
        )

    def count_keyword_likes(self, keyword_id: int) -> int:
        return (
            self.db.query(KeywordLike)
            .filter(KeywordLike.keyword_id == keyword_id)
            .count()
        )

    def toggle_like_keyword(self, user_id: int, keyword_id: int) -> bool:
        liked = self.get_keyword_like_by_user_id(user_id=user_id, keyword_id=keyword_id)
        if liked:
            self.delete(model=liked)
            return False
        else:
            self.create(model=KeywordLike(keyword_id=keyword_id, user_id=user_id))
            return True

    def search_keywords(self, name: str, limit: int = 10) -> List[Keyword]:
        return (
            self.db.query(Keyword)
            .filter(Keyword.name.ilike("%{}%".format(name)))
            .limit(limit)
            .all()
        )

    def create_keyword(self, name: str):
        return self.create(
            Keyword(
                name=name,
            )
        )

    def get_keyword_by_name(self, name: str) -> Keyword | None:
        return self.db.query(Keyword).filter(Keyword.name == name).first()

    def get_keyword_posts(self, keyword_id: int, page, page_size=20) -> List[Post]:
        end = page * page_size
        return (
            self.db.query(Post)
            .join(PostKeyword)
            .filter(PostKeyword.keyword_id == keyword_id)
            .order_by(Post.id.desc())
            .slice(end - page_size, end)
            .all()
        )

    def delete_keyword(self, keyword: Keyword):
        self.delete(model=keyword)
