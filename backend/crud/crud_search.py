from sqlalchemy import Text, cast, desc, func, literal_column, union_all
from backend.crud.crud_file import FileCRUD
from backend.crud.crud_post import PostCRUD
from backend.db.base import CRUDBase
from backend.models.files import Image
from backend.schemas.schemas import AllSearchItems, PostIdBase, UserInfo, PostBase, IdeaWithUser
from backend.models.user import Post, User, PostLike, UserLike
from backend.models.idea import Idea, IdeaLike


from backend.crud.crud_file import FileCRUD


class SearchCRUD(CRUDBase):
    def search_all(self, query: str):
        label_num_likes = "num_likes"
        label_resource_type = "resource_type"
        label_id = "id"
        post_resource_type = 'post'
        idea_resource_type = 'idea'
        user_resource_type = 'user'
        q1 = self.db.query(
            Post.id.label(label_id),
            func.count(PostLike.post_id).label(label_num_likes),
            literal_column(f"'{post_resource_type}'").label(
                label_resource_type)
        ).join(
            PostLike, Post.id == PostLike.post_id, isouter=True
        ).filter(
            func.lower(Post.title).contains(query.lower())
        ).group_by(Post.id)

        q2 = self.db.query(
            User.id.label(label_id),
            func.count(UserLike.user_id).label(label_num_likes),
            literal_column(f"'{user_resource_type}'").label(
                label_resource_type)
        ).join(
            UserLike, UserLike.user_id == User.id, isouter=True
        ).filter(
            func.lower(User.username).contains(query.lower())
        ).group_by(User.id)

        q3 = self.db.query(
            Idea.id.label(label_id),
            func.count(IdeaLike.idea_id).label(label_num_likes),
            literal_column(f"'{idea_resource_type}'").label(
                label_resource_type)
        ).join(IdeaLike, IdeaLike.idea_id == Idea.id, isouter=True
               ).filter(

            func.lower(Idea.name).contains(query.lower())
        ).group_by(Idea.id)

        query = union_all(q1, q2, q3)
        query_result = self.db.query(
            getattr(query.c, label_id),
            getattr(query.c, label_num_likes),
            getattr(query.c, label_resource_type),
        ).order_by(desc(label_num_likes)).limit(5).all()
        results = []
        for query_item in query_result:
            resource_type = getattr(query_item, label_resource_type)

            model_schema = None
            if resource_type == post_resource_type:
                model_schema = PostIdBase.from_orm(PostCRUD(self.db).get_post_by_id(
                    post_id=query_item.id
                ))

            elif resource_type == idea_resource_type:
                model_schema = IdeaWithUser.from_orm(self.db.query(Idea).filter(
                    Idea.id == query_item.id).first())
            elif resource_type == user_resource_type:
                model_schema = UserInfo.from_orm(self.db.query(User).filter(
                    User.id == query_item.id).first())

            if model_schema:
                results.append(AllSearchItems(
                    type=resource_type,
                    info=model_schema
                ))
        return results
