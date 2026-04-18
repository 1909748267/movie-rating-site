from sqlalchemy.orm import Session
from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentUpdate


class CommentService:
    @staticmethod
    def create_comment(db: Session, user_id: int, movie_id: int, comment_data: CommentCreate) -> Comment:
        comment = Comment(
            user_id=user_id,
            movie_id=movie_id,
            content=comment_data.content
        )
        
        db.add(comment)
        db.commit()
        db.refresh(comment)
        
        return comment

    @staticmethod
    def get_comments_by_movie(db: Session, movie_id: int, page: int = 1, page_size: int = 20) -> tuple[list[Comment], int]:
        offset = (page - 1) * page_size
        query = db.query(Comment).filter(Comment.movie_id == movie_id)
        
        total = query.count()
        comments = query.order_by(Comment.created_at.desc()).offset(offset).limit(page_size).all()
        
        return comments, total

    @staticmethod
    def update_comment(db: Session, comment_id: int, user_id: int, comment_data: CommentUpdate) -> Comment:
        comment = db.query(Comment).filter(Comment.id == comment_id).first()
        
        if not comment:
            raise ValueError("评论不存在")
        
        if comment.user_id != user_id:
            raise ValueError("无权修改此评论")
        
        comment.content = comment_data.content
        db.commit()
        db.refresh(comment)
        
        return comment

    @staticmethod
    def delete_comment(db: Session, comment_id: int, user_id: int) -> None:
        comment = db.query(Comment).filter(Comment.id == comment_id).first()
        
        if not comment:
            raise ValueError("评论不存在")
        
        if comment.user_id != user_id:
            raise ValueError("无权删除此评论")
        
        db.delete(comment)
        db.commit()
