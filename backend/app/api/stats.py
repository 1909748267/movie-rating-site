from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.user import User
from app.models.movie import Movie
from app.models.comment import Comment
from app.utils.response import success_response

router = APIRouter(prefix="/api/v1/stats", tags=["统计"])


@router.get("")
def get_stats(db: Session = Depends(get_db)):
    movie_count = db.query(func.count(Movie.id)).scalar()
    user_count = db.query(func.count(User.id)).scalar()
    comment_count = db.query(func.count(Comment.id)).scalar()
    
    return success_response({
        "movie_count": movie_count,
        "user_count": user_count,
        "comment_count": comment_count
    })
