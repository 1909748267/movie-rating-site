from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup
import time
import random


class BaseCrawler(ABC):
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
    
    def fetch_page(self, url: str, max_retries: int = 3) -> Optional[str]:
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                time.sleep(random.uniform(1, 3))
                return response.text
            except Exception as e:
                print(f"尝试 {attempt + 1}/{max_retries} 失败: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(2)
                else:
                    return None
        return None
    
    @abstractmethod
    def get_nowplaying_movies(self) -> List[Dict]:
        pass
    
    @abstractmethod
    def parse_movie_data(self, html: str) -> List[Dict]:
        pass
