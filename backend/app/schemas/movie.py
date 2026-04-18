from pydantic import BaseModel
from typing import Optional


class MovieBase(BaseModel):
    title: str
    poster_url: Optional[str] = None
    director: Optional[str] = None
    actors: Optional[str] = None
    genre: Optional[str] = None
    release_date: Optional[str] = None
    duration: Optional[int] = None
    synopsis: Optional[str] = None


class MovieCreate(MovieBase):
    source: Optional[str] = None
    source_id: Optional[str] = None


class MovieResponse(MovieBase):
    id: int
    avg_score: Optional[float] = None
    rating_count: int = 0

    class Config:
        from_attributes = True


class MovieListResponse(BaseModel):
    movies: list[MovieResponse]
    total: int
    page: int
    page_size: int
