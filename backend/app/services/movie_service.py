from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List, Tuple
from app.models.movie import Movie
from app.models.rating import Rating


class MovieService:
    @staticmethod
    def get_movies(db: Session, page: int = 1, page_size: int = 20) -> Tuple[List[Movie], int]:
        offset = (page - 1) * page_size
        query = db.query(Movie)
        
        total = query.count()
        movies = query.offset(offset).limit(page_size).all()
        
        return movies, total

    @staticmethod
    def get_movie_by_id(db: Session, movie_id: int) -> Optional[Movie]:
        return db.query(Movie).filter(Movie.id == movie_id).first()

    @staticmethod
    def get_movie_rating_stats(db: Session, movie_id: int) -> Tuple[float, int]:
        result = db.query(
            func.avg(Rating.score).label('avg_score'),
            func.count(Rating.id).label('count')
        ).filter(Rating.movie_id == movie_id).first()
        
        avg_score = float(result.avg_score) if result.avg_score else 0.0
        count = result.count
        
        return avg_score, count
