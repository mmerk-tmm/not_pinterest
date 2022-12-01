from datetime import datetime
from backend.crud.crud_idea import idea_cruds
from backend.models.idea import Idea
from backend.core.config import settings


def set_idea_data(idea: Idea):
    idea_obj = idea.as_dict()
    idea_obj['created'] = idea.time_created.strftime(
        settings.DATETIME_FORMAT)
    idea_obj['likes'] = idea_cruds.count_idea_likes(idea_id=idea.id)
    return idea_obj
