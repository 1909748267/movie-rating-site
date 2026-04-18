from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.crawlers.crawler_manager import CrawlerManager
from app.utils.response import success_response, error_response

router = APIRouter(prefix="/api/v1/crawler", tags=["爬虫"])


@router.post("/movies")
def crawl_movies(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        manager = CrawlerManager()
        count = manager.crawl_movies(db)
        return success_response({"saved_count": count}, f"成功爬取并保存了 {count} 部电影")
    except Exception as e:
        return error_response("CRAWL_ERROR", f"爬取失败: {str(e)}")
