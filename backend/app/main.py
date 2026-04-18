from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, users, movies, ratings, comments, stats, crawler

app = FastAPI(title="电影评分网站API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(movies.router)
app.include_router(ratings.router)
app.include_router(comments.router)
app.include_router(stats.router)
app.include_router(crawler.router)


@app.get("/")
def root():
    return {"message": "电影评分网站API"}
