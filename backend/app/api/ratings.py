from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.rating import RatingCreate, RatingResponse
from app.services.rating_service import RatingService
from app.utils.response import success_response, error_response

router = APIRouter(tags=["评分"])


@router.post("/api/v1/movies/{movie_id}/ratings")
def create_rating(
    movie_id: int,
    rating_data: RatingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        RatingService.create_rating(db, current_user.id, movie_id, rating_data)
        return success_response(message="评分成功")
    except ValueError as e:
        return error_response("ALREADY_RATED", str(e))


@router.put("/api/v1/movies/{movie_id}/ratings")
def update_rating(
    movie_id: int,
    rating_data: RatingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        RatingService.update_rating(db, current_user.id, movie_id, rating_data)
        return success_response(message="评分更新成功")
    except ValueError as e:
        return error_response("NOT_RATED", str(e))


@router.get("/api/v1/movies/{movie_id}/ratings/me")
def get_user_rating(
    movie_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    rating = RatingService.get_user_rating(db, current_user.id, movie_id)
    
    if not rating:
        return success_response({"score": None})
    
    return success_response({"score": rating.score})
