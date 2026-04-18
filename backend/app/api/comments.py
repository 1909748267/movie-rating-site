from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentUpdate
from app.services.comment_service import CommentService
from app.utils.response import success_response, error_response

router = APIRouter(tags=["评论"])


@router.post("/api/v1/movies/{movie_id}/comments")
def create_comment(
    movie_id: int,
    comment_data: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    comment = CommentService.create_comment(db, current_user.id, movie_id, comment_data)
    return success_response({"comment_id": comment.id}, "评论成功")


@router.get("/api/v1/movies/{movie_id}/comments")
def get_comments(
    movie_id: int,
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db)
):
    comments, total = CommentService.get_comments_by_movie(db, movie_id, page, page_size)
    
    comment_responses = []
    for comment in comments:
        comment_dict = {
            "id": comment.id,
            "user_id": comment.user_id,
            "username": comment.user.username,
            "content": comment.content,
            "created_at": comment.created_at.isoformat(),
            "updated_at": comment.updated_at.isoformat()
        }
        comment_responses.append(comment_dict)
    
    return success_response({
        "comments": comment_responses,
        "total": total,
        "page": page,
        "page_size": page_size
    })


@router.put("/api/v1/comments/{comment_id}")
def update_comment(
    comment_id: int,
    comment_data: CommentUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        CommentService.update_comment(db, comment_id, current_user.id, comment_data)
        return success_response(message="评论更新成功")
    except ValueError as e:
        return error_response("FORBIDDEN", str(e))


@router.delete("/api/v1/comments/{comment_id}")
def delete_comment(
    comment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        CommentService.delete_comment(db, comment_id, current_user.id)
        return success_response(message="评论删除成功")
    except ValueError as e:
        return error_response("FORBIDDEN", str(e))
