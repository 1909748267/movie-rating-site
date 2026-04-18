from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    poster_url = Column(String, nullable=True)
    director = Column(String, nullable=True)
    actors = Column(String, nullable=True)
    genre = Column(String, nullable=True)
    release_date = Column(String, nullable=True)
    duration = Column(Integer, nullable=True)
    synopsis = Column(String, nullable=True)
    source = Column(String, nullable=True)
    source_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
