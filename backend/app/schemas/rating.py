from pydantic import BaseModel, field_validator


class RatingCreate(BaseModel):
    score: int

    @field_validator('score')
    @classmethod
    def score_range(cls, v):
        if not 1 <= v <= 5:
            raise ValueError('评分必须在1-5之间')
        return v


class RatingResponse(BaseModel):
    score: int

    class Config:
        from_attributes = True


class RatingStatsResponse(BaseModel):
    avg_score: float
    count: int
