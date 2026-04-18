from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from app.crawlers.base_crawler import BaseCrawler


class MaoyanCrawler(BaseCrawler):
    def __init__(self):
        super().__init__()
        self.base_url = "https://maoyan.com"
        self.films_url = f"{self.base_url}/films"
    
    def get_nowplaying_movies(self) -> List[Dict]:
        html = self.fetch_page(self.films_url)
        if not html:
            return []
        
        return self.parse_movie_data(html)
    
    def parse_movie_data(self, html: str) -> List[Dict]:
        soup = BeautifulSoup(html, 'lxml')
        movies = []
        
        movie_items = soup.find_all('div', class_='movie-item')
        
        for item in movie_items:
            try:
                movie_data = {}
                
                title_tag = item.find('span', class_='name')
                if title_tag:
                    movie_data['title'] = title_tag.text.strip()
                
                score_tag = item.find('span', class_='score')
                if score_tag:
                    movie_data['score'] = score_tag.text.strip()
                
                poster_img = item.find('img')
                if poster_img:
                    movie_data['poster_url'] = poster_img.get('data-src', '') or poster_img.get('src', '')
                
                link_tag = item.find('a')
                if link_tag:
                    href = link_tag.get('href', '')
                    movie_data['source_id'] = href.split('/')[-1] if href else ''
                
                movie_data['source'] = 'maoyan'
                
                if movie_data.get('title'):
                    movies.append(movie_data)
            except Exception as e:
                print(f"解析电影数据失败: {str(e)}")
                continue
        
        return movies
