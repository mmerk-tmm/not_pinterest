from fastapi import APIRouter
from fastapi import HTTPException, status
from backend.crud.crud_comments import CommentCRUD
from backend.helpers.auth_helper import Authenticate
from backend.schemas.schemas import CreateComment, PostComment
from fastapi import Depends, APIRouter, status, HTTPException
from fastapi import HTTPException, Depends, APIRouter, status


router = APIRouter(tags=["Комментарии"], prefix="/comments")


@router.put("/{comment_id}", response_model=PostComment)
def update_comment(
    comment_id: int,
    comment_data: CreateComment,
    Auth: Authenticate = Depends(Authenticate()),
):
    comment_cruds = CommentCRUD(Auth.db)
    comment = comment_cruds.get_comment_by_id(comment_id=comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Комментарий не найден"
        )
    if comment.user_id != Auth.current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Вы не можете изменить чужой комментарий",
        )
    return comment_cruds.update_comment(db_comment=comment, text=comment_data.text)


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id: int, Auth: Authenticate = Depends(Authenticate())):
    comment_cruds = CommentCRUD(Auth.db)
    comment = comment_cruds.get_comment_by_id(comment_id=comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Комментарий не найден"
        )
    if comment.user_id != Auth.current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Вы не можете удалить чужой комментарий",
        )
    comment_cruds.delete_comment(db_comment=comment)
