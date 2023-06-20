from datetime import datetime
from backend.crud.crud_idea import IdeaCRUD
from backend.helpers.images import set_picture
from backend.models.idea import Idea
from backend.core.config import settings
from sqlalchemy.orm import Session


def set_idea_data(idea: Idea, db: Session, user_id: int = None):
    idea_cruds = IdeaCRUD(db)
    idea_obj = idea.as_dict()
    idea_obj['created'] = idea.created.strftime(
        settings.DATETIME_FORMAT)
    idea_obj['likes'] = idea_cruds.count_idea_likes(idea_id=idea.id)
    idea_obj['user'] = set_picture(idea.user.as_dict(), idea.user.picture)
    if user_id:
        idea_obj['liked'] = bool(idea_cruds.get_idea_like_by_user_id(
            user_id=user_id, idea_id=idea.id))

    return idea_obj
