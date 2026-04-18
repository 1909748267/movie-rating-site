from sqlalchemy.orm import Session
from typing import Optional
from app.models.rating import Rating
from app.schemas.rating import RatingCreate


class RatingService:
    @staticmethod
    def create_rating(db: Session, user_id: int, movie_id: int, rating_data: RatingCreate) -> Rating:
        existing = db.query(Rating).filter(
            Rating.user_id == user_id,
            Rating.movie_id == movie_id
        ).first()
        
        if existing:
            raise ValueError("您已经评分过该电影")
        
        rating = Rating(
            user_id=user_id,
            movie_id=movie_id,
            score=rating_data.score
        )
        
        db.add(rating)
        db.commit()
        db.refresh(rating)
        
        return rating

    @staticmethod
    def update_rating(db: Session, user_id: int, movie_id: int, rating_data: RatingCreate) -> Rating:
        rating = db.query(Rating).filter(
            Rating.user_id == user_id,
            Rating.movie_id == movie_id
        ).first()
        
        if not rating:
            raise ValueError("您还没有评分该电影")
        
        rating.score = rating_data.score
        db.commit()
        db.refresh(rating)
        
        return rating

    @staticmethod
    def get_user_rating(db: Session, user_id: int, movie_id: int) -> Optional[Rating]:
        return db.query(Rating).filter(
            Rating.user_id == user_id,
            Rating.movie_id == movie_id
        ).first()
