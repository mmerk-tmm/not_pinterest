
from backend.helpers.images import set_picture
from backend.crud.crud_post import post_cruds
from backend.models.post import Post
from fastapi.encoders import jsonable_encoder
from backend.helpers.ideas import set_idea_data


def get_post_json(post: Post, current_user_id: int = None, idea_data: bool = False, user_data: bool = False):
    post_obj = jsonable_encoder(post)
    post_obj = set_picture(post_obj, post.image)
    if idea_data:
        post_obj['idea'] = set_idea_data(post.idea)
    if user_data:
        post_obj['user'] = jsonable_encoder(post.user)
    # post_obj['user'] = get_user_json(post.user)
    # post_obj['idea'] = get_idea_json(post.idea)
    post_obj['likes'] = post_cruds.count_post_likes(post.id)
    post_obj['liked'] = post_cruds.get_post_like_by_user_id(
        user_id=current_user_id, post_id=post.id) is not None
    post_obj = set_picture(post_obj, post.image)
    return post_obj
