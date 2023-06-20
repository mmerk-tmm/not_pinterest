
from backend.helpers.images import set_picture
from backend.crud.crud_post import PostCRUD
from backend.models.post import Post
from fastapi.encoders import jsonable_encoder
from backend.helpers.ideas import set_idea_data
from sqlalchemy.orm import Session


def get_post_json(post: Post, db: Session, current_user_id: int = None, idea_data: bool = False, user_data: bool = False):
    post_cruds = PostCRUD(db)
    post_obj = jsonable_encoder(post)
    post_obj = set_picture(post_obj, post.picture)
    if idea_data:
        post_obj['idea'] = set_idea_data(
            post.idea, db=db, user_id=current_user_id)
    if user_data:
        post_obj['user'] = jsonable_encoder(post.user)
    post_obj['likes'] = post_cruds.count_post_likes(post.id)
    post_obj['liked'] = post_cruds.get_post_like_by_user_id(
        user_id=current_user_id, post_id=post.id) is not None
    return post_obj
