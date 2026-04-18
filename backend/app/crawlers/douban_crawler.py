from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from app.crawlers.base_crawler import BaseCrawler


class DoubanCrawler(BaseCrawler):
    def __init__(self):
        super().__init__()
        self.base_url = "https://movie.douban.com"
        self.nowplaying_url = f"{self.base_url}/cinema/nowplaying/"
    
    def get_nowplaying_movies(self) -> List[Dict]:
        html = self.fetch_page(self.nowplaying_url)
        if not html:
            return []
        
        return self.parse_movie_data(html)
    
    def parse_movie_data(self, html: str) -> List[Dict]:
        soup = BeautifulSoup(html, 'lxml')
        movies = []
        
        nowplaying_div = soup.find('div', id='nowplaying')
        if not nowplaying_div:
            return movies
        
        movie_items = nowplaying_div.find_all('li', class_='list-item')
        
        for item in movie_items:
            try:
                movie_data = {
                    'title': item.get('data-title', ''),
                    'score': item.get('data-score', '0'),
                    'release': item.get('data-release', ''),
                    'duration': item.get('data-duration', ''),
                    'region': item.get('data-region', ''),
                    'director': item.get('data-director', ''),
                    'actors': item.get('data-actors', ''),
                    'source': 'douban',
                    'source_id': item.get('id', '')
                }
                
                poster_img = item.find('img')
                if poster_img:
                    movie_data['poster_url'] = poster_img.get('src', '')
                
                if movie_data['title']:
                    movies.append(movie_data)
            except Exception as e:
                print(f"解析电影数据失败: {str(e)}")
                continue
        
        return movies
