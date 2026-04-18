# 电影评分网站实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 从零开发一个电影评分网站，支持用户注册登录、电影浏览、评分评论和数据爬取功能

**Architecture:** 经典三层架构，前后端分离。后端使用FastAPI + SQLAlchemy + SQLite，前端使用React + Vite，数据爬取使用requests + BeautifulSoup

**Tech Stack:** 
- 后端: FastAPI 0.104+, SQLAlchemy 2.0, bcrypt, Pydantic 2.0, pytest
- 前端: React 18, Vite 5, React Router 6, Axios, Vitest
- 数据库: SQLite 3
- 爬虫: requests, BeautifulSoup4

---

## 阶段一：项目初始化

### Task 1: 创建项目根目录结构

**Files:**
- Create: `backend/` directory
- Create: `frontend/` directory
- Create: `.gitignore`

- [ ] **Step 1: 创建项目根目录结构**

Run:
```bash
mkdir -p backend frontend
```

- [ ] **Step 2: 创建.gitignore文件**

Create `.gitignore`:
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
venv/
ENV/
env/

# Node
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.pnpm-debug.log*

# Build
frontend/dist/
frontend/build/

# Environment
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Database
*.db
*.sqlite
*.sqlite3

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Test
.coverage
htmlcov/
.pytest_cache/
coverage/
.nyc_output/

# Logs
logs/
*.log
```

- [ ] **Step 3: 提交项目结构**

Run:
```bash
git add .gitignore backend frontend
git commit -m "chore: 初始化项目结构"
```

---

### Task 2: 初始化后端项目

**Files:**
- Create: `backend/requirements.txt`
- Create: `backend/app/__init__.py`
- Create: `backend/app/config.py`
- Create: `backend/app/database.py`

- [ ] **Step 1: 创建requirements.txt**

Create `backend/requirements.txt`:
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
pydantic-settings==2.1.0
bcrypt==4.1.1
python-jose[cryptography]==3.3.0
requests==2.31.0
beautifulsoup4==4.12.2
lxml==4.9.3
pytest==7.4.3
pytest-cov==4.1.0
pytest-asyncio==0.21.1
httpx==0.25.2
```

- [ ] **Step 2: 创建app包**

Run:
```bash
mkdir -p backend/app
touch backend/app/__init__.py
```

- [ ] **Step 3: 创建配置文件**

Create `backend/app/config.py`:
```python
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./database.db"
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_days: int = 7

    class Config:
        env_file = ".env"


settings = Settings()
```

- [ ] **Step 4: 创建数据库连接文件**

Create `backend/app/database.py`:
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

- [ ] **Step 5: 提交后端初始化**

Run:
```bash
git add backend/
git commit -m "chore: 初始化后端项目配置"
```

---

### Task 3: 初始化前端项目

**Files:**
- Create: `frontend/package.json`
- Create: `frontend/vite.config.js`
- Create: `frontend/index.html`
- Create: `frontend/src/main.jsx`
- Create: `frontend/src/App.jsx`
- Create: `frontend/src/index.css`

- [ ] **Step 1: 创建package.json**

Create `frontend/package.json`:
```json
{
  "name": "movie-rating-website-frontend",
  "private": true,
  "version": "0.0.1",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "test": "vitest",
    "test:coverage": "vitest --coverage"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "axios": "^1.6.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.37",
    "@types/react-dom": "^18.2.15",
    "@vitejs/plugin-react": "^4.2.0",
    "@testing-library/react": "^14.1.0",
    "@testing-library/jest-dom": "^6.1.0",
    "jsdom": "^22.1.0",
    "vite": "^5.0.0",
    "vitest": "^1.0.0",
    "@vitest/coverage-v8": "^1.0.0",
    "msw": "^2.0.0"
  }
}
```

- [ ] **Step 2: 创建vite.config.js**

Create `frontend/vite.config.js`:
```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  },
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.js',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      lines: 85,
      branches: 85,
      functions: 85,
      statements: 85
    }
  }
})
```

- [ ] **Step 3: 创建index.html**

Create `frontend/index.html`:
```html
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>电影评分网站</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
```

- [ ] **Step 4: 创建src目录结构**

Run:
```bash
mkdir -p frontend/src/components frontend/src/pages frontend/src/services frontend/src/utils frontend/src/test
```

- [ ] **Step 5: 创建main.jsx**

Create `frontend/src/main.jsx`:
```jsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
```

- [ ] **Step 6: 创建App.jsx**

Create `frontend/src/App.jsx`:
```jsx
import React from 'react'

function App() {
  return (
    <div className="App">
      <h1>电影评分网站</h1>
    </div>
  )
}

export default App
```

- [ ] **Step 7: 创建index.css**

Create `frontend/src/index.css`:
```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #f5f5f5;
}

.App {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
```

- [ ] **Step 8: 创建测试配置文件**

Create `frontend/src/test/setup.js`:
```javascript
import '@testing-library/jest-dom'
```

- [ ] **Step 9: 提交前端初始化**

Run:
```bash
git add frontend/
git commit -m "chore: 初始化前端项目配置"
```

---

## 阶段二：数据库设计与实现

### Task 4: 创建用户数据模型

**Files:**
- Create: `backend/app/models/__init__.py`
- Create: `backend/app/models/user.py`
- Test: `backend/tests/test_models/test_user.py`

- [ ] **Step 1: 创建models包**

Run:
```bash
mkdir -p backend/app/models backend/tests/test_models
touch backend/app/models/__init__.py backend/tests/test_models/__init__.py
```

- [ ] **Step 2: 编写用户模型测试**

Create `backend/tests/test_models/test_user.py`:
```python
import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models.user import User


@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    SessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()


def test_create_user(db):
    user = User(
        email="test@example.com",
        username="testuser",
        password_hash="hashed_password"
    )
    db.add(user)
    db.commit()
    
    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.username == "testuser"
    assert user.password_hash == "hashed_password"
    assert isinstance(user.created_at, datetime)
    assert isinstance(user.updated_at, datetime)


def test_user_email_unique(db):
    user1 = User(
        email="test@example.com",
        username="user1",
        password_hash="hash1"
    )
    db.add(user1)
    db.commit()
    
    user2 = User(
        email="test@example.com",
        username="user2",
        password_hash="hash2"
    )
    db.add(user2)
    
    with pytest.raises(Exception):
        db.commit()


def test_user_username_unique(db):
    user1 = User(
        email="user1@example.com",
        username="testuser",
        password_hash="hash1"
    )
    db.add(user1)
    db.commit()
    
    user2 = User(
        email="user2@example.com",
        username="testuser",
        password_hash="hash2"
    )
    db.add(user2)
    
    with pytest.raises(Exception):
        db.commit()
```

- [ ] **Step 3: 运行测试确认失败**

Run:
```bash
cd backend && python -m pytest tests/test_models/test_user.py -v
```

Expected: FAIL with "ModuleNotFoundError: No module named 'app.models.user'"

- [ ] **Step 4: 创建用户模型**

Create `backend/app/models/user.py`:
```python
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

- [ ] **Step 5: 运行测试确认通过**

Run:
```bash
cd backend && python -m pytest tests/test_models/test_user.py -v
```

Expected: PASS

- [ ] **Step 6: 提交用户模型**

Run:
```bash
git add backend/app/models/ backend/tests/test_models/
git commit -m "feat: 添加用户数据模型"
```

---

### Task 5: 创建电影数据模型

**Files:**
- Create: `backend/app/models/movie.py`
- Test: `backend/tests/test_models/test_movie.py`

- [ ] **Step 1: 编写电影模型测试**

Create `backend/tests/test_models/test_movie.py`:
```python
import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models.movie import Movie


@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    SessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()


def test_create_movie(db):
    movie = Movie(
        title="测试电影",
        poster_url="https://example.com/poster.jpg",
        director="测试导演",
        actors="演员1, 演员2",
        genre="动作",
        release_date="2026-04-18",
        duration=120,
        synopsis="这是一部测试电影",
        source="douban",
        source_id="12345"
    )
    db.add(movie)
    db.commit()
    
    assert movie.id is not None
    assert movie.title == "测试电影"
    assert movie.poster_url == "https://example.com/poster.jpg"
    assert movie.director == "测试导演"
    assert movie.actors == "演员1, 演员2"
    assert movie.genre == "动作"
    assert movie.release_date == "2026-04-18"
    assert movie.duration == 120
    assert movie.synopsis == "这是一部测试电影"
    assert movie.source == "douban"
    assert movie.source_id == "12345"
    assert isinstance(movie.created_at, datetime)


def test_movie_optional_fields(db):
    movie = Movie(
        title="最小电影",
        source="maoyan",
        source_id="67890"
    )
    db.add(movie)
    db.commit()
    
    assert movie.id is not None
    assert movie.title == "最小电影"
    assert movie.poster_url is None
    assert movie.director is None
    assert movie.actors is None
    assert movie.genre is None
    assert movie.release_date is None
    assert movie.duration is None
    assert movie.synopsis is None
```

- [ ] **Step 2: 运行测试确认失败**

Run:
```bash
cd backend && python -m pytest tests/test_models/test_movie.py -v
```

Expected: FAIL with "ModuleNotFoundError: No module named 'app.models.movie'"

- [ ] **Step 3: 创建电影模型**

Create `backend/app/models/movie.py`:
```python
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
```

- [ ] **Step 4: 运行测试确认通过**

Run:
```bash
cd backend && python -m pytest tests/test_models/test_movie.py -v
```

Expected: PASS

- [ ] **Step 5: 提交电影模型**

Run:
```bash
git add backend/app/models/movie.py backend/tests/test_models/test_movie.py
git commit -m "feat: 添加电影数据模型"
```

---

### Task 6: 创建评分数据模型

**Files:**
- Create: `backend/app/models/rating.py`
- Test: `backend/tests/test_models/test_rating.py`

- [ ] **Step 1: 编写评分模型测试**

Create `backend/tests/test_models/test_rating.py`:
```python
import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models.user import User
from app.models.movie import Movie
from app.models.rating import Rating


@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    SessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()


@pytest.fixture
def test_user(db):
    user = User(
        email="test@example.com",
        username="testuser",
        password_hash="hashed_password"
    )
    db.add(user)
    db.commit()
    return user


@pytest.fixture
def test_movie(db):
    movie = Movie(
        title="测试电影",
        source="douban",
        source_id="12345"
    )
    db.add(movie)
    db.commit()
    return movie


def test_create_rating(db, test_user, test_movie):
    rating = Rating(
        user_id=test_user.id,
        movie_id=test_movie.id,
        score=5
    )
    db.add(rating)
    db.commit()
    
    assert rating.id is not None
    assert rating.user_id == test_user.id
    assert rating.movie_id == test_movie.id
    assert rating.score == 5
    assert isinstance(rating.created_at, datetime)
    assert isinstance(rating.updated_at, datetime)


def test_rating_score_range(db, test_user, test_movie):
    rating = Rating(
        user_id=test_user.id,
        movie_id=test_movie.id,
        score=3
    )
    db.add(rating)
    db.commit()
    
    assert 1 <= rating.score <= 5


def test_rating_unique_per_user_movie(db, test_user, test_movie):
    rating1 = Rating(
        user_id=test_user.id,
        movie_id=test_movie.id,
        score=4
    )
    db.add(rating1)
    db.commit()
    
    rating2 = Rating(
        user_id=test_user.id,
        movie_id=test_movie.id,
        score=5
    )
    db.add(rating2)
    
    with pytest.raises(Exception):
        db.commit()
```

- [ ] **Step 2: 运行测试确认失败**

Run:
```bash
cd backend && python -m pytest tests/test_models/test_rating.py -v
```

Expected: FAIL with "ModuleNotFoundError: No module named 'app.models.rating'"

- [ ] **Step 3: 创建评分模型**

Create `backend/app/models/rating.py`:
```python
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    score = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint('user_id', 'movie_id', name='unique_user_movie_rating'),
    )

    user = relationship("User", backref="ratings")
    movie = relationship("Movie", backref="ratings")
```

- [ ] **Step 4: 运行测试确认通过**

Run:
```bash
cd backend && python -m pytest tests/test_models/test_rating.py -v
```

Expected: PASS

- [ ] **Step 5: 提交评分模型**

Run:
```bash
git add backend/app/models/rating.py backend/tests/test_models/test_rating.py
git commit -m "feat: 添加评分数据模型"
```

---

### Task 7: 创建评论数据模型

**Files:**
- Create: `backend/app/models/comment.py`
- Test: `backend/tests/test_models/test_comment.py`

- [ ] **Step 1: 编写评论模型测试**

Create `backend/tests/test_models/test_comment.py`:
```python
import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models.user import User
from app.models.movie import Movie
from app.models.comment import Comment


@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    SessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()


@pytest.fixture
def test_user(db):
    user = User(
        email="test@example.com",
        username="testuser",
        password_hash="hashed_password"
    )
    db.add(user)
    db.commit()
    return user


@pytest.fixture
def test_movie(db):
    movie = Movie(
        title="测试电影",
        source="douban",
        source_id="12345"
    )
    db.add(movie)
    db.commit()
    return movie


def test_create_comment(db, test_user, test_movie):
    comment = Comment(
        user_id=test_user.id,
        movie_id=test_movie.id,
        content="这是一条测试评论"
    )
    db.add(comment)
    db.commit()
    
    assert comment.id is not None
    assert comment.user_id == test_user.id
    assert comment.movie_id == test_movie.id
    assert comment.content == "这是一条测试评论"
    assert isinstance(comment.created_at, datetime)
    assert isinstance(comment.updated_at, datetime)


def test_comment_multiple_per_user_movie(db, test_user, test_movie):
    comment1 = Comment(
        user_id=test_user.id,
        movie_id=test_movie.id,
        content="第一条评论"
    )
    db.add(comment1)
    
    comment2 = Comment(
        user_id=test_user.id,
        movie_id=test_movie.id,
        content="第二条评论"
    )
    db.add(comment2)
    db.commit()
    
    assert comment1.id != comment2.id
    assert comment1.content == "第一条评论"
    assert comment2.content == "第二条评论"
```

- [ ] **Step 2: 运行测试确认失败**

Run:
```bash
cd backend && python -m pytest tests/test_models/test_comment.py -v
```

Expected: FAIL with "ModuleNotFoundError: No module named 'app.models.comment'"

- [ ] **Step 3: 创建评论模型**

Create `backend/app/models/comment.py`:
```python
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", backref="comments")
    movie = relationship("Movie", backref="comments")
```

- [ ] **Step 4: 运行测试确认通过**

Run:
```bash
cd backend && python -m pytest tests/test_models/test_comment.py -v
```

Expected: PASS

- [ ] **Step 5: 提交评论模型**

Run:
```bash
git add backend/app/models/comment.py backend/tests/test_models/test_comment.py
git commit -m "feat: 添加评论数据模型"
```

---

### Task 8: 更新models包导出

**Files:**
- Modify: `backend/app/models/__init__.py`

- [ ] **Step 1: 更新models包导出**

Modify `backend/app/models/__init__.py`:
```python
from app.models.user import User
from app.models.movie import Movie
from app.models.rating import Rating
from app.models.comment import Comment

__all__ = ["User", "Movie", "Rating", "Comment"]
```

- [ ] **Step 2: 提交models包更新**

Run:
```bash
git add backend/app/models/__init__.py
git commit -m "refactor: 更新models包导出"
```

---

## 阶段三：后端核心功能

### Task 9: 创建Pydantic schemas

**Files:**
- Create: `backend/app/schemas/__init__.py`
- Create: `backend/app/schemas/user.py`
- Create: `backend/app/schemas/movie.py`
- Create: `backend/app/schemas/rating.py`
- Create: `backend/app/schemas/comment.py`
- Test: `backend/tests/test_schemas/`

- [ ] **Step 1: 创建schemas包**

Run:
```bash
mkdir -p backend/app/schemas backend/tests/test_schemas
touch backend/app/schemas/__init__.py backend/tests/test_schemas/__init__.py
```

- [ ] **Step 2: 编写用户schema测试**

Create `backend/tests/test_schemas/test_user.py`:
```python
import pytest
from pydantic import ValidationError
from app.schemas.user import UserCreate, UserLogin, UserResponse


def test_user_create_valid():
    user = UserCreate(
        email="test@example.com",
        username="testuser",
        password="password123",
        confirm_password="password123"
    )
    assert user.email == "test@example.com"
    assert user.username == "testuser"
    assert user.password == "password123"


def test_user_create_password_mismatch():
    with pytest.raises(ValidationError):
        UserCreate(
            email="test@example.com",
            username="testuser",
            password="password123",
            confirm_password="password456"
        )


def test_user_create_invalid_email():
    with pytest.raises(ValidationError):
        UserCreate(
            email="invalid-email",
            username="testuser",
            password="password123",
            confirm_password="password123"
        )


def test_user_login_valid():
    user = UserLogin(
        email="test@example.com",
        password="password123"
    )
    assert user.email == "test@example.com"
    assert user.password == "password123"


def test_user_response():
    user = UserResponse(
        id=1,
        email="test@example.com",
        username="testuser"
    )
    assert user.id == 1
    assert user.email == "test@example.com"
    assert user.username == "testuser"
```

- [ ] **Step 3: 创建用户schema**

Create `backend/app/schemas/user.py`:
```python
from pydantic import BaseModel, EmailStr, field_validator


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    confirm_password: str

    @field_validator('confirm_password')
    @classmethod
    def passwords_match(cls, v, info):
        if 'password' in info.data and v != info.data['password']:
            raise ValueError('密码不匹配')
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    username: str

    class Config:
        from_attributes = True


class PasswordUpdate(BaseModel):
    old_password: str
    new_password: str
    confirm_password: str

    @field_validator('confirm_password')
    @classmethod
    def passwords_match(cls, v, info):
        if 'new_password' in info.data and v != info.data['new_password']:
            raise ValueError('密码不匹配')
        return v
```

- [ ] **Step 4: 创建电影schema**

Create `backend/app/schemas/movie.py`:
```python
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
```

- [ ] **Step 5: 创建评分schema**

Create `backend/app/schemas/rating.py`:
```python
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
```

- [ ] **Step 6: 创建评论schema**

Create `backend/app/schemas/comment.py`:
```python
from pydantic import BaseModel
from datetime import datetime


class CommentCreate(BaseModel):
    content: str


class CommentUpdate(BaseModel):
    content: str


class CommentResponse(BaseModel):
    id: int
    user_id: int
    username: str
    content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CommentListResponse(BaseModel):
    comments: list[CommentResponse]
    total: int
    page: int
    page_size: int
```

- [ ] **Step 7: 运行schema测试**

Run:
```bash
cd backend && python -m pytest tests/test_schemas/ -v
```

Expected: PASS

- [ ] **Step 8: 提交schemas**

Run:
```bash
git add backend/app/schemas/ backend/tests/test_schemas/
git commit -m "feat: 添加Pydantic schemas"
```

---

### Task 10: 创建认证工具函数

**Files:**
- Create: `backend/app/utils/__init__.py`
- Create: `backend/app/utils/auth.py`
- Create: `backend/app/utils/response.py`
- Test: `backend/tests/test_utils/`

- [ ] **Step 1: 创建utils包**

Run:
```bash
mkdir -p backend/app/utils backend/tests/test_utils
touch backend/app/utils/__init__.py backend/tests/test_utils/__init__.py
```

- [ ] **Step 2: 编写认证工具测试**

Create `backend/tests/test_utils/test_auth.py`:
```python
import pytest
from app.utils.auth import hash_password, verify_password, create_token, verify_token


def test_hash_password():
    password = "test_password"
    hashed = hash_password(password)
    
    assert hashed != password
    assert len(hashed) > 0
    assert hashed.startswith('$2b$')


def test_verify_password():
    password = "test_password"
    hashed = hash_password(password)
    
    assert verify_password(password, hashed) is True
    assert verify_password("wrong_password", hashed) is False


def test_create_and_verify_token():
    data = {"user_id": 1, "email": "test@example.com"}
    token = create_token(data)
    
    assert isinstance(token, str)
    assert len(token) > 0
    
    payload = verify_token(token)
    assert payload["user_id"] == 1
    assert payload["email"] == "test@example.com"


def test_verify_invalid_token():
    invalid_token = "invalid_token_string"
    payload = verify_token(invalid_token)
    
    assert payload is None
```

- [ ] **Step 3: 创建认证工具**

Create `backend/app/utils/auth.py`:
```python
import bcrypt
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.config import settings


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )


def create_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.access_token_expire_days)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def verify_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except JWTError:
        return None
```

- [ ] **Step 4: 创建响应工具**

Create `backend/app/utils/response.py`:
```python
from typing import Any, Optional


def success_response(data: Any = None, message: str = "操作成功") -> dict:
    response = {
        "code": "SUCCESS",
        "message": message
    }
    if data is not None:
        response["data"] = data
    return response


def error_response(code: str, message: str) -> dict:
    return {
        "code": code,
        "message": message
    }
```

- [ ] **Step 5: 运行工具测试**

Run:
```bash
cd backend && python -m pytest tests/test_utils/ -v
```

Expected: PASS

- [ ] **Step 6: 提交工具函数**

Run:
```bash
git add backend/app/utils/ backend/tests/test_utils/
git commit -m "feat: 添加认证和响应工具函数"
```

---

### Task 11: 创建用户服务层

**Files:**
- Create: `backend/app/services/__init__.py`
- Create: `backend/app/services/auth_service.py`
- Create: `backend/app/services/user_service.py`
- Test: `backend/tests/test_services/`

- [ ] **Step 1: 创建services包**

Run:
```bash
mkdir -p backend/app/services backend/tests/test_services
touch backend/app/services/__init__.py backend/tests/test_services/__init__.py
```

- [ ] **Step 2: 编写认证服务测试**

Create `backend/tests/test_services/test_auth_service.py`:
```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.services.auth_service import AuthService
from app.schemas.user import UserCreate, UserLogin


@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    SessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()


def test_register_user(db):
    user_data = UserCreate(
        email="test@example.com",
        username="testuser",
        password="password123",
        confirm_password="password123"
    )
    
    user = AuthService.register_user(db, user_data)
    
    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.username == "testuser"
    assert user.password_hash != "password123"


def test_register_duplicate_email(db):
    user_data1 = UserCreate(
        email="test@example.com",
        username="user1",
        password="password123",
        confirm_password="password123"
    )
    AuthService.register_user(db, user_data1)
    
    user_data2 = UserCreate(
        email="test@example.com",
        username="user2",
        password="password123",
        confirm_password="password123"
    )
    
    with pytest.raises(ValueError, match="邮箱已被注册"):
        AuthService.register_user(db, user_data2)


def test_register_duplicate_username(db):
    user_data1 = UserCreate(
        email="user1@example.com",
        username="testuser",
        password="password123",
        confirm_password="password123"
    )
    AuthService.register_user(db, user_data1)
    
    user_data2 = UserCreate(
        email="user2@example.com",
        username="testuser",
        password="password123",
        confirm_password="password123"
    )
    
    with pytest.raises(ValueError, match="用户名已被使用"):
        AuthService.register_user(db, user_data2)


def test_login_user(db):
    user_data = UserCreate(
        email="test@example.com",
        username="testuser",
        password="password123",
        confirm_password="password123"
    )
    AuthService.register_user(db, user_data)
    
    login_data = UserLogin(
        email="test@example.com",
        password="password123"
    )
    
    token, user = AuthService.login_user(db, login_data)
    
    assert token is not None
    assert user.email == "test@example.com"


def test_login_wrong_password(db):
    user_data = UserCreate(
        email="test@example.com",
        username="testuser",
        password="password123",
        confirm_password="password123"
    )
    AuthService.register_user(db, user_data)
    
    login_data = UserLogin(
        email="test@example.com",
        password="wrongpassword"
    )
    
    with pytest.raises(ValueError, match="密码错误"):
        AuthService.login_user(db, login_data)


def test_login_nonexistent_user(db):
    login_data = UserLogin(
        email="nonexistent@example.com",
        password="password123"
    )
    
    with pytest.raises(ValueError, match="用户不存在"):
        AuthService.login_user(db, login_data)
```

- [ ] **Step 3: 创建认证服务**

Create `backend/app/services/auth_service.py`:
```python
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.utils.auth import hash_password, verify_password, create_token


class AuthService:
    @staticmethod
    def register_user(db: Session, user_data: UserCreate) -> User:
        existing_email = db.query(User).filter(User.email == user_data.email).first()
        if existing_email:
            raise ValueError("邮箱已被注册")
        
        existing_username = db.query(User).filter(User.username == user_data.username).first()
        if existing_username:
            raise ValueError("用户名已被使用")
        
        hashed_password = hash_password(user_data.password)
        
        user = User(
            email=user_data.email,
            username=user_data.username,
            password_hash=hashed_password
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return user

    @staticmethod
    def login_user(db: Session, login_data: UserLogin) -> tuple[str, User]:
        user = db.query(User).filter(User.email == login_data.email).first()
        
        if not user:
            raise ValueError("用户不存在")
        
        if not verify_password(login_data.password, user.password_hash):
            raise ValueError("密码错误")
        
        token = create_token({"user_id": user.id, "email": user.email})
        
        return token, user
```

- [ ] **Step 4: 编写用户服务测试**

Create `backend/tests/test_services/test_user_service.py`:
```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models.user import User
from app.services.user_service import UserService
from app.schemas.user import PasswordUpdate
from app.utils.auth import hash_password, verify_password


@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    SessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()


@pytest.fixture
def test_user(db):
    user = User(
        email="test@example.com",
        username="testuser",
        password_hash=hash_password("oldpassword")
    )
    db.add(user)
    db.commit()
    return user


def test_get_user_by_id(db, test_user):
    user = UserService.get_user_by_id(db, test_user.id)
    
    assert user is not None
    assert user.id == test_user.id
    assert user.email == test_user.email


def test_get_user_by_id_not_found(db):
    user = UserService.get_user_by_id(db, 999)
    
    assert user is None


def test_update_password(db, test_user):
    password_data = PasswordUpdate(
        old_password="oldpassword",
        new_password="newpassword123",
        confirm_password="newpassword123"
    )
    
    UserService.update_password(db, test_user.id, password_data)
    
    db.refresh(test_user)
    assert verify_password("newpassword123", test_user.password_hash)


def test_update_password_wrong_old(db, test_user):
    password_data = PasswordUpdate(
        old_password="wrongpassword",
        new_password="newpassword123",
        confirm_password="newpassword123"
    )
    
    with pytest.raises(ValueError, match="原密码错误"):
        UserService.update_password(db, test_user.id, password_data)
```

- [ ] **Step 5: 创建用户服务**

Create `backend/app/services/user_service.py`:
```python
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import PasswordUpdate
from app.utils.auth import hash_password, verify_password


class UserService:
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User | None:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def update_password(db: Session, user_id: int, password_data: PasswordUpdate) -> None:
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise ValueError("用户不存在")
        
        if not verify_password(password_data.old_password, user.password_hash):
            raise ValueError("原密码错误")
        
        user.password_hash = hash_password(password_data.new_password)
        db.commit()
```

- [ ] **Step 6: 运行服务测试**

Run:
```bash
cd backend && python -m pytest tests/test_services/ -v
```

Expected: PASS

- [ ] **Step 7: 提交服务层**

Run:
```bash
git add backend/app/services/ backend/tests/test_services/
git commit -m "feat: 添加用户认证和用户服务"
```

---

### Task 12: 创建电影服务层

**Files:**
- Create: `backend/app/services/movie_service.py`
- Test: `backend/tests/test_services/test_movie_service.py`

- [ ] **Step 1: 编写电影服务测试**

Create `backend/tests/test_services/test_movie_service.py`:
```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models.movie import Movie
from app.models.rating import Rating
from app.models.user import User
from app.services.movie_service import MovieService


@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    SessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()


@pytest.fixture
def test_movies(db):
    movies = []
    for i in range(5):
        movie = Movie(
            title=f"测试电影{i+1}",
            director=f"导演{i+1}",
            source="douban",
            source_id=str(i+1)
        )
        db.add(movie)
        movies.append(movie)
    db.commit()
    return movies


@pytest.fixture
def test_user(db):
    user = User(
        email="test@example.com",
        username="testuser",
        password_hash="hashed_password"
    )
    db.add(user)
    db.commit()
    return user


def test_get_movies(db, test_movies):
    movies, total = MovieService.get_movies(db, page=1, page_size=10)
    
    assert len(movies) == 5
    assert total == 5


def test_get_movies_pagination(db, test_movies):
    movies, total = MovieService.get_movies(db, page=1, page_size=2)
    
    assert len(movies) == 2
    assert total == 5


def test_get_movie_by_id(db, test_movies):
    movie = MovieService.get_movie_by_id(db, test_movies[0].id)
    
    assert movie is not None
    assert movie.id == test_movies[0].id
    assert movie.title == test_movies[0].title


def test_get_movie_by_id_not_found(db):
    movie = MovieService.get_movie_by_id(db, 999)
    
    assert movie is None


def test_get_movie_rating_stats(db, test_movies, test_user):
    movie = test_movies[0]
    
    rating1 = Rating(user_id=test_user.id, movie_id=movie.id, score=4)
    db.add(rating1)
    
    user2 = User(email="user2@example.com", username="user2", password_hash="hash")
    db.add(user2)
    db.commit()
    
    rating2 = Rating(user_id=user2.id, movie_id=movie.id, score=5)
    db.add(rating2)
    db.commit()
    
    avg_score, count = MovieService.get_movie_rating_stats(db, movie.id)
    
    assert avg_score == 4.5
    assert count == 2


def test_get_movie_rating_stats_no_ratings(db, test_movies):
    avg_score, count = MovieService.get_movie_rating_stats(db, test_movies[0].id)
    
    assert avg_score == 0
    assert count == 0
```

- [ ] **Step 2: 创建电影服务**

Create `backend/app/services/movie_service.py`:
```python
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.movie import Movie
from app.models.rating import Rating


class MovieService:
    @staticmethod
    def get_movies(db: Session, page: int = 1, page_size: int = 20) -> tuple[list[Movie], int]:
        offset = (page - 1) * page_size
        query = db.query(Movie)
        
        total = query.count()
        movies = query.offset(offset).limit(page_size).all()
        
        return movies, total

    @staticmethod
    def get_movie_by_id(db: Session, movie_id: int) -> Movie | None:
        return db.query(Movie).filter(Movie.id == movie_id).first()

    @staticmethod
    def get_movie_rating_stats(db: Session, movie_id: int) -> tuple[float, int]:
        result = db.query(
            func.avg(Rating.score).label('avg_score'),
            func.count(Rating.id).label('count')
        ).filter(Rating.movie_id == movie_id).first()
        
        avg_score = float(result.avg_score) if result.avg_score else 0.0
        count = result.count
        
        return avg_score, count
```

- [ ] **Step 3: 运行电影服务测试**

Run:
```bash
cd backend && python -m pytest tests/test_services/test_movie_service.py -v
```

Expected: PASS

- [ ] **Step 4: 提交电影服务**

Run:
```bash
git add backend/app/services/movie_service.py backend/tests/test_services/test_movie_service.py
git commit -m "feat: 添加电影服务"
```

---

### Task 13: 创建评分服务层

**Files:**
- Create: `backend/app/services/rating_service.py`
- Test: `backend/tests/test_services/test_rating_service.py`

- [ ] **Step 1: 编写评分服务测试**

Create `backend/tests/test_services/test_rating_service.py`:
```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models.user import User
from app.models.movie import Movie
from app.models.rating import Rating
from app.services.rating_service import RatingService
from app.schemas.rating import RatingCreate


@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    SessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()


@pytest.fixture
def test_user(db):
    user = User(
        email="test@example.com",
        username="testuser",
        password_hash="hashed_password"
    )
    db.add(user)
    db.commit()
    return user


@pytest.fixture
def test_movie(db):
    movie = Movie(
        title="测试电影",
        source="douban",
        source_id="12345"
    )
    db.add(movie)
    db.commit()
    return movie


def test_create_rating(db, test_user, test_movie):
    rating_data = RatingCreate(score=5)
    
    rating = RatingService.create_rating(db, test_user.id, test_movie.id, rating_data)
    
    assert rating.id is not None
    assert rating.user_id == test_user.id
    assert rating.movie_id == test_movie.id
    assert rating.score == 5


def test_create_rating_already_exists(db, test_user, test_movie):
    rating_data = RatingCreate(score=5)
    RatingService.create_rating(db, test_user.id, test_movie.id, rating_data)
    
    with pytest.raises(ValueError, match="您已经评分过该电影"):
        RatingService.create_rating(db, test_user.id, test_movie.id, rating_data)


def test_update_rating(db, test_user, test_movie):
    rating_data = RatingCreate(score=5)
    RatingService.create_rating(db, test_user.id, test_movie.id, rating_data)
    
    update_data = RatingCreate(score=4)
    rating = RatingService.update_rating(db, test_user.id, test_movie.id, update_data)
    
    assert rating.score == 4


def test_update_rating_not_exists(db, test_user, test_movie):
    update_data = RatingCreate(score=4)
    
    with pytest.raises(ValueError, match="您还没有评分该电影"):
        RatingService.update_rating(db, test_user.id, test_movie.id, update_data)


def test_get_user_rating(db, test_user, test_movie):
    rating_data = RatingCreate(score=5)
    RatingService.create_rating(db, test_user.id, test_movie.id, rating_data)
    
    rating = RatingService.get_user_rating(db, test_user.id, test_movie.id)
    
    assert rating is not None
    assert rating.score == 5


def test_get_user_rating_not_exists(db, test_user, test_movie):
    rating = RatingService.get_user_rating(db, test_user.id, test_movie.id)
    
    assert rating is None
```

- [ ] **Step 2: 创建评分服务**

Create `backend/app/services/rating_service.py`:
```python
from sqlalchemy.orm import Session
from app.models.rating import Rating
from app.schemas.rating import RatingCreate


class RatingService:
    @staticmethod
    def create_rating(db: Session, user_id: int, movie_id: int, rating_data: RatingCreate) -> Rating:
        existing = db.query(Rating).filter(
            Rating.user_id == user_id,
            Rating.movie_id == movie_id
        ).first()
        
        if existing:
            raise ValueError("您已经评分过该电影")
        
        rating = Rating(
            user_id=user_id,
            movie_id=movie_id,
            score=rating_data.score
        )
        
        db.add(rating)
        db.commit()
        db.refresh(rating)
        
        return rating

    @staticmethod
    def update_rating(db: Session, user_id: int, movie_id: int, rating_data: RatingCreate) -> Rating:
        rating = db.query(Rating).filter(
            Rating.user_id == user_id,
            Rating.movie_id == movie_id
        ).first()
        
        if not rating:
            raise ValueError("您还没有评分该电影")
        
        rating.score = rating_data.score
        db.commit()
        db.refresh(rating)
        
        return rating

    @staticmethod
    def get_user_rating(db: Session, user_id: int, movie_id: int) -> Rating | None:
        return db.query(Rating).filter(
            Rating.user_id == user_id,
            Rating.movie_id == movie_id
        ).first()
```

- [ ] **Step 3: 运行评分服务测试**

Run:
```bash
cd backend && python -m pytest tests/test_services/test_rating_service.py -v
```

Expected: PASS

- [ ] **Step 4: 提交评分服务**

Run:
```bash
git add backend/app/services/rating_service.py backend/tests/test_services/test_rating_service.py
git commit -m "feat: 添加评分服务"
```

---

### Task 14: 创建评论服务层

**Files:**
- Create: `backend/app/services/comment_service.py`
- Test: `backend/tests/test_services/test_comment_service.py`

- [ ] **Step 1: 编写评论服务测试**

Create `backend/tests/test_services/test_comment_service.py`:
```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models.user import User
from app.models.movie import Movie
from app.models.comment import Comment
from app.services.comment_service import CommentService
from app.schemas.comment import CommentCreate, CommentUpdate


@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    SessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()


@pytest.fixture
def test_user(db):
    user = User(
        email="test@example.com",
        username="testuser",
        password_hash="hashed_password"
    )
    db.add(user)
    db.commit()
    return user


@pytest.fixture
def test_movie(db):
    movie = Movie(
        title="测试电影",
        source="douban",
        source_id="12345"
    )
    db.add(movie)
    db.commit()
    return movie


def test_create_comment(db, test_user, test_movie):
    comment_data = CommentCreate(content="这是一条测试评论")
    
    comment = CommentService.create_comment(db, test_user.id, test_movie.id, comment_data)
    
    assert comment.id is not None
    assert comment.user_id == test_user.id
    assert comment.movie_id == test_movie.id
    assert comment.content == "这是一条测试评论"


def test_get_comments_by_movie(db, test_user, test_movie):
    comment_data1 = CommentCreate(content="第一条评论")
    comment_data2 = CommentCreate(content="第二条评论")
    
    CommentService.create_comment(db, test_user.id, test_movie.id, comment_data1)
    CommentService.create_comment(db, test_user.id, test_movie.id, comment_data2)
    
    comments, total = CommentService.get_comments_by_movie(db, test_movie.id, page=1, page_size=10)
    
    assert len(comments) == 2
    assert total == 2


def test_get_comments_pagination(db, test_user, test_movie):
    for i in range(5):
        comment_data = CommentCreate(content=f"评论{i+1}")
        CommentService.create_comment(db, test_user.id, test_movie.id, comment_data)
    
    comments, total = CommentService.get_comments_by_movie(db, test_movie.id, page=1, page_size=2)
    
    assert len(comments) == 2
    assert total == 5


def test_update_comment(db, test_user, test_movie):
    comment_data = CommentCreate(content="原始评论")
    comment = CommentService.create_comment(db, test_user.id, test_movie.id, comment_data)
    
    update_data = CommentUpdate(content="更新后的评论")
    updated_comment = CommentService.update_comment(db, comment.id, test_user.id, update_data)
    
    assert updated_comment.content == "更新后的评论"


def test_update_comment_not_owner(db, test_user, test_movie):
    comment_data = CommentCreate(content="原始评论")
    comment = CommentService.create_comment(db, test_user.id, test_movie.id, comment_data)
    
    user2 = User(email="user2@example.com", username="user2", password_hash="hash")
    db.add(user2)
    db.commit()
    
    update_data = CommentUpdate(content="更新后的评论")
    
    with pytest.raises(ValueError, match="无权修改此评论"):
        CommentService.update_comment(db, comment.id, user2.id, update_data)


def test_delete_comment(db, test_user, test_movie):
    comment_data = CommentCreate(content="要删除的评论")
    comment = CommentService.create_comment(db, test_user.id, test_movie.id, comment_data)
    
    CommentService.delete_comment(db, comment.id, test_user.id)
    
    comments, total = CommentService.get_comments_by_movie(db, test_movie.id, page=1, page_size=10)
    assert total == 0


def test_delete_comment_not_owner(db, test_user, test_movie):
    comment_data = CommentCreate(content="要删除的评论")
    comment = CommentService.create_comment(db, test_user.id, test_movie.id, comment_data)
    
    user2 = User(email="user2@example.com", username="user2", password_hash="hash")
    db.add(user2)
    db.commit()
    
    with pytest.raises(ValueError, match="无权删除此评论"):
        CommentService.delete_comment(db, comment.id, user2.id)
```

- [ ] **Step 2: 创建评论服务**

Create `backend/app/services/comment_service.py`:
```python
from sqlalchemy.orm import Session
from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentUpdate


class CommentService:
    @staticmethod
    def create_comment(db: Session, user_id: int, movie_id: int, comment_data: CommentCreate) -> Comment:
        comment = Comment(
            user_id=user_id,
            movie_id=movie_id,
            content=comment_data.content
        )
        
        db.add(comment)
        db.commit()
        db.refresh(comment)
        
        return comment

    @staticmethod
    def get_comments_by_movie(db: Session, movie_id: int, page: int = 1, page_size: int = 20) -> tuple[list[Comment], int]:
        offset = (page - 1) * page_size
        query = db.query(Comment).filter(Comment.movie_id == movie_id)
        
        total = query.count()
        comments = query.order_by(Comment.created_at.desc()).offset(offset).limit(page_size).all()
        
        return comments, total

    @staticmethod
    def update_comment(db: Session, comment_id: int, user_id: int, comment_data: CommentUpdate) -> Comment:
        comment = db.query(Comment).filter(Comment.id == comment_id).first()
        
        if not comment:
            raise ValueError("评论不存在")
        
        if comment.user_id != user_id:
            raise ValueError("无权修改此评论")
        
        comment.content = comment_data.content
        db.commit()
        db.refresh(comment)
        
        return comment

    @staticmethod
    def delete_comment(db: Session, comment_id: int, user_id: int) -> None:
        comment = db.query(Comment).filter(Comment.id == comment_id).first()
        
        if not comment:
            raise ValueError("评论不存在")
        
        if comment.user_id != user_id:
            raise ValueError("无权删除此评论")
        
        db.delete(comment)
        db.commit()
```

- [ ] **Step 3: 运行评论服务测试**

Run:
```bash
cd backend && python -m pytest tests/test_services/test_comment_service.py -v
```

Expected: PASS

- [ ] **Step 4: 提交评论服务**

Run:
```bash
git add backend/app/services/comment_service.py backend/tests/test_services/test_comment_service.py
git commit -m "feat: 添加评论服务"
```

---

### Task 15: 创建API路由 - 认证

**Files:**
- Create: `backend/app/api/__init__.py`
- Create: `backend/app/api/auth.py`
- Create: `backend/app/main.py`
- Test: `backend/tests/test_api/test_auth_api.py`

- [ ] **Step 1: 创建api包**

Run:
```bash
mkdir -p backend/app/api backend/tests/test_api
touch backend/app/api/__init__.py backend/tests/test_api/__init__.py
```

- [ ] **Step 2: 编写认证API测试**

Create `backend/tests/test_api/test_auth_api.py`:
```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app


@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    SessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()


@pytest.fixture
def client(db):
    def override_get_db():
        yield db
    
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_register(client):
    response = client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "username": "testuser",
        "password": "password123",
        "confirm_password": "password123"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "SUCCESS"
    assert data["message"] == "注册成功"
    assert "user_id" in data["data"]


def test_register_duplicate_email(client):
    client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "username": "testuser",
        "password": "password123",
        "confirm_password": "password123"
    })
    
    response = client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "username": "testuser2",
        "password": "password123",
        "confirm_password": "password123"
    })
    
    assert response.status_code == 400
    data = response.json()
    assert data["code"] == "DUPLICATE_EMAIL"


def test_login(client):
    client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "username": "testuser",
        "password": "password123",
        "confirm_password": "password123"
    })
    
    response = client.post("/api/v1/auth/login", json={
        "email": "test@example.com",
        "password": "password123"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "SUCCESS"
    assert data["message"] == "登录成功"
    assert "token" in data["data"]
    assert "user" in data["data"]


def test_login_wrong_password(client):
    client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "username": "testuser",
        "password": "password123",
        "confirm_password": "password123"
    })
    
    response = client.post("/api/v1/auth/login", json={
        "email": "test@example.com",
        "password": "wrongpassword"
    })
    
    assert response.status_code == 401
    data = response.json()
    assert data["code"] == "WRONG_PASSWORD"
```

- [ ] **Step 3: 创建认证API路由**

Create `backend/app/api/auth.py`:
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.auth_service import AuthService
from app.utils.response import success_response, error_response

router = APIRouter(prefix="/api/v1/auth", tags=["认证"])


@router.post("/register")
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        user = AuthService.register_user(db, user_data)
        return success_response({"user_id": user.id}, "注册成功")
    except ValueError as e:
        error_code = "DUPLICATE_EMAIL" if "邮箱" in str(e) else "DUPLICATE_USERNAME"
        return error_response(error_code, str(e))


@router.post("/login")
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    try:
        token, user = AuthService.login_user(db, login_data)
        return success_response({
            "token": token,
            "user": UserResponse.model_validate(user).model_dump()
        }, "登录成功")
    except ValueError as e:
        error_code = "WRONG_PASSWORD" if "密码" in str(e) else "USER_NOT_FOUND"
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error_response(error_code, str(e))
        )


@router.post("/logout")
def logout():
    return success_response(message="登出成功")
```

- [ ] **Step 4: 创建FastAPI主应用**

Create `backend/app/main.py`:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth

app = FastAPI(title="电影评分网站API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "电影评分网站API"}
```

- [ ] **Step 5: 运行认证API测试**

Run:
```bash
cd backend && python -m pytest tests/test_api/test_auth_api.py -v
```

Expected: PASS

- [ ] **Step 6: 提交认证API**

Run:
```bash
git add backend/app/api/ backend/app/main.py backend/tests/test_api/
git commit -m "feat: 添加认证API路由"
```

---

### Task 16: 创建API路由 - 用户管理

**Files:**
- Create: `backend/app/api/users.py`
- Create: `backend/app/api/deps.py`
- Test: `backend/tests/test_api/test_user_api.py`

- [ ] **Step 1: 创建依赖注入模块**

Create `backend/app/api/deps.py`:
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.utils.auth import verify_token
from app.utils.response import error_response

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    token = credentials.credentials
    payload = verify_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error_response("UNAUTHORIZED", "无效的认证令牌")
        )
    
    user_id = payload.get("user_id")
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error_response("UNAUTHORIZED", "用户不存在")
        )
    
    return user
```

- [ ] **Step 2: 编写用户API测试**

Create `backend/tests/test_api/test_user_api.py`:
```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app


@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    SessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()


@pytest.fixture
def client(db):
    def override_get_db():
        yield db
    
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def auth_token(client):
    response = client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "username": "testuser",
        "password": "password123",
        "confirm_password": "password123"
    })
    
    response = client.post("/api/v1/auth/login", json={
        "email": "test@example.com",
        "password": "password123"
    })
    
    return response.json()["data"]["token"]


def test_get_current_user(client, auth_token):
    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "SUCCESS"
    assert data["data"]["email"] == "test@example.com"
    assert data["data"]["username"] == "testuser"


def test_get_current_user_unauthorized(client):
    response = client.get("/api/v1/users/me")
    
    assert response.status_code == 403


def test_update_password(client, auth_token):
    response = client.put(
        "/api/v1/users/me/password",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "old_password": "password123",
            "new_password": "newpassword456",
            "confirm_password": "newpassword456"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "SUCCESS"
    assert data["message"] == "密码修改成功"


def test_update_password_wrong_old(client, auth_token):
    response = client.put(
        "/api/v1/users/me/password",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "old_password": "wrongpassword",
            "new_password": "newpassword456",
            "confirm_password": "newpassword456"
        }
    )
    
    assert response.status_code == 400
    data = response.json()
    assert data["code"] == "WRONG_PASSWORD"
```

- [ ] **Step 3: 创建用户API路由**

Create `backend/app/api/users.py`:
```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse, PasswordUpdate
from app.services.user_service import UserService
from app.utils.response import success_response, error_response

router = APIRouter(prefix="/api/v1/users", tags=["用户"])


@router.get("/me")
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return success_response(UserResponse.model_validate(current_user).model_dump())


@router.put("/me/password")
def update_password(
    password_data: PasswordUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        UserService.update_password(db, current_user.id, password_data)
        return success_response(message="密码修改成功")
    except ValueError as e:
        return error_response("WRONG_PASSWORD", str(e))
```

- [ ] **Step 4: 更新main.py添加用户路由**

Modify `backend/app/main.py`:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, users

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


@app.get("/")
def root():
    return {"message": "电影评分网站API"}
```

- [ ] **Step 5: 运行用户API测试**

Run:
```bash
cd backend && python -m pytest tests/test_api/test_user_api.py -v
```

Expected: PASS

- [ ] **Step 6: 提交用户API**

Run:
```bash
git add backend/app/api/users.py backend/app/api/deps.py backend/app/main.py backend/tests/test_api/test_user_api.py
git commit -m "feat: 添加用户管理API路由"
```

---

由于计划文档过长，我将继续创建剩余的任务。让我保存当前的计划文档，然后继续添加剩余部分。

---

### Task 17: 创建API路由 - 电影管理

**Files:**
- Create: `backend/app/api/movies.py`
- Test: `backend/tests/test_api/test_movie_api.py`

- [ ] **Step 1: 编写电影API测试**

Create `backend/tests/test_api/test_movie_api.py`:
```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.models.movie import Movie
from app.main import app


@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    SessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()


@pytest.fixture
def client(db):
    def override_get_db():
        yield db
    
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def test_movies(db):
    movies = []
    for i in range(5):
        movie = Movie(
            title=f"测试电影{i+1}",
            director=f"导演{i+1}",
            source="douban",
            source_id=str(i+1)
        )
        db.add(movie)
        movies.append(movie)
    db.commit()
    return movies


def test_get_movies(client, test_movies):
    response = client.get("/api/v1/movies")
    
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "SUCCESS"
    assert len(data["data"]["movies"]) == 5
    assert data["data"]["total"] == 5


def test_get_movies_pagination(client, test_movies):
    response = client.get("/api/v1/movies?page=1&page_size=2")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]["movies"]) == 2
    assert data["data"]["total"] == 5


def test_get_movie_by_id(client, test_movies):
    response = client.get(f"/api/v1/movies/{test_movies[0].id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "SUCCESS"
    assert data["data"]["id"] == test_movies[0].id
    assert data["data"]["title"] == test_movies[0].title


def test_get_movie_by_id_not_found(client):
    response = client.get("/api/v1/movies/999")
    
    assert response.status_code == 404
    data = response.json()
    assert data["code"] == "NOT_FOUND"
```

- [ ] **Step 2: 创建电影API路由**

Create `backend/app/api/movies.py`:
```python
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
```

- [ ] **Step 3: 更新main.py添加电影路由**

Modify `backend/app/main.py`:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, users, movies

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


@app.get("/")
def root():
    return {"message": "电影评分网站API"}
```

- [ ] **Step 4: 运行电影API测试**

Run:
```bash
cd backend && python -m pytest tests/test_api/test_movie_api.py -v
```

Expected: PASS

- [ ] **Step 5: 提交电影API**

Run:
```bash
git add backend/app/api/movies.py backend/app/main.py backend/tests/test_api/test_movie_api.py
git commit -m "feat: 添加电影管理API路由"
```

---

### Task 18: 创建API路由 - 评分管理

**Files:**
- Create: `backend/app/api/ratings.py`
- Test: `backend/tests/test_api/test_rating_api.py`

- [ ] **Step 1: 编写评分API测试**

Create `backend/tests/test_api/test_rating_api.py`:
```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.models.user import User
from app.models.movie import Movie
from app.main import app
from app.utils.auth import hash_password


@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    SessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()


@pytest.fixture
def client(db):
    def override_get_db():
        yield db
    
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db):
    user = User(
        email="test@example.com",
        username="testuser",
        password_hash=hash_password("password123")
    )
    db.add(user)
    db.commit()
    return user


@pytest.fixture
def test_movie(db):
    movie = Movie(
        title="测试电影",
        source="douban",
        source_id="12345"
    )
    db.add(movie)
    db.commit()
    return movie


@pytest.fixture
def auth_token(client, test_user):
    response = client.post("/api/v1/auth/login", json={
        "email": "test@example.com",
        "password": "password123"
    })
    return response.json()["data"]["token"]


def test_create_rating(client, auth_token, test_movie):
    response = client.post(
        f"/api/v1/movies/{test_movie.id}/ratings",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"score": 5}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "SUCCESS"
    assert data["message"] == "评分成功"


def test_create_rating_unauthorized(client, test_movie):
    response = client.post(
        f"/api/v1/movies/{test_movie.id}/ratings",
        json={"score": 5}
    )
    
    assert response.status_code == 403


def test_get_user_rating(client, auth_token, test_movie):
    client.post(
        f"/api/v1/movies/{test_movie.id}/ratings",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"score": 5}
    )
    
    response = client.get(
        f"/api/v1/movies/{test_movie.id}/ratings/me",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "SUCCESS"
    assert data["data"]["score"] == 5
```

- [ ] **Step 2: 创建评分API路由**

Create `backend/app/api/ratings.py`:
```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.rating import RatingCreate, RatingResponse
from app.services.rating_service import RatingService
from app.utils.response import success_response, error_response

router = APIRouter(tags=["评分"])


@router.post("/api/v1/movies/{movie_id}/ratings")
def create_rating(
    movie_id: int,
    rating_data: RatingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        RatingService.create_rating(db, current_user.id, movie_id, rating_data)
        return success_response(message="评分成功")
    except ValueError as e:
        return error_response("ALREADY_RATED", str(e))


@router.put("/api/v1/movies/{movie_id}/ratings")
def update_rating(
    movie_id: int,
    rating_data: RatingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        RatingService.update_rating(db, current_user.id, movie_id, rating_data)
        return success_response(message="评分更新成功")
    except ValueError as e:
        return error_response("NOT_RATED", str(e))


@router.get("/api/v1/movies/{movie_id}/ratings/me")
def get_user_rating(
    movie_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    rating = RatingService.get_user_rating(db, current_user.id, movie_id)
    
    if not rating:
        return success_response({"score": None})
    
    return success_response({"score": rating.score})
```

- [ ] **Step 3: 更新main.py添加评分路由**

Modify `backend/app/main.py`:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, users, movies, ratings

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


@app.get("/")
def root():
    return {"message": "电影评分网站API"}
```

- [ ] **Step 4: 运行评分API测试**

Run:
```bash
cd backend && python -m pytest tests/test_api/test_rating_api.py -v
```

Expected: PASS

- [ ] **Step 5: 提交评分API**

Run:
```bash
git add backend/app/api/ratings.py backend/app/main.py backend/tests/test_api/test_rating_api.py
git commit -m "feat: 添加评分管理API路由"
```

---

### Task 19: 创建API路由 - 评论管理

**Files:**
- Create: `backend/app/api/comments.py`
- Test: `backend/tests/test_api/test_comment_api.py`

- [ ] **Step 1: 编写评论API测试**

Create `backend/tests/test_api/test_comment_api.py`:
```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.models.user import User
from app.models.movie import Movie
from app.main import app
from app.utils.auth import hash_password


@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    SessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()


@pytest.fixture
def client(db):
    def override_get_db():
        yield db
    
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db):
    user = User(
        email="test@example.com",
        username="testuser",
        password_hash=hash_password("password123")
    )
    db.add(user)
    db.commit()
    return user


@pytest.fixture
def test_movie(db):
    movie = Movie(
        title="测试电影",
        source="douban",
        source_id="12345"
    )
    db.add(movie)
    db.commit()
    return movie


@pytest.fixture
def auth_token(client, test_user):
    response = client.post("/api/v1/auth/login", json={
        "email": "test@example.com",
        "password": "password123"
    })
    return response.json()["data"]["token"]


def test_create_comment(client, auth_token, test_movie):
    response = client.post(
        f"/api/v1/movies/{test_movie.id}/comments",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"content": "这是一条测试评论"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "SUCCESS"
    assert data["message"] == "评论成功"


def test_get_comments(client, auth_token, test_movie):
    client.post(
        f"/api/v1/movies/{test_movie.id}/comments",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"content": "第一条评论"}
    )
    
    response = client.get(f"/api/v1/movies/{test_movie.id}/comments")
    
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "SUCCESS"
    assert len(data["data"]["comments"]) == 1


def test_update_comment(client, auth_token, test_movie):
    response = client.post(
        f"/api/v1/movies/{test_movie.id}/comments",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"content": "原始评论"}
    )
    comment_id = response.json()["data"]["comment_id"]
    
    response = client.put(
        f"/api/v1/comments/{comment_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"content": "更新后的评论"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "SUCCESS"


def test_delete_comment(client, auth_token, test_movie):
    response = client.post(
        f"/api/v1/movies/{test_movie.id}/comments",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"content": "要删除的评论"}
    )
    comment_id = response.json()["data"]["comment_id"]
    
    response = client.delete(
        f"/api/v1/comments/{comment_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "SUCCESS"
```

- [ ] **Step 2: 创建评论API路由**

Create `backend/app/api/comments.py`:
```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentUpdate
from app.services.comment_service import CommentService
from app.utils.response import success_response, error_response

router = APIRouter(tags=["评论"])


@router.post("/api/v1/movies/{movie_id}/comments")
def create_comment(
    movie_id: int,
    comment_data: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    comment = CommentService.create_comment(db, current_user.id, movie_id, comment_data)
    return success_response({"comment_id": comment.id}, "评论成功")


@router.get("/api/v1/movies/{movie_id}/comments")
def get_comments(
    movie_id: int,
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db)
):
    comments, total = CommentService.get_comments_by_movie(db, movie_id, page, page_size)
    
    comment_responses = []
    for comment in comments:
        comment_dict = {
            "id": comment.id,
            "user_id": comment.user_id,
            "username": comment.user.username,
            "content": comment.content,
            "created_at": comment.created_at.isoformat(),
            "updated_at": comment.updated_at.isoformat()
        }
        comment_responses.append(comment_dict)
    
    return success_response({
        "comments": comment_responses,
        "total": total,
        "page": page,
        "page_size": page_size
    })


@router.put("/api/v1/comments/{comment_id}")
def update_comment(
    comment_id: int,
    comment_data: CommentUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        CommentService.update_comment(db, comment_id, current_user.id, comment_data)
        return success_response(message="评论更新成功")
    except ValueError as e:
        return error_response("FORBIDDEN", str(e))


@router.delete("/api/v1/comments/{comment_id}")
def delete_comment(
    comment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        CommentService.delete_comment(db, comment_id, current_user.id)
        return success_response(message="评论删除成功")
    except ValueError as e:
        return error_response("FORBIDDEN", str(e))
```

- [ ] **Step 3: 更新main.py添加评论路由**

Modify `backend/app/main.py`:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, users, movies, ratings, comments

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


@app.get("/")
def root():
    return {"message": "电影评分网站API"}
```

- [ ] **Step 4: 运行评论API测试**

Run:
```bash
cd backend && python -m pytest tests/test_api/test_comment_api.py -v
```

Expected: PASS

- [ ] **Step 5: 提交评论API**

Run:
```bash
git add backend/app/api/comments.py backend/app/main.py backend/tests/test_api/test_comment_api.py
git commit -m "feat: 添加评论管理API路由"
```

---

### Task 20: 创建API路由 - 统计信息

**Files:**
- Create: `backend/app/api/stats.py`
- Test: `backend/tests/test_api/test_stats_api.py`

- [ ] **Step 1: 编写统计API测试**

Create `backend/tests/test_api/test_stats_api.py`:
```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.models.user import User
from app.models.movie import Movie
from app.models.comment import Comment
from app.main import app
from app.utils.auth import hash_password


@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    SessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()


@pytest.fixture
def client(db):
    def override_get_db():
        yield db
    
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def test_data(db):
    user = User(
        email="test@example.com",
        username="testuser",
        password_hash=hash_password("password123")
    )
    db.add(user)
    
    movie = Movie(
        title="测试电影",
        source="douban",
        source_id="12345"
    )
    db.add(movie)
    db.commit()
    
    comment = Comment(
        user_id=user.id,
        movie_id=movie.id,
        content="测试评论"
    )
    db.add(comment)
    db.commit()


def test_get_stats(client, test_data):
    response = client.get("/api/v1/stats")
    
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "SUCCESS"
    assert data["data"]["movie_count"] == 1
    assert data["data"]["user_count"] == 1
    assert data["data"]["comment_count"] == 1
```

- [ ] **Step 2: 创建统计API路由**

Create `backend/app/api/stats.py`:
```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.user import User
from app.models.movie import Movie
from app.models.comment import Comment
from app.utils.response import success_response

router = APIRouter(prefix="/api/v1/stats", tags=["统计"])


@router.get("")
def get_stats(db: Session = Depends(get_db)):
    movie_count = db.query(func.count(Movie.id)).scalar()
    user_count = db.query(func.count(User.id)).scalar()
    comment_count = db.query(func.count(Comment.id)).scalar()
    
    return success_response({
        "movie_count": movie_count,
        "user_count": user_count,
        "comment_count": comment_count
    })
```

- [ ] **Step 3: 更新main.py添加统计路由**

Modify `backend/app/main.py`:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, users, movies, ratings, comments, stats

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


@app.get("/")
def root():
    return {"message": "电影评分网站API"}
```

- [ ] **Step 4: 运行统计API测试**

Run:
```bash
cd backend && python -m pytest tests/test_api/test_stats_api.py -v
```

Expected: PASS

- [ ] **Step 5: 提交统计API**

Run:
```bash
git add backend/app/api/stats.py backend/app/main.py backend/tests/test_api/test_stats_api.py
git commit -m "feat: 添加统计信息API路由"
```

---

## 阶段四：数据爬取

由于篇幅限制，剩余的任务（数据爬取、前端开发、集成测试与优化、部署与交付）将在后续文档中继续补充。当前计划已覆盖后端核心功能的完整实现。
