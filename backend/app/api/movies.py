from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.movie import Movie
from app.schemas.movie import MovieResponse, MovieListResponse
from app.services.movie_service import MovieService
from app.utils.response import success_response, error_response

router = APIRouter(prefix="/api/v1/movies", tags=["电影"])


@router.get("")
def get_movies(page: int = 1, page_size: int = 20, db: Session = Depends(get_db)):
    movies, total = MovieService.get_movies(db, page, page_size)
    
    movie_responses = []
    for movie in movies:
        avg_score, rating_count = MovieService.get_movie_rating_stats(db, movie.id)
        movie_dict = {
            "id": movie.id,
            "title": movie.title,
            "poster_url": movie.poster_url,
            "director": movie.director,
            "avg_score": avg_score,
            "rating_count": rating_count
        }
        movie_responses.append(movie_dict)
    
    return success_response({
        "movies": movie_responses,
        "total": total,
        "page": page,
        "page_size": page_size
    })


@router.get("/{movie_id}")
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = MovieService.get_movie_by_id(db, movie_id)
    
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_response("NOT_FOUND", "电影不存在")
        )
    
    avg_score, rating_count = MovieService.get_movie_rating_stats(db, movie.id)
    
    movie_dict = {
        "id": movie.id,
        "title": movie.title,
        "poster_url": movie.poster_url,
        "director": movie.director,
        "actors": movie.actors,
        "genre": movie.genre,
        "release_date": movie.release_date,
        "duration": movie.duration,
        "synopsis": movie.synopsis,
        "avg_score": avg_score,
        "rating_count": rating_count
    }
    
    return success_response(movie_dict)


@router.get("/{movie_id}/ratings")
def get_movie_ratings(movie_id: int, db: Session = Depends(get_db)):
    avg_score, count = MovieService.get_movie_rating_stats(db, movie_id)
    
    return success_response({
        "avg_score": avg_score,
        "count": count
    })
