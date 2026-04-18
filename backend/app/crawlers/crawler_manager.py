from typing import List, Dict
from sqlalchemy.orm import Session
from app.models.movie import Movie
from app.crawlers.douban_crawler import DoubanCrawler
from app.crawlers.maoyan_crawler import MaoyanCrawler


class CrawlerManager:
    def __init__(self):
        self.douban_crawler = DoubanCrawler()
        self.maoyan_crawler = MaoyanCrawler()
    
    def crawl_movies(self, db: Session) -> int:
        movies = self.douban_crawler.get_nowplaying_movies()
        
        if not movies:
            print("豆瓣爬取失败，尝试猫眼...")
            movies = self.maoyan_crawler.get_nowplaying_movies()
        
        if not movies:
            print("所有爬虫都失败了")
            return 0
        
        saved_count = 0
        for movie_data in movies:
            try:
                existing = db.query(Movie).filter(
                    Movie.source == movie_data['source'],
                    Movie.source_id == movie_data['source_id']
                ).first()
                
                if existing:
                    continue
                
                movie = Movie(
                    title=movie_data.get('title', ''),
                    poster_url=movie_data.get('poster_url', ''),
                    director=movie_data.get('director', ''),
                    actors=movie_data.get('actors', ''),
                    genre=movie_data.get('genre', ''),
                    release_date=movie_data.get('release', ''),
                    duration=self._parse_duration(movie_data.get('duration', '')),
                    synopsis=movie_data.get('synopsis', ''),
                    source=movie_data.get('source', ''),
                    source_id=movie_data.get('source_id', '')
                )
                
                db.add(movie)
                saved_count += 1
            except Exception as e:
                print(f"保存电影失败: {str(e)}")
                continue
        
        db.commit()
        return saved_count
    
    def _parse_duration(self, duration_str: str) -> int:
        if not duration_str:
            return None
        
        try:
            if '分钟' in duration_str:
                return int(duration_str.replace('分钟', '').strip())
            elif 'min' in duration_str.lower():
                return int(duration_str.lower().replace('min', '').strip())
            else:
                return int(duration_str.strip())
        except:
            return None
