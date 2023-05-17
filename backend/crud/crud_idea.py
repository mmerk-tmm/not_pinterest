from typing import List
from backend.db.base import CRUDBase
from backend.models.idea import Idea, IdeaLike, IdeaKeyword
from backend.models.keywords import Keyword


class IdeaCRUD(CRUDBase):
    def create_idea(self, *, name: str, description: str, user_id: int):

        return self.create(Idea(name=name, description=description, user_id=user_id))

    def search_ideas(self, query: str) -> List[Idea]:
        return self.db.query(Idea).filter(Idea.name.ilike(f'%{query}%')).limit(10).all()

    def get_idea_by_id(self, idea_id: int) -> Idea | None:
        return self.get(id=idea_id, model=Idea)

    def get_ideas(self, page, page_size=20) -> List[Idea]:
        end = page * page_size
        return self.db.query(Idea).order_by(Idea.id.desc()).slice(end-page_size, end).all()

    def get_popular_ideas(self, page, page_size=20) -> List[Idea]:
        end = page * page_size
        return self.db.query(Idea).outerjoin(IdeaLike).group_by(Idea.id).order_by(
            Idea.id.desc()).slice(end-page_size, end).all()

    def get_idea_like_by_user_id(self, user_id: int, idea_id: int):
        return self.db.query(IdeaLike).filter(
            IdeaLike.idea_id == idea_id and IdeaLike.user_id == user_id).first()

    def count_idea_likes(self, idea_id: int):
        return self.db.query(IdeaLike).filter(IdeaLike.idea_id == idea_id).count()

    def toggle_like_idea(self, user_id: int, idea_id: int) -> bool:
        liked = self.get_idea_like_by_user_id(user_id=user_id, idea_id=idea_id)
        if liked:
            self.delete(model=liked)
            return False
        else:
            self.create(model=IdeaLike(idea_id=idea_id, user_id=user_id))
            return True

    def get_idea_by_name(self, name: str):
        return self.db.query(Idea).filter(Idea.name == name).first()
