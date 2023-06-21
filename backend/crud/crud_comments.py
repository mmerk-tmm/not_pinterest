from backend.db.base import CRUDBase
from backend.models.user import PostComment


class CommentCRUD(CRUDBase):
    def get_post_comments(self, post_id: int):
        return self.db.query(PostComment).filter(PostComment.post_id == post_id).all()

    def create_comment(self, post_id: int, user_id: int, text: str):
        return self.create(PostComment(post_id=post_id, user_id=user_id, text=text))

    def get_comment_by_id(self, comment_id: int) -> PostComment | None:
        return self.get(id=comment_id, model=PostComment)

    def delete_comment(self, db_comment: PostComment):
        self.delete(model=db_comment)

    def update_comment(self, db_comment: PostComment, text: str):
        db_comment.text = text
        return self.update(db_comment)
